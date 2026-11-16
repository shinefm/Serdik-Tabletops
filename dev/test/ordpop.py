import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,o,tag in [({'width':1280,'height':860},'2','d'),({'width':390,'height':844},'0','m')]:
            pg=await b.new_page(viewport=vw); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js'); await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
            await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(250); await pg.select_option('#lpN','3'); await pg.wait_for_timeout(100)
            await pg.evaluate(f"document.querySelector('#lpOrd').value='{o}'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(500)
            t=await pg.evaluate("document.getElementById('rankpop').innerText"); chip=await pg.inner_text('.rankchip')
            await pg.screenshot(path=f'ord_{tag}.png')
            # no pop on later renders / score changes
            await pg.wait_for_timeout(5500); await pg.evaluate("(()=>{cur.st.players[1].cards=['3r1'];render();})()"); await pg.wait_for_timeout(400)
            again=await pg.evaluate("document.getElementById('rankpop').classList.contains('show')")
            print(tag,'pop:',t.replace('\n',' / '),'| chip:',chip,'| re-pop on score change:',again,errs)
        await b.close()
asyncio.run(main())
