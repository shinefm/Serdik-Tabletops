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
        await pg.select_option('#lpLv','hard'); await ev("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        await pg.click('.brand'); await pg.wait_for_timeout(700)
        print('leave dialog:',(await ev("$('#modal').innerText")).replace('\n',' ')[:120])
        await pg.click('#modal [data-act="restartlocalok"]'); await pg.wait_for_timeout(1300); await ev("closeModal()")
        print('new game from leave dialog:',await ev("[cur.st.mode,cur.level]"))
        await ev("(()=>{cur.st.turn=cur.human;attemptMove({type:'pass'});})()"); await pg.wait_for_timeout(800)
        await pg.click('.brand'); await pg.wait_for_timeout(700)
        print('2nd dialog',(await ev("($('#modal')||{}).innerText||''")).replace('\n',' ')[:80],'active',await ev("localGameActive()"),'view',await ev("view"))
        await pg.click('#modal [data-act="savequit"]'); await pg.wait_for_timeout(1500)
        sv=await ev("ui.saveMeta&&ui.saveMeta.variant"); print('saved variant',sv)
        html=await ev("ui.saveMeta?saveCardHTML(ui.saveMeta,'history'):'(none) active='+localGameActive()")
        import re; print('save card:',re.sub('<[^>]+>',' ',html)[:160])
        print('errs',errs); await b.close()
asyncio.run(main())
