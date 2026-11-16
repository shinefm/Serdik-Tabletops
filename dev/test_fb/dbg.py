import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844})
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(2000)
        await pg.click('#createBtn'); await pg.wait_for_timeout(1500)
        await pg.evaluate("window.__rc=0;const r=render;render=function(){window.__rc++;if(window.__rc<4)console.log(new Error().stack.split('\\n').slice(1,6).join('|'));return r.apply(this,arguments)};window.__o=JSON.stringify(__FSOPS)")
        msgs=[]; pg.on('console',lambda m: msgs.append(m.text))
        await pg.wait_for_timeout(2000)
        print('renders in 2s',await pg.evaluate("__rc"),await pg.evaluate("__o"),await pg.evaluate("JSON.stringify(__FSOPS)"))
        for m in msgs[:3]: print(m[:600])
        await b.close()
asyncio.run(main())
