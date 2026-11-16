import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':1000})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(2000)
        await pg.click('[data-act="localSetup"]'); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(600)
        await pg.screenshot(path='pat_game.png',clip={'x':0,'y':80,'width':790,'height':320})
        await pg.click('[data-act="patron"]'); await pg.wait_for_timeout(300)
        el=await pg.query_selector('.mbox'); await el.screenshot(path='pat_modal.png')
        print(errs); await b.close()
asyncio.run(main())
