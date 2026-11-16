import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        # Permata
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300); await pg.select_option('#lpLv','hard'); await pg.click('#mbox .btn.pri'); await pg.wait_for_timeout(4000)
        a=await pg.evaluate("JSON.stringify({lid:cur.lid,lv:cur.level,names:cur.st.players.map(p=>p.nick),log:cur.st.log.length})")
        await pg.click('header [data-act="lobby"]'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='restart_modal.png')
        await pg.click('#mbox [data-act="restartlocalok"]'); await pg.wait_for_timeout(800)
        bb=await pg.evaluate("JSON.stringify({lid:cur.lid,lv:cur.level,names:cur.st.players.map(p=>p.nick),log:cur.st.log.length,view})")
        print('permata before',a); print('permata after',bb)
        # Pemukim
        await pg.evaluate("backToLobby()"); await pg.wait_for_timeout(500)
        await pg.click('[data-act="pmlocal"]'); await pg.wait_for_timeout(200); await pg.click('[data-act="pmlocalgo"]'); await pg.wait_for_timeout(2500)
        a=await pg.evaluate("JSON.stringify({g:cur.st.game,lid:cur.lid,names:cur.st.players.map(p=>p.nick)})")
        await pg.evaluate("leaveTable()"); await pg.wait_for_timeout(400)
        btn=await pg.query_selector('#mbox [data-act="restartlocalok"]')
        if btn: await btn.click()
        await pg.wait_for_timeout(800)
        bb=await pg.evaluate("JSON.stringify({g:cur.st.game,lid:cur.lid,names:cur.st.players.map(p=>p.nick),phase:cur.st.phase})")
        print('pemukim before',a); print('pemukim after',bb, 'had button',bool(btn))
        print('errors',errs); await b.close()
asyncio.run(main())
