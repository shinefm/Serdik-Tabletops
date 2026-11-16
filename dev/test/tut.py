import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,tag in [((1200,850),'d'),((390,844),'m')]:
            pg=await b.new_page(viewport={'width':vw[0],'height':vw[1]}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
            await pg.goto('file:///home/claude/pub/index.html'); await pg.wait_for_timeout(1200)
            await pg.click('[data-act="tutorial"]'); await pg.wait_for_timeout(1500)
            d1=await pg.evaluate("(()=>{const v=document.querySelector('.tutv video');return v&&{dur:v.duration,rs:v.readyState,src:v.currentSrc.split('/').pop()}})()")
            await pg.click('.tabs [data-w="duel"]'); await pg.wait_for_timeout(1500)
            d2=await pg.evaluate("(()=>{const v=document.querySelector('.tutv video');return v&&{dur:v.duration,rs:v.readyState,src:v.currentSrc.split('/').pop()}})()")
            el=await pg.query_selector('.mbox'); await el.screenshot(path=f'tut_{tag}.png')
            print(tag,d1,d2,errs); await pg.close()
        await b.close()
asyncio.run(main())
