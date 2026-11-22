import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300); await pg.click('[data-act="lpmode"][data-m="duel"]')
        await pg.select_option('#lpLv','hard'); await ev("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        print('start',await ev("[cur.st.mode,cur.level,cur.st.players.length]"))
        await pg.click('.brand'); await pg.wait_for_timeout(700)
        print('leave dialog:',(await ev("($('#modal')||{}).innerText||''")).replace('\n',' ')[:110])
        if await ev("!!document.querySelector('#modal [data-act=\"restartlocalok\"]')"):
            await pg.click('#modal [data-act="restartlocalok"]'); await pg.wait_for_timeout(1300); await ev("closeModal()")
        print('after new game (leave)',await ev("[cur.st.mode,cur.level,cur.st.players.length]"))
        await ev("restartLocal()"); await pg.wait_for_timeout(300)
        print('restart label:',(await ev("$('#modal').innerText")).replace('\n',' ')[:140])
        await pg.click('#modal [data-act="restartlocalok"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        print('after restart',await ev("[cur.st.mode,cur.level,cur.st.players.length]"))
        await ev("(()=>{clearTimeout(cur.botTimer);cur.botTimer=1;const st=cur.st;st.status='ended';onGameEnded(st);cur.botTimer=null;render();})()"); await pg.wait_for_timeout(1500)
        print('end modal btns:',await ev("[...document.querySelectorAll('#modal button')].map(b=>b.dataset.act)"))
        if await ev("!!document.querySelector('#modal [data-act=\"restartlocalok\"]')"):
            await pg.click('#modal [data-act="restartlocalok"]'); await pg.wait_for_timeout(1300); await ev("closeModal()")
            print('after new game (end)',await ev("[cur.st.mode,cur.level,cur.st.players.length,cur.st.status]"))
        print('errs',errs); await b.close()
asyncio.run(main())
