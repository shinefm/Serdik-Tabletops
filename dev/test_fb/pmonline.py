import asyncio,json,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="hubnew"][data-g="pemukim"]'); await pg.wait_for_timeout(600)
        print('created',await pg.evaluate("JSON.stringify({g:cur.st.game,t:cur.st.timer})"))
        await pg.click('[data-act="addbot"]'); await pg.wait_for_timeout(400)
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push({id:'u_dina',nick:'Dina'});s.v++;await r.set(s);}""")
        await pg.wait_for_timeout(500); await pg.screenshot(path='pmo_wait.png',full_page=True)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1000)
        ids=json.loads(await pg.evaluate("JSON.stringify(cur.st.players.map(p=>p.id))")); print(ids)
        async def as_(uid,js):
            return await pg.evaluate(f"(async()=>{{myId='{uid}';try{{return await ({js});}}finally{{myId='u_me';render();}}}})()")
        shot=False
        for k in range(1500):
            st=json.loads(await pg.evaluate("JSON.stringify({s:cur.st.status,ph:cur.st.phase,t:cur.st.turn,pend:pmPending(cur.st),offer:cur.st.offer,r:cur.st.round})"))
            if st['s']!='playing':break
            pend=[ids[j] for j in st['pend']]
            acted=False
            for uid in pend:
                if uid.startswith('bot_'):continue
                j=ids.index(uid)
                mvjs=f"(cur.st.phase==='discard'?pmBotDiscard(cur.st,{j}):pmBotMove(cur.st,{j},'normal'))"
                if uid=='u_me': await pg.evaluate(f"pmMove({mvjs})")
                else: await as_(uid,f"pmMove({mvjs})")
                acted=True; break
            if st['r']==4 and not shot:
                await pg.screenshot(path='pmo_mid.png',full_page=True); shot=True
            await pg.wait_for_timeout(150 if acted else 400)
        await pg.wait_for_timeout(2000)
        print('status',await pg.evaluate("JSON.stringify({s:cur.st.status,w:cur.st.winner,r:cur.st.round})"))
        await pg.screenshot(path='pmo_end.png')
        gid=await pg.evaluate("cur.gid")
        r=json.loads(await pg.evaluate(f"JSON.stringify(__store['results/g_{gid}']||null)"))
        print('result',r and {k:r[k] for k in ['variant','mode','rounds']}, r and [(x['nick'],x['rank'],x['pts'],x['bot']) for x in r['players']])
        print('stats me',await pg.evaluate("JSON.stringify(__store['stats/u_me']&&__store['stats/u_me'].rec.online.pemukim)"),'dina',await pg.evaluate("JSON.stringify(__store['stats/u_dina']&&__store['stats/u_dina'].rec.online.pemukim)"))
        print('errors',errs); await b.close()
asyncio.run(main())
