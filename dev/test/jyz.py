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
        await pg.evaluate("cur.st.teams[0].emp=[1,1,1];cur.st.teams[0].inv={H:2,M:1,L:1};cur.st.teams[0].cr=3;cur.st.teams[0].bud.sl=100;ui.jyOpen={};render()")
        await pg.evaluate("ui.jyOpen={hr:1};ui.jy.d={h2:2,h0:1};render()")
        for k,n in []:
            for _ in range(n): await pg.click(f'[data-act="jyinc"][data-k="{k}"][data-d="1"]')
        await pg.wait_for_timeout(500)
        await pg.click('[data-act="jysum"]'); await pg.wait_for_timeout(200); await pg.click('[data-act="jysum"]'); await pg.wait_for_timeout(200)
        await pg.click('[data-act="jysum"]'); el=await pg.query_selector('.jymine'); await el.screenshot(path='jyz.png'); print(errs)
        await b.close()
asyncio.run(main())
