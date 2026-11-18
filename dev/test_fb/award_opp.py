import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js'); await pg.goto(U); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        # 1) bot lokal dapat pahlawan
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
        await ev("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        await ev("""(()=>{const st=cur.st,p=st.players[1],id=st.patrons[0],nd=PAT[id].need;for(const c in nd){const ids=TIER_IDS[1].filter(x=>CARDS[x].b===c);for(let k=0;k<nd[c];k++)p.cards.push(ids[k%ids.length]);}render();})()""")
        await ev("attemptMove({type:'pass'})")
        seen=None
        for k in range(40):
            await pg.wait_for_timeout(250)
            t=await ev("(document.querySelector('.awov')||{}).innerText||''")
            if t: seen=t; break
        print('bot award overlay:',repr(seen))
        await pg.screenshot(path='award_bot.png')
        # 2) lawan online merebut kota
        await pg.wait_for_timeout(3500)
        await pg.click('.brand'); await pg.wait_for_timeout(800)
        if await ev("!!document.querySelector('#modal [data-act=\"nosavequit\"]')"): await pg.click('#modal [data-act="nosavequit"]'); await pg.wait_for_timeout(800)
        await pg.select_option('#modeIn','kota'); await pg.click('#createBtn'); await pg.wait_for_timeout(800)
        await ev("""(async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push(newPlayer('u_dina','Dina'));s.v++;await r.set(s);})()"""); await pg.wait_for_timeout(500)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        await ev("""(async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();const i=s.players.findIndex(p=>p.id==='u_dina');const p=s.players[i];const id=s.cities[0];
            p.kota=id;s.kotaBy[id]=i;s.endTriggered=true;s.v++;await r.set(s);})()""")
        await pg.wait_for_timeout(900)
        print('online opp overlay:',repr(await ev("(document.querySelector('.awov')||{}).innerText||''")))
        await pg.screenshot(path='award_opp.png')
        print('errs',errs); await b.close()
asyncio.run(main())
