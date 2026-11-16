import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1280,'height':860}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js'); await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("""()=>{__store['games/tord']={name:'Meja Urut',host:'u_b',createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',timer:180,players:[newPlayer('u_b','Dina'),newPlayer('u_me','Farhan'),newPlayer('u_c','Raka')],v:1};}""")
        await pg.evaluate("openTable('tord')"); await pg.wait_for_timeout(500)
        await pg.evaluate("""(async()=>{const st=__store['games/tord'];startGame(st);st.v++;await db.doc('games/tord').set(st);})()"""); await pg.wait_for_timeout(800)
        print('online pop:',(await pg.evaluate("(document.getElementById('rankpop')||{}).innerText||'NONE'")).replace('\n',' / '),'| chip',await pg.inner_text('.rankchip'),errs)
        await b.close()
asyncio.run(main())
