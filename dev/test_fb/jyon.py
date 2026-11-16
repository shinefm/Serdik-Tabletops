import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="hubnew"][data-g="jualan"]'); await pg.wait_for_timeout(900)
        print('view',await pg.evaluate("JSON.stringify({v:view,g:cur.st&&cur.st.game,nt:cur.st&&cur.st.nteams})"))
        await pg.select_option('#jyNt','3'); await pg.wait_for_timeout(500)
        await pg.select_option('#jySp','1'); await pg.wait_for_timeout(500)
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push({id:'u_dina',nick:'Dina',team:0},{id:'u_budi',nick:'Budi',team:1});s.v++;await r.set(s);}""")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path='jyon_wait.png',full_page=True)
        await pg.click('[data-act="jyjoin"][data-t="1"]'); await pg.wait_for_timeout(500)
        await pg.click('[data-act="jyjoin"][data-t="0"]'); await pg.wait_for_timeout(500)
        print('cfg',await pg.evaluate("JSON.stringify({nt:cur.st.nteams,sp:cur.st.split,pl:cur.st.players.map(p=>[p.id,p.team])})"))
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200)
        print('teams',await pg.evaluate("JSON.stringify(cur.st.teams.map(T=>({m:T.members,bot:T.bot,roles:T.roles})))"), await pg.evaluate("JSON.stringify(cur.st.players.map(p=>[p.id,p.team]))"))
        # split: aku pegang fin/op/sl; coba ubah bagian orang lain -> harus ditolak, bagianku -> tersimpan via debounce
        await pg.evaluate("ui.jyOpen={hr:1,op:1,mk:1,sl:1};render()")
        await pg.click('[data-act="jyinc"][data-d="1"]:not([disabled])'); await pg.wait_for_timeout(1200)
        print('draft synced',await pg.evaluate("JSON.stringify([cur.st.teams[0].draft.H,Object.keys(ui.jy.d)])"),'hr btn disabled',await pg.evaluate("document.querySelector('[data-k=h2][data-d=\"1\"]').disabled"))
        await pg.screenshot(path='jyon_plan.png',full_page=True)
        ids=json.loads(await pg.evaluate("JSON.stringify(cur.st.players.map(p=>p.id))"))
        async def actAs(uid,js):
            return await pg.evaluate(f"(async()=>{{myId='{uid}';try{{return await ({js});}}catch(e){{return 'ERR '+e.message}}finally{{myId='u_me';render();}}}})()")
        shot=False
        for i in range(600):
            st=json.loads(await pg.evaluate("JSON.stringify({s:cur.st.status,w:jyWaiting(cur.st),ph:cur.st.phase,r:cur.st.round})"))
            if st['s']!='playing':break
            await pg.evaluate("if(modalOpen())closeModal()")
            done=False
            for w in st['w']:
                t=w['t']
                if await pg.evaluate(f"cur.st.teams[{t}].bot"): continue
                if w['div']=='plan':
                    fin=await pg.evaluate(f"cur.st.split?cur.st.teams[{t}].roles.fin:cur.st.teams[{t}].members[0]")
                    uid=ids[fin]
                    r=await actAs(uid,f"commitOnline(s=>{{s.teams[{t}].draft=jyBotPlan(s,{t});jyAct(s,meIdx(s),{{type:'ready'}});}})")
                else:
                    sl=await pg.evaluate(f"cur.st.teams[{t}].roles.sl")
                    if sl is None: break
                    uid=ids[sl]
                    if uid=='u_me' and not shot:
                        await pg.screenshot(path='jyon_sell.png',full_page=True); shot=True
                    r=await actAs(uid,f"commitOnline(s=>{{jyAct(s,meIdx(s),jyBotSell(s,{t}));}})")
                if r and str(r).startswith('ERR'):print('err',uid,w,r)
                done=True;break
            await pg.wait_for_timeout(300 if done else 900)
        await pg.wait_for_timeout(1500)
        print('end',await pg.evaluate("JSON.stringify({s:cur.st.status,r:cur.st.round,cash:cur.st.teams.map(T=>T.cash),w:cur.st.winner})"))
        await pg.screenshot(path='jyon_end.png')
        print('errs',errs); await b.close()
asyncio.run(main())
