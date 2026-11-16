import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='jy_lobby.png',full_page=False)
        await pg.click('[data-act="jylocal"]'); await pg.wait_for_timeout(300)
        await pg.select_option('#jyNb','2'); await pg.click('[data-act="jylocalgo"]'); await pg.wait_for_timeout(800)
        await pg.screenshot(path='jy_plan_fin.png',full_page=True)
        await pg.screenshot(path='jy_plan_closed.png',full_page=True)
        await pg.evaluate("ui.jyOpen={hr:1,op:1,mk:1,sl:1};render()")
        for k,n in [('h2',2),('H',3),('cr',2),('sl',5)]:
            for _ in range(n): await pg.click(f'[data-act="jyinc"][data-k="{k}"][data-d="1"]')
        await pg.screenshot(path='jy_plan_hr.png',full_page=True)
        print('draft',await pg.evaluate("JSON.stringify(cur.st.teams[0].draft)"))
        await pg.click('[data-act="jyready"]'); await pg.wait_for_timeout(2500)
        print('phase',await pg.evaluate("JSON.stringify({ph:cur.st.phase,order:cur.st.order,si:cur.st.si})"))
        await pg.evaluate("closeModal()")
        # wait my sell turn
        for i in range(30):
            ok=await pg.evaluate("cur.st.phase==='sell'&&cur.st.order[cur.st.si]===0")
            if ok:break
            await pg.wait_for_timeout(700)
        await pg.evaluate("closeModal()")
        await pg.screenshot(path='jy_sell_pick.png',full_page=True)
        cell=await pg.query_selector('.jyc[data-act="jycell"]')
        if cell:
            await cell.click(); await pg.wait_for_timeout(200)
            await pg.click('[data-act="jyk"][data-k="2"]'); await pg.wait_for_timeout(200)
            await pg.screenshot(path='jy_sell_form.png',full_page=True)
            await pg.click('[data-act="jysell"]'); await pg.wait_for_timeout(600)
            await pg.screenshot(path='jy_sell_draw.png',full_page=True)
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path='jy_sell_draw2.png',full_page=True)
        # autoplay rest
        for i in range(400):
            st=json.loads(await pg.evaluate("JSON.stringify({s:cur.st.status,ph:cur.st.phase,r:cur.st.round})"))
            if st['s']!='playing':break
            await pg.evaluate("""(()=>{if(modalOpen())closeModal();const w=jyWaiting(cur.st).find(w=>w.t===0);if(!w)return;if(w.div==='sl')jyMove(jyBotSell(cur.st,0));else{ui.jy=null;jyForm(cur.st).d=jyBotPlan(cur.st,0);jyReady();}})()""")
            await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(1500)
        print('end',await pg.evaluate("JSON.stringify({s:cur.st.status,cash:cur.st.teams.map(T=>T.cash),stars:cur.st.teams.map(T=>T.stars),w:cur.st.winner})"))
        await pg.screenshot(path='jy_end.png',full_page=False)
        print('errs',errs)
        await b.close()
asyncio.run(main())
