import asyncio,json,sys,random
from playwright.async_api import async_playwright
W=int(sys.argv[1]) if len(sys.argv)>1 else 1300
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':W,'height':950 if W>500 else 844},device_scale_factor=1 if W>500 else 2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'wk{W}_lobby.png',full_page=True)
        await pg.click('[data-act="hubnew"][data-g="wwk"]'); await pg.wait_for_timeout(600)
        print('created',await pg.evaluate("JSON.stringify({g:cur.st.game,t:cur.st.timer})"))
        names=['Dina','Raka','Sari','Bima','Tono','Ayu','Rudi','Lia','Fajar','Nina','Yoga','Mega','Hadi','Putri','Eka','Joko','Wulan','Arif','Sinta']
        await pg.evaluate("""async(ns)=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();ns.forEach(n=>s.players.push({id:'u_'+n.toLowerCase(),nick:n}));s.v++;await r.set(s);}""",names)
        await pg.wait_for_timeout(500); await pg.screenshot(path=f'wk{W}_wait.png',full_page=True)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1000)
        info=json.loads(await pg.evaluate("JSON.stringify({ids:cur.st.players.map(p=>p.id),R:wkRoles(cur.st),me:meIdx(cur.st)})")); ids=info['ids'];R=info['R'];me=info['me']
        print('n',len(ids),'my role',R[me],'roles',''.join(R))
        await pg.screenshot(path=f'wk{W}_night1.png',full_page=True)
        async def as_(uid,js):
            return await pg.evaluate(f"(async()=>{{myId='{uid}';try{{return await ({js});}}finally{{myId='u_me';render();}}}})()")
        shots=set()
        for k in range(600):
            st=json.loads(await pg.evaluate("JSON.stringify({s:cur.st.status,ph:cur.st.phase,n:cur.st.night,d:cur.st.day,alive:cur.st.alive,done:cur.st.done,votes:cur.st.votes,h:cur.st.hunter,lp:cur.st.lastProt})"))
            if st['s']!='playing':break
            al=[i for i,a in enumerate(st['alive']) if a]
            if st['ph']=='night':
                pend=[i for i in al if i not in st['done']]
                i=pend[0]; r=R[i]; mv={'type':'night','skip':True}
                if r=='W' and st['n']>1: mv={'type':'night','t':random.choice([j for j in al if R[j]!='W'])}
                if r=='S': mv={'type':'night','t':random.choice([j for j in al if j!=i])}
                if r=='T': mv={'type':'night','t':random.choice([j for j in al if j!=st['lp']])}
                if i==me:
                    if 'mynight' not in shots and st['n']>1: await pg.screenshot(path=f'wk{W}_mynight.png',full_page=True); shots.add('mynight')
                    if 't' in mv: await pg.click(f'.rpchip.pick[data-i="{mv["t"]}"]'); await pg.click('[data-act="wknight"]')
                    else: await pg.click('[data-act="wkskip"]')
                else: await as_(ids[i],f"hubMove({json.dumps(mv)})")
            elif st['ph']=='day':
                pend=[i for i in al if str(i) not in st['votes']]
                i=pend[0]
                wolves=[j for j in al if R[j]=='W' and j!=i]
                t=random.choice(wolves) if wolves and random.random()<0.45 else random.choice([j for j in al if j!=i])
                if i==me:
                    if 'myday' not in shots: await pg.screenshot(path=f'wk{W}_day.png',full_page=True); shots.add('myday')
                    await pg.click(f'.rpchip.pick[data-i="{t}"]'); await pg.click('[data-act="wkvote"]')
                else: await as_(ids[i],f"hubMove({{type:'vote',t:{t}}})")
            elif st['ph']=='hunter':
                hp=st['h']['p']; t=random.choice(al)
                if hp==me: await pg.screenshot(path=f'wk{W}_hunter.png',full_page=True); await pg.click(f'.rpchip.pick[data-i="{t}"]'); await pg.click('[data-act="wkshoot"]')
                else: await as_(ids[hp],f"hubMove({{type:'shoot',t:{t}}})")
            await pg.wait_for_timeout(60)
        await pg.wait_for_timeout(1500)
        print('status',await pg.evaluate("JSON.stringify({s:cur.st.status,w:cur.st.winner,why:cur.st.winBy,day:cur.st.day,dead:cur.st.deaths.length})"))
        await pg.screenshot(path=f'wk{W}_endmodal.png')
        await pg.click('#mbox [data-act="close"]'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'wk{W}_end.png',full_page=True)
        await pg.wait_for_timeout(600); gid=await pg.evaluate("cur.gid")
        r=json.loads(await pg.evaluate(f"JSON.stringify(__store['results/g_{gid}']||null)"))
        print('result',r and {k:r[k] for k in ['variant','winner','rounds']}, r and sum(1 for x in r['players'] if x['rank']==1),'winners')
        print('stats',await pg.evaluate("JSON.stringify(__store['stats/u_me'].rec.online.wwk)"))
        await pg.evaluate("openHistory()"); await pg.wait_for_timeout(500); await pg.click('.hrow'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'wk{W}_hdet.png')
        print('errors',errs); await b.close()
asyncio.run(main())
