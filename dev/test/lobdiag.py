import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        print(await pg.evaluate("$('#acctLine').textContent"))
        await pg.evaluate("ui.lobbyErr='permission-denied';lobbyGames=[];render()")
        await pg.wait_for_timeout(300)
        el=await pg.query_selector('#tableList'); await el.scroll_into_view_if_needed(); await pg.screenshot(path='lobdiag.png')
        await pg.click('#tableList [data-act="reconnect"]'); await pg.wait_for_timeout(800)
        print('after retry',await pg.evaluate("$('#lobbyStatus').textContent"))
        print('errs',errs); await b.close()
asyncio.run(main())
