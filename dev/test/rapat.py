import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':950})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='r_lobby.png',full_page=True)
        await pg.click('[data-act="hubnew"][data-g="rapat"]'); await pg.wait_for_timeout(600)
        gid=await pg.evaluate("cur.gid"); print('gid',gid, await pg.evaluate("JSON.stringify({g:cur.st.game,t:cur.st.timer,sp:cur.st.special})"))
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();['Dina','Raka','Sari','Bima','Tono','Ayu'].forEach((n,i)=>s.players.push({id:'u_'+n.toLowerCase(),nick:n}));s.v++;await r.set(s);}""")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='r_wait.png',full_page=True)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='r_role.png')
        print('modal:',(await pg.inner_text('#mbox'))[:300].replace('\n',' / '))
        await pg.click('#mbox [data-act="close"]'); await pg.wait_for_timeout(300)
        # make me the leader for UI test
        info=json.loads(await pg.evaluate("JSON.stringify({leader:cur.st.leader,me:meIdx(cur.st),ids:cur.st.players.map(p=>p.id),roles:rapatRoles(cur.st)})")); print(info)
        async def as_(uid,js):
            return await pg.evaluate(f"(async()=>{{myId='{uid}';try{{return await ({js});}}finally{{myId='u_me';render();}}}})()")
        lead=info['ids'][info['leader']]
        await pg.screenshot(path='r_propose_other.png')
        # leader propose via UI as leader
        await pg.evaluate(f"myId='{lead}';render()")
        size=await pg.evaluate("cur.st.missions[0].size")
        for i in range(size): await pg.click(f'.rpchip.pick[data-i="{i}"]'); await pg.wait_for_timeout(80)
        await pg.screenshot(path='r_propose_lead.png')
        await pg.click('[data-act="rpropose"]'); await pg.wait_for_timeout(500)
        await pg.evaluate("myId='u_me';render()"); await pg.wait_for_timeout(200)
        await pg.screenshot(path='r_vote.png')
        await pg.click('[data-act="rvote"][data-y="1"]'); await pg.wait_for_timeout(400)
        for uid in info['ids']:
            if uid=='u_me':continue
            await as_(uid,"hubMove({type:'vote',yes:true})"); await pg.wait_for_timeout(150)
        await pg.wait_for_timeout(300)
        print('phase',await pg.evaluate("cur.st.phase"), await pg.evaluate("cur.st.team"))
        await pg.screenshot(path='r_mission.png')
        roles=info['roles']; team=await pg.evaluate("cur.st.team")
        for t in team:
            uid=info['ids'][t]; card='f' if roles[t] in 'OD' else 's'
            await as_(uid,f"hubMove({{type:'play',card:'{card}'}})"); await pg.wait_for_timeout(150)
        await pg.wait_for_timeout(500)
        await pg.screenshot(path='r_after1.png')
        print('res',await pg.evaluate("cur.st.res"), 'phase', await pg.evaluate("cur.st.phase"))
        # play rest programmatically: Integritas team picks only I's -> success, so reach shoot
        for k in range(12):
            st=json.loads(await pg.evaluate("JSON.stringify({ph:cur.st.phase,st:cur.st.status,l:cur.st.leader,mi:cur.st.mi})"))
            if st['st']!='playing':break
            if st['ph']=='propose':
                size=await pg.evaluate("cur.st.missions[cur.st.mi].size")
                good=[i for i,r in enumerate(roles) if r in 'IA'][:size]
                await as_(info['ids'][st['l']],f"hubMove({{type:'propose',team:{good}}})")
            elif st['ph']=='vote':
                for uid in info['ids']: await as_(uid,"hubMove({type:'vote',yes:true})"); await pg.wait_for_timeout(60)
            elif st['ph']=='mission':
                for t in await pg.evaluate("cur.st.team"): await as_(info['ids'][t],"hubMove({type:'play',card:'s'})"); await pg.wait_for_timeout(60)
            elif st['ph']=='shoot':
                d=roles.index('D'); await pg.evaluate(f"myId='{info['ids'][d]}';render()"); await pg.wait_for_timeout(200)
                await pg.screenshot(path='r_shoot.png')
                tg=[i for i,r in enumerate(roles) if r=='I'][0]
                await pg.click(f'.rpchip[data-i="{tg}"]'); await pg.click('[data-act="rshootok"]'); await pg.wait_for_timeout(200); await pg.click('[data-act="rshootgo"]')
                await pg.wait_for_timeout(500); await pg.evaluate("myId='u_me';render()")
            await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(1500)
        print('status',await pg.evaluate("cur.st.status"),await pg.evaluate("cur.st.winBy"))
        await pg.screenshot(path='r_end.png')
        print('endmodal:',(await pg.inner_text('#mbox'))[:400].replace('\n',' / ') if await pg.evaluate("document.getElementById('modal').classList.contains('open')") else 'NONE')
        await pg.wait_for_timeout(800)
        r=await pg.evaluate(f"JSON.stringify(__store['results/g_{gid}'])"); r=json.loads(r) if r else None
        print('result', r and {k:r[k] for k in ['variant','mode','rounds','winner','winBy']}, r and [(x['nick'],x['rank'],x['role']) for x in r['players']])
        print('stats me', await pg.evaluate("JSON.stringify(__store['stats/u_me']&&__store['stats/u_me'].rec)"))
        await pg.click('#mbox [data-act="close"]')
        await pg.evaluate("openHistory()"); await pg.wait_for_timeout(700)
        await pg.screenshot(path='r_hist.png')
        await pg.click('.hrow'); await pg.wait_for_timeout(300); await pg.screenshot(path='r_hdet.png')
        await pg.evaluate("openProfile()"); await pg.wait_for_timeout(700); await pg.screenshot(path='r_prof.png')
        print('errors',errs); await b.close()
asyncio.run(main())
