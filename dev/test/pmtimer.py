import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="pmlocal"]'); await pg.wait_for_timeout(200); await pg.select_option('#pmTmr','30'); await pg.click('[data-act="pmlocalgo"]')
        for k in range(200):
            st=json.loads(await pg.evaluate("JSON.stringify({ph:cur.st.phase,t:cur.st.turn,h:cur.human})"))
            if st['t']==st['h']:
                await pg.evaluate("cur.st.turnAt=Date.now()-31000"); await pg.wait_for_timeout(1500)
                print('after timeout',st['ph'],'->',await pg.evaluate("JSON.stringify({ph:cur.st.phase,t:cur.st.turn,h:cur.human,setup:cur.st.setup})"))
                if st['ph']=='roll':break
            await pg.wait_for_timeout(300)
        print('errors',errs); await b.close()
asyncio.run(main())
