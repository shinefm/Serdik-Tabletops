import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/pub/index.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="tutorial"][data-w="jualan"]'); await pg.wait_for_timeout(1500)
        print(await pg.evaluate("(()=>{const v=document.querySelector('#mbox video');return v?[v.getAttribute('src'),v.readyState,Math.round(v.duration)]:null})()"),errs)
        await pg.screenshot(path='jytut.png')
        await b.close()
asyncio.run(main())
