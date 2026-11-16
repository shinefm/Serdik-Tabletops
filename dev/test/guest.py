import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for mk,tag in [('mock_guest.js','guest'),('mock.js','member')]:
            pg=await b.new_page(viewport={'width':1100,'height':800}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/'+mk)
            if tag=='member': await pg.add_init_script(script="window.__email=1")
            await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
            await pg.screenshot(path=f'{tag}_lobby.png',clip={'x':0,'y':0,'width':1100,'height':420})
            await pg.click('#profBtn'); await pg.wait_for_timeout(500)
            el=await pg.query_selector('.mbox'); await el.screenshot(path=f'{tag}_prof.png')
            await pg.click('[data-act="close"]')
            await pg.evaluate("c0delay=()=>10")
            await pg.click('[data-act="localSetup"]'); await pg.select_option('#lpN','1'); await pg.select_option('#lpLv','easy'); await pg.click('[data-act="localStart"]')
            r=await pg.evaluate("""async()=>{let g=0;while(cur.st.status==='playing'&&g++<500){if(cur.st.turn===cur.human&&!ui.busy){await runMove(botMove(cur.st,cur.human,'normal'));}await new Promise(r=>setTimeout(r,15));}await new Promise(r=>setTimeout(r,500));return {st:cur.st.status,keys:Object.keys(__store)};}""")
            print(tag,r,errs); await pg.close()
        await b.close()
asyncio.run(main())
