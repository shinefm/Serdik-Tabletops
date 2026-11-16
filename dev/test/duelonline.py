import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1200,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
        await pg.fill('#tblIn','Duel Serdik'); await pg.select_option('#modeIn','duel'); await pg.click('[data-act="create"]'); await pg.wait_for_timeout(600)
        seats=await pg.evaluate("document.querySelectorAll('.seat').length")
        wa=await pg.get_attribute('a.wa','href')
        # simulate opponent joining
        await pg.evaluate("(async()=>{const ref=db.doc('games/'+cur.gid);const s=(await ref.get()).data();s.players.push(newPlayer('u_b','Dina'));s.v++;await ref.set(s);})()"); await pg.wait_for_timeout(500)
        await pg.screenshot(path='duel_wait.png',clip={'x':0,'y':0,'width':1200,'height':560})
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(700)
        st=await pg.evaluate("({mode:cur.st.mode,status:cur.st.status,board:cur.st.board.filter(x=>x).length,me:meIdx(cur.st),turn:cur.st.turn})")
        cells=await pg.evaluate("(()=>{for(const L of DLINES){if(L.length===2&&L.every(i=>cur.st.board[i]&&cur.st.board[i]!=='y'))return L;}})()")
        for c in cells: await pg.click(f'.dcell[data-i="{c}"]')
        await pg.click('[data-act="dtake"]'); await pg.wait_for_timeout(700)
        after=await pg.evaluate("({turn:cur.st.turn,log:cur.st.log.slice(-1)[0].m})")
        print('seats',seats,'duel in wa text','Duel' in wa,st,after,errs); await b.close()
asyncio.run(main())
