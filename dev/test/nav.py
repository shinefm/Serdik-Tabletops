import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        S=lambda: pg.evaluate("JSON.stringify({v:view,m:modalOpen(),h:location.hash,st:history.state,len:history.length,url:location.href.slice(-30)})")
        back=lambda: pg.evaluate("history.back()")
        print('start',await S())
        await pg.click('#profBtn'); await pg.wait_for_timeout(400); print('profile',await S())
        await back(); await pg.wait_for_timeout(500); print('back1',await S())
        # online table
        await pg.click('#createBtn'); await pg.wait_for_timeout(800); print('table',await S())
        await back(); await pg.wait_for_timeout(600); print('back2',await S())
        # open again then leave via UI
        await pg.click('#gateSlot [data-act="open"]'); await pg.wait_for_timeout(800); print('reopen',await S())
        await pg.click('#backBtn'); await pg.wait_for_timeout(800); print('ui-leave',await S())
        # local bot game
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300); await pg.click('#mbox .btn.pri'); await pg.wait_for_timeout(3000)
        print('local',await S())
        await back(); await pg.wait_for_timeout(600); print('back3 (leave modal?)',await S(), await pg.evaluate("$('#mbox h3')&&$('#mbox h3').textContent"))
        await back(); await pg.wait_for_timeout(600); print('back4 (modal closed, still table)',await S())
        await back(); await pg.wait_for_timeout(600); print('back5',await S())
        await pg.click('[data-act="nosavequit"]'); await pg.wait_for_timeout(800); print('quit',await S())
        print('errs',errs); await b.close()
asyncio.run(main())
