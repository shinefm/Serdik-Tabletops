import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for W,H,dsf in [(1300,900,1),(390,844,2)]:
            pg=await b.new_page(viewport={'width':W,'height':H},device_scale_factor=dsf); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
            await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
            await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
            await pg.select_option('#lpOrd','1'); await pg.click('#mbox .btn.pri'); await pg.wait_for_timeout(900)
            await pg.screenshot(path=f'pop_rank_{W}.png')
            await pg.evaluate("toast('Valckenier mengambil 2 🟢 Hijau')"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'pop_toast_{W}.png'); print(W,errs)
        await b.close()
asyncio.run(main())
