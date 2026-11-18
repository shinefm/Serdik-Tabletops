import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,tag,dsf in [({'width':390,'height':844},'m',2),({'width':1300,'height':900},'d',1)]:
            pg=await b.new_page(viewport=vw,device_scale_factor=dsf); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
            await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
            await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
            await pg.evaluate("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await pg.evaluate("closeModal()")
            await pg.evaluate("(()=>{const p=cur.st.players[cur.human];p.t={w:3,u:3,g:2,r:2,k:0,y:0};render();})()"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'sq_{tag}.png',full_page=(tag=='m')); print(tag,errs)
        await b.close()
asyncio.run(main())
