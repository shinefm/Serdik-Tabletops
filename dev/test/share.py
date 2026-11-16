import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
        await pg.fill('#nickIn','Farhan'); await pg.fill('#tblIn','Meja Serdik')
        await pg.tap('[data-act="create"]'); await pg.wait_for_timeout(800)
        await pg.screenshot(path='share.png')
        print(await pg.get_attribute('a.wa','href'))
        print(await pg.evaluate("location.hash"), errs); await b.close()
asyncio.run(main())
