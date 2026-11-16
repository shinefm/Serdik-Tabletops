import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':760},device_scale_factor=2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="jylocal"]'); await pg.wait_for_timeout(300); await pg.click('[data-act="jylocalgo"]'); await pg.wait_for_timeout(800)
        for i in range(200):
            if await pg.evaluate("cur.st.round")>=2: break
            await pg.evaluate("""(()=>{if(modalOpen())closeModal();const w=jyWaiting(cur.st).find(w=>w.t===0);if(!w)return;if(w.div==='sl')jyMove(jyBotSell(cur.st,0));else{ui.jy=null;jyForm(cur.st).d=jyBotPlan(cur.st,0);jyReady();}})()""")
            await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(1200); await pg.evaluate("closeModal();ui.jySum=true;ui.jy=null;jyForm(cur.st).d={H:1};render()")
        el=await pg.query_selector('.jytotal'); await el.screenshot(path='jysum.png'); print(await pg.evaluate("JSON.stringify([cur.st.recap,cur.st.teams[0].cash])"),errs)
        await b.close()
asyncio.run(main())
