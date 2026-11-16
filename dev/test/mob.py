import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for mode in ['light','dark']:
            ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
            pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
            await pg.add_init_script(script=f"try{{localStorage.setItem('sp_mode','{mode}')}}catch(e){{}}")
            await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
            await pg.click('[data-act="localSetup"]'); await pg.select_option('#lpN','3'); await pg.select_option('#lpLv','normal'); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'mob_{mode}.png')
            await pg.evaluate("window.scrollTo(0,9999)"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f'mob_{mode}_bottom.png')
            print(mode,errs); await ctx.close()
        pg=await b.new_page(viewport={'width':1366,'height':768})
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
        await pg.click('[data-act="localSetup"]'); await pg.select_option('#lpN','3'); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='desk.png'); await b.close()
asyncio.run(main())
