import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="hubnew"][data-g="pemukim"]'); await pg.wait_for_timeout(600)
        await pg.click('[data-act="addbot"]'); await pg.wait_for_timeout(400)
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push({id:'u_dina',nick:'Dina'});s.v++;await r.set(s);}""")
        await pg.wait_for_timeout(500); await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1000)
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();const d=s.players.findIndex(p=>p.id==='u_dina');s.players[d].auto=true;s.v++;await r.set(s);}""")
        for i in range(40):
            await pg.wait_for_timeout(1000)
            st=json.loads(await pg.evaluate("JSON.stringify({t:cur.st.turn,ph:cur.st.phase,me:meIdx(cur.st),r:cur.st.round})"))
            if st['t']==st['me']:break
        print("reached my turn",st, await pg.evaluate("JSON.stringify({d:cur.st.players.findIndex(p=>p.id===\"u_dina\"),log:(cur.st.log||[]).slice(-6)})"))
        print('botnext for auto:',await pg.evaluate("(()=>{const s=clone(cur.st);const d=s.players.findIndex(p=>p.id==='u_dina');s.turn=d;const x=pmBotNext(s);s.players[d].auto=false;return JSON.stringify([d,x&&x.j,pmBotNext(s)])})()"))
        print('bar',await pg.evaluate("($('#afkBar')||{}).textContent"))
        print('errs',errs); await b.close()
asyncio.run(main())
