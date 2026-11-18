import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        await pg.click('.brand'); await pg.wait_for_timeout(300); print('lobby click view',await ev("view"))
        await pg.click('#createBtn'); await pg.wait_for_timeout(800); print('at table',await ev("view"),await ev("location.hash"))
        await pg.click('.brand'); await pg.wait_for_timeout(1000); print('after brand (online)',await ev("view"),await ev("location.hash"))
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1500); await ev("closeModal()")
        print('local game',await ev("view"),await ev("cur.st.status"))
        await pg.click('.brand'); await pg.wait_for_timeout(600)
        print('confirm modal:',(await ev("$('#modal').innerText")).split('\n')[0])
        btns=await ev("[...document.querySelectorAll('#modal button')].map(b=>b.textContent.trim()+'|'+b.dataset.act)"); print(btns)
        await pg.click('#modal [data-act="close"]') if 'close' in str(btns) else None
        print('still table',await ev("view"),'errs',errs)
        await b.close()
asyncio.run(main())
