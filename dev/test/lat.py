import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/pub/latihan/index.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='test/lat_hub.png')
        await pg.click('[data-act="tutorial"][data-w="rapat"]'); await pg.wait_for_timeout(300); await pg.screenshot(path='test/lat_rules.png')
        print(errs); await b.close()
asyncio.run(main())
