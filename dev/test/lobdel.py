import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.click('#createBtn'); await pg.wait_for_timeout(800)
        await pg.evaluate("db.doc('games/tother').set({name:'Meja Lain',status:'lobby',host:'u_x',players:[{id:'u_x',nick:'X'}],createdAt:Date.now(),updatedAt:Date.now(),v:1,mode:'klasik'})")
        await pg.evaluate("backToLobby()"); await pg.wait_for_timeout(800)
        print('del buttons',await pg.evaluate("[...document.querySelectorAll('[data-act=lobdel]')].map(e=>e.dataset.n).join('|')"))
        await pg.screenshot(path='lobdel.png')
        await pg.click('#gateSlot [data-act="lobdel"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-act="lobdelok"]'); await pg.wait_for_timeout(800)
        print('games left',await pg.evaluate("lobbyGames.map(g=>g.name).join('|')"),'view',await pg.evaluate("view"),errs)
        await b.close()
asyncio.run(main())
