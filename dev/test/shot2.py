import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(2000)
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
        await pg.select_option('#lpN','3'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='setup.png')
        await pg.fill('.lpName >> nth=0','Bot Pak Dosen')
        await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(500)
        for c in ['w','u','g']: await pg.click(f'[data-act="tok"][data-c="{c}"]')
        await pg.click('[data-act="take"]')
        await pg.wait_for_timeout(6000)
        await pg.screenshot(path='afterbots.png')
        print('log:',await pg.inner_text('.log'))
        print('errors:',errs)
        await b.close()
asyncio.run(main())
