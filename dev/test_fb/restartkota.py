import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300); await pg.click('[data-act="lpmode"][data-m="kota"]')
        await pg.select_option('#lpLv','hard'); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        print('start',await ev("[cur.st.mode,cur.level,cur.st.players.length]"))
        # akhiri game paksa, lalu Main game baru dari layar akhir
        await ev("(()=>{const st=cur.st,p=st.players[cur.human];p.kota=st.cities[0];st.kotaBy[st.cities[0]]=cur.human;st.status='ended';onGameEnded(st);render();})()"); await pg.wait_for_timeout(1500)
        btn=await ev("!!document.querySelector('#modal [data-act=\"restartlocalok\"]')"); print('end modal has new game btn',btn)
        await pg.click('#modal [data-act="restartlocalok"]'); await pg.wait_for_timeout(1500); await ev("closeModal()")
        print('after new game',await ev("[cur.st.mode,cur.level,cur.st.players.length,cur.st.cities&&cur.st.cities.length,cur.st.status]"))
        # ulang dari tengah game
        await ev("restartLocal()"); await pg.wait_for_timeout(300)
        print('restart label',(await ev("$('#modal').innerText")).replace('\n',' | ')[:160])
        await pg.click('#modal [data-act="restartlocalok"]'); await pg.wait_for_timeout(1200)
        print('after restart',await ev("[cur.st.mode,cur.level]"),'errs',errs); await b.close()
asyncio.run(main())
