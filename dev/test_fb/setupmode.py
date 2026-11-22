import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context(viewport={'width':390,'height':844}); pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js'); await pg.goto(U); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        for mode in ['duel','kota']:
            await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300); await pg.click(f'[data-act="lpmode"][data-m="{mode}"]')
            await pg.select_option('#lpLv','hard'); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
            ui0=await ev("[cur.st.mode,cur.level]")
            await ev("(()=>{cur.st.turn=cur.human;attemptMove({type:'pass'});})()"); await pg.wait_for_timeout(600)
            await pg.click('.brand'); await pg.wait_for_timeout(600); await pg.click('#modal [data-act="savequit"]'); await pg.wait_for_timeout(1200)
            # refresh halaman: pengaturan terakhir harus tetap diingat
            await pg.reload(); await pg.wait_for_timeout(1800)
            await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
            print(mode,'played',ui0,'| after reload setup opens:',await ev("[ui.lpMode,$('#lpLv').value]"))
            await ev("closeModal()")
            # lanjutkan game tersimpan lalu Ganti bot/level
            await ev("resumeSaved()"); await pg.wait_for_timeout(1500); await ev("closeModal()")
            await ev("ui.lastLocal=null"); await ev("localSetup()"); await pg.wait_for_timeout(300)
            print(mode,'resumed',await ev("[cur.st.mode,cur.level]"),'| Ganti bot/level opens:',await ev("[ui.lpMode,$('#lpLv').value]"))
            await ev("closeModal()"); await pg.click('.brand'); await pg.wait_for_timeout(600)
            if await ev("!!document.querySelector('#modal [data-act=\"nosavequit\"]')"): await pg.click('#modal [data-act="nosavequit"]'); await pg.wait_for_timeout(800)
        print('errs',errs); await b.close()
asyncio.run(main())
