import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/pub/latihan/index.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="onlineinfo"]'); await pg.wait_for_timeout(300)
        print((await pg.inner_text('#mbox'))[:120].replace('\n',' | '),errs)
        await pg.screenshot(path='oinfo.png')
        await b.close()
asyncio.run(main())
