import asyncio
from playwright.async_api import async_playwright
async def shot(p,name,mock=None,ua=None):
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,user_agent=ua) if ua else await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
    pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    if mock: await pg.add_init_script(path=mock)
    await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html#meja-abc'); await pg.wait_for_timeout(3000)
    await pg.screenshot(path=name); print(name,errs); await b.close()
async def main():
    async with async_playwright() as p:
        await shot(p,'gate_off.png')
        await shot(p,'gate_wa.png',ua='Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36 WhatsApp/2.23')
        await shot(p,'gate_guest.png',mock='/home/claude/serdik-tabletops/dev/test/mock_guest.js')
        await shot(p,'gate_ok.png',mock='/home/claude/serdik-tabletops/dev/test/mock.js')
asyncio.run(main())
