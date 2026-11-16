import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':760})
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="jylocal"]'); await pg.wait_for_timeout(300); await pg.click('[data-act="jylocalgo"]'); await pg.wait_for_timeout(800)
        print(await pg.evaluate("JSON.stringify(ui.jyOpen)"))
        await pg.click('[data-act="jyacc"][data-d="op"]'); await pg.wait_for_timeout(200)
        print(await pg.evaluate("JSON.stringify(ui.jyOpen)"), await pg.evaluate("!!document.querySelector('[data-k=H]')"))
        await pg.click('[data-act="jyacc"][data-d="hr"]'); await pg.wait_for_timeout(200)
        print(await pg.evaluate("JSON.stringify(ui.jyOpen)"), await pg.evaluate("!!document.querySelector('[data-k=h2]')"))
        await pg.click('[data-act="jyhelp"]'); print('help',await pg.evaluate("ui.jyHelpOpen"))
        await pg.click('.jyc'); await pg.wait_for_timeout(200); print('modal',await pg.evaluate("modalOpen()"))
        await b.close()
asyncio.run(main())
