import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':950}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        # permata local vs 3 bots, me 3rd
        await pg.evaluate("openLocalSetup&&openLocalSetup()") if await pg.evaluate("typeof openLocalSetup==='function'") else await pg.click('[data-act="localSetup"]')
        await pg.wait_for_timeout(300)
        sel=await pg.query_selector_all('#mbox select'); print('selects',len(sel))
        html=await pg.inner_html('#mbox'); 
        import re; print(re.findall(r'id="(\w+)"',html)[:10])
        await pg.screenshot(path='me_setup.png')
        await pg.evaluate("""(()=>{const o=document.querySelector('#obOrd,#lsOrd,#ordSel');if(o){o.value='2';}})()""")
        btn=await pg.query_selector('#mbox .btn.pri'); await btn.click(); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='me_permata.png')
        print('human seat',await pg.evaluate("cur.human"),'first panel',await pg.evaluate("(()=>{const els=[...document.querySelectorAll('.players .pl')];const vis=els.map(e=>[e.getBoundingClientRect().top,e.querySelector('.n').textContent]).sort((a,b)=>a[0]-b[0]);return vis.map(v=>v[1]).join(' | ');})()"))
        print(errs); await b.close()
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(3000)
        await pg.screenshot(path='me_loginpop.png'); await b.close()
asyncio.run(main())
