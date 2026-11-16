import asyncio
from playwright.async_api import async_playwright
async def run(b,vw,mode,tag):
    ctx=await b.new_context(viewport={'width':vw[0],'height':vw[1]},device_scale_factor=1 if vw[0]>800 else 2)
    pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
    await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
    await pg.evaluate("c0delay=()=>150")
    await pg.click('[data-act="tutorial"]'); await pg.wait_for_timeout(300)
    if mode=='duel': await pg.click('.tabs [data-w="duel"]'); await pg.wait_for_timeout(200)
    await pg.click('[data-act="guided"]'); await pg.wait_for_timeout(500)
    log=[]; shots=0; blocked_ok=None
    for it in range(200):
        info=await pg.evaluate("""()=>{const g=ui.guide;if(!g)return null;const s=g.steps[g.i];const st=cur.st;const myT=st.turn===cur.human;
           return {i:g.i,t:s.t||'wait',next:!!s.next,wait:!!s.wait||(s.turn&&!myT),sels:(s.sel&&!(s.wait||(s.turn&&!myT)))?s.sel(g):[]};}""")
        if info is None: break
        if not log or log[-1]!=info['t']: log.append(info['t'])
        if shots<4 and not info['wait'] and info['sels'] and it%2==0:
            await pg.screenshot(path=f'g_{tag}_{shots}.png'); shots+=1
        if info['wait']: await pg.wait_for_timeout(300); continue
        if info['next']: await pg.click('#gd [data-act="guidenext"]'); await pg.wait_for_timeout(300); continue
        if blocked_ok is None and info['sels']:
            before=await pg.evaluate("cur.st.log.length")
            await pg.evaluate("(()=>{const b=document.querySelector('[data-act=\"pass\"]');if(b)b.click();})()"); await pg.wait_for_timeout(300)
            blocked_ok=(await pg.evaluate("cur.st.log.length"))==before and not await pg.evaluate("document.getElementById('modal').classList.contains('open')")
        i0=info['i']
        for sel in info['sels']:
            await pg.evaluate("s=>{const e=document.querySelector(s);if(e)e.click();}",sel); await pg.wait_for_timeout(120)
            if await pg.evaluate("ui.guide?ui.guide.i:null")!=i0: break
        await pg.wait_for_timeout(350)
        if await pg.evaluate("ui.guide?ui.guide.i:null")==i0:
            await pg.evaluate("s=>{const e=document.querySelector(s);if(e)e.click();}",info['sels'][0]); await pg.wait_for_timeout(350)
    end=await pg.evaluate("({guide:!!ui.guide,status:cur.st.status,me:cur.st.players[cur.human].cards.length,res:cur.st.players[cur.human].res.length,store:Object.keys(__store).length})")
    print(tag,'steps:',' > '.join(log)); print(tag,'blocked non-target:',blocked_ok,'end',end,'errs',errs)
    await ctx.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        await run(b,(1280,860),'klasik','kd'); await run(b,(390,844),'klasik','km')
        await run(b,(1280,860),'duel','dd'); await run(b,(390,844),'duel','dm')
        await b.close()
asyncio.run(main())
