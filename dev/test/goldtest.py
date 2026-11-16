import asyncio
from playwright.async_api import async_playwright
async def page(b,vw):
    pg=await b.new_page(viewport=vw,device_scale_factor=1 if vw['width']>800 else 2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
    await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
    await pg.evaluate("c0delay=()=>150"); return pg,errs
async def startLocal(pg,mode='klasik'):
    await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(250)
    if mode=='duel': await pg.click('[data-act="lpmode"][data-m="duel"]'); await pg.wait_for_timeout(100)
    await pg.evaluate("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,tag in [({'width':1280,'height':860},'d'),({'width':390,'height':844},'m')]:
            pg,errs=await page(b,vw); await startLocal(pg)
            await pg.click('[data-act="gold"]'); await pg.wait_for_timeout(200)
            n=await pg.evaluate("document.querySelectorAll('.card.gpick').length+'/'+document.querySelectorAll('.deck.gpick').length")
            await pg.screenshot(path=f'gold_{tag}.png')
            await pg.click('[data-act="card"][data-tier="2"][data-slot="1"]'); await pg.wait_for_timeout(400)
            r=await pg.evaluate("({res:cur.st.players[0].res.length,y:cur.st.players[0].t.y,modal:document.getElementById('modal').classList.contains('open'),gres:!!ui.gres,log:cur.st.log.at(-1).m})")
            print(tag,'klasik highlights',n,'->',r)
            await pg.wait_for_timeout(1500)
            # deck reserve + cancel
            await pg.click('[data-act="gold"]'); await pg.wait_for_timeout(150); await pg.click('[data-act="goldoff"]'); await pg.wait_for_timeout(150)
            c=await pg.evaluate("!!ui.gres")
            await pg.click('[data-act="gold"]'); await pg.wait_for_timeout(150)
            await pg.evaluate("document.querySelector('.deck.t3').click()"); await pg.wait_for_timeout(400)
            print(tag,'cancel ok',not c,'deck reserve:',await pg.evaluate("({res:cur.st.players[0].res.length,log:cur.st.log.filter(l=>l.p===0).at(-1).m})"))
            # tok cancels gold
            await pg.wait_for_timeout(1500)
            await pg.click('[data-act="gold"]'); await pg.wait_for_timeout(100)
            await pg.evaluate("document.querySelector('[data-act=\"tok\"][data-c=\"w\"]').click()"); await pg.wait_for_timeout(100)
            print(tag,'tok cancels gold:',await pg.evaluate("!ui.gres&&ui.sel.w===1"))
            # bot toast text sample
            print(tag,'last bot log:',await pg.evaluate("cur.st.log.filter(l=>l.p===1).map(l=>l.m).slice(-2)"),errs)
        # duel
        pg,errs=await page(b,{'width':1280,'height':860}); await startLocal(pg,'duel')
        gi=await pg.evaluate("cur.st.board.indexOf('y')")
        await pg.click(f'.dcell[data-i="{gi}"]'); await pg.wait_for_timeout(200)
        n=await pg.evaluate("document.querySelectorAll('.card.gpick').length")
        await pg.screenshot(path='gold_duel.png')
        await pg.click('[data-act="card"][data-tier="1"][data-slot="2"]'); await pg.wait_for_timeout(400)
        print('duel highlights',n,'->',await pg.evaluate(f"({{res:cur.st.players[0].res.length,y:cur.st.players[0].t.y,cellEmpty:cur.st.board[{gi}]===null,log:cur.st.log.filter(l=>l.p===0).at(-1).m}})"),errs)
        await b.close()
asyncio.run(main())
