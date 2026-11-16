import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("c0delay=()=>30")
        await pg.tap('[data-act="localSetup"]'); await pg.select_option('#lpN','2'); await pg.tap('[data-act="localStart"]'); await pg.wait_for_timeout(400)
        for c in ['w','u','g']: await pg.tap(f'.m-gem[data-c="{c}"]')
        await pg.tap('[data-act="take"]'); await pg.wait_for_timeout(600)
        await pg.tap('.m-field [data-act="card"]'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='mob_modal.png'); await pg.tap('[data-act="doreserve"]'); await pg.wait_for_timeout(700)
        await pg.evaluate("window.scrollTo(0,500)"); await pg.wait_for_timeout(200)
        await pg.screenshot(path='mob_after.png')
        print('log',await pg.evaluate("cur.st.log.slice(-5).map(l=>l.m).join(' | ')"),'errs',errs)
        pg2=await b.new_page(viewport={'width':1366,'height':768})
        await pg2.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg2.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg2.wait_for_timeout(1200)
        await pg2.click('[data-act="localSetup"]'); await pg2.select_option('#lpN','3'); await pg2.click('[data-act="localStart"]'); await pg2.wait_for_timeout(400)
        await pg2.screenshot(path='desk.png'); await b.close()
asyncio.run(main())
