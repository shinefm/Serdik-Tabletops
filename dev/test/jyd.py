import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1280,'height':900})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='jyd_lobby.png')
        await pg.click('[data-act="jylocal"]'); await pg.wait_for_timeout(300); await pg.click('[data-act="jylocalgo"]'); await pg.wait_for_timeout(800)
        await pg.evaluate("ui.jy.a={hr:300,op:450,mk:100,sl:250};render()"); await pg.click('[data-act="jyalloc"]')
        await pg.evaluate("ui.jy.h=[0,0,2];render()"); await pg.click('[data-act="jyhr"]')
        await pg.evaluate("ui.jy.m={H:3,M:0,L:0};render()"); await pg.click('[data-act="jyop"]')
        await pg.evaluate("ui.jy.cr=2;render()"); await pg.click('[data-act="jymk"]'); await pg.wait_for_timeout(2500)
        await pg.evaluate("closeModal()")
        c=await pg.query_selector('.jyc[data-act="jycell"]')
        if c: await c.click()
        await pg.wait_for_timeout(300); await pg.screenshot(path='jyd_sell.png')
        print(errs); await b.close()
asyncio.run(main())
