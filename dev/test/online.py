import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate("""()=>{const st={name:'Meja Uji',host:'u_b',createdAt:Date.now(),status:'lobby',players:[newPlayer('u_b','Dina'),newPlayer('u_c','Raka'),newPlayer('u_me','Farhan')],v:1};
          startGame(st); st.players[2].cards=['3r1','3k1','3u1','2g4']; st.players[0].cards=['3w1','2g4']; st.endTriggered=true; st.turn=2; st.round=19;
          __store['games/tuji']=st;}""")
        await pg.evaluate("openTable('tuji')"); await pg.wait_for_timeout(500)
        await pg.evaluate("(async()=>{await runMove({type:'pass'});})()"); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("JSON.stringify(__store['results/g_tuji']&&{mode:__store['results/g_tuji'].mode,award:__store['results/g_tuji'].award,week:__store['results/g_tuji'].week,ids:__store['results/g_tuji'].ids})")
        print(r)
        await pg.screenshot(path='online_end.png',clip={'x':0,'y':80,'width':1300,'height':230})
        await pg.wait_for_timeout(900); print('online popup:',(await pg.inner_text('#mbox'))[:160].replace('\n',' / ') if await pg.evaluate("document.getElementById('modal').classList.contains('open')") else 'NONE')
        print('errors',errs); await b.close()
asyncio.run(main())
