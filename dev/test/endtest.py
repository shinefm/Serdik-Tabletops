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
async def finish(pg,duel=False):
    if duel: await pg.evaluate("(()=>{const st=cur.st;const me=st.players[cur.human];me.cards=Object.keys(CARDS).filter(id=>CARDS[id].duel&&CARDS[id].tier===3&&!CARDS[id].wild).slice(0,6);render();})()")
    else: await pg.evaluate("(()=>{const st=cur.st;st.players[cur.human].cards=['3r1','3k1','3u1','2g4'];st.endTriggered=true;render();})()")
    for k in range(40):
        if await pg.evaluate("cur.st.status")=='ended': break
        if await pg.evaluate("cur.st.turn===cur.human"): await pg.evaluate("(async()=>{await runMove({type:'pass'});})()")
        await pg.wait_for_timeout(250)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,tag,mode in [({'width':1280,'height':860},'d','klasik'),({'width':390,'height':844},'m','klasik'),({'width':390,'height':844},'md','duel')]:
            pg,errs=await page(b,vw); await startLocal(pg,mode)
            await pg.evaluate("window.scrollTo(0,document.body.scrollHeight)")
            await finish(pg,mode=='duel'); await pg.wait_for_timeout(1200)
            open_=await pg.evaluate("document.getElementById('modal').classList.contains('open')")
            txt=(await pg.inner_text('#mbox'))[:140].replace('\n',' | ')
            await pg.screenshot(path=f'end_{tag}.png')
            await pg.click('#mbox [data-act="close"]'); await pg.wait_for_timeout(300)
            pill=await pg.evaluate("!!document.querySelector('.endpill')")
            await pg.screenshot(path=f'end_{tag}_pill.png')
            await pg.click('.endpill'); await pg.wait_for_timeout(200)
            re_=await pg.evaluate("document.getElementById('modal').classList.contains('open')")
            await pg.click('#mbox [data-act="lobby"]'); await pg.wait_for_timeout(300)
            print(tag,'popup:',open_,txt,'| pill:',pill,'reopen:',re_,'-> view',await pg.evaluate("view"),errs)
        await b.close()
asyncio.run(main())
