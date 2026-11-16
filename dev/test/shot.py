import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':1000})
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html')
        await pg.wait_for_timeout(2500)
        await pg.click('[data-act="localSetup"]'); await pg.click('[data-act="localStart"]')
        await pg.wait_for_timeout(800)
        await pg.screenshot(path='board.png',full_page=True)
        await pg.click('[data-act="card"]'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='modal.png')
        await b.close()
asyncio.run(main())
