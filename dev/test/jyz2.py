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
        await pg.click('.jyc.qM >> nth=1'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='jyz2.png'); await pg.evaluate("closeModal();ui.jyOpen={sl:1};render()"); el=await pg.query_selector('.jyacc.open'); await el.screenshot(path='jyz3.png'); print(errs)
        await b.close()
asyncio.run(main())
