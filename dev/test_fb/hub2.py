import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w,h,n in [(1300,900,'d'),(390,844,'m')]:
            ctx=await b.new_context(viewport={'width':w,'height':h}); pg=await ctx.new_page(); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
            await pg.goto(U); await pg.wait_for_timeout(2500)
            await pg.evaluate("closeModal&&closeModal()")
            print(n,'mode',await pg.evaluate("ui.mode"),'light',await pg.evaluate("document.body.classList.contains('light')"),'title',await pg.title(),'h1',await pg.evaluate("document.querySelector('.brand h1').textContent"),'errs',errs)
            await pg.screenshot(path=f'hub2_{n}.png',full_page=True)
        await b.close()
asyncio.run(main())
