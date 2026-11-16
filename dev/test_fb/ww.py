import asyncio,json,sys
from playwright.async_api import async_playwright
W=int(sys.argv[1]) if len(sys.argv)>1 else 1300
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':W,'height':950 if W>500 else 844},device_scale_factor=1 if W>500 else 2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'w{W}_lobby.png',full_page=True)
        await pg.click('[data-act="hubnew"][data-g="werewolf"]'); await pg.wait_for_timeout(600)
        print('created',await pg.evaluate("JSON.stringify({g:cur.st.game,t:cur.st.timer})"))
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();['Dina','Raka','Sari','Bima'].forEach(n=>s.players.push({id:'u_'+n.toLowerCase(),nick:n}));s.v++;await r.set(s);}""")
        await pg.wait_for_timeout(500); await pg.screenshot(path=f'w{W}_wait.png',full_page=True)
        # custom roles modal
        await pg.click('[data-act="wwroles"]'); await pg.wait_for_timeout(200); await pg.screenshot(path=f'w{W}_roles.png')
        await pg.click('#mbox [data-act="close"]')
        # rig: make me Seer by retrying start until my card is S? Instead start and adapt.
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1000)
        info=json.loads(await pg.evaluate("JSON.stringify({ids:cur.st.players.map(p=>p.id),deal:wwDeal(cur.st),me:meIdx(cur.st),inPlay:cur.st.inPlay})")); print(info)
        await pg.screenshot(path=f'w{W}_night.png',full_page=True)
        n=len(info['ids']); deal=info['deal']
        async def as_(uid,js):
            return await pg.evaluate(f"(async()=>{{myId='{uid}';try{{return await ({js});}}finally{{myId='u_me';render();}}}})()")
        def mv(i):
            r=deal[i]; o=(i+1)%n
            if r=='S':return "{type:'night',c:[0,2]}"
            if r=='R':return f"{{type:'night',p:{o}}}"
            if r=='T':return f"{{type:'night',ps:[{o},{(i+2)%n}]}}"
            if r=='D':return "{type:'night',c:1}"
            if r=='W':return "{type:'night',c:0}"
            return "{type:'night'}"
        me=info['me']
        # me via UI
        r=deal[me]; print('my role',r)
        if r in 'SRTDW':
            if r=='S': await pg.click('.wwcard.pick[data-c="0"]'); await pg.click('.wwcard.pick[data-c="2"]')
            elif r=='R': await pg.click(f'.rpchip.pick[data-i="{(me+1)%n}"]')
            elif r=='T': await pg.click(f'.rpchip.pick[data-i="{(me+1)%n}"]'); await pg.click(f'.rpchip.pick[data-i="{(me+2)%n}"]')
            elif r in 'DW':
                if await pg.query_selector('.wwcard.pick'): await pg.click('.wwcard.pick[data-c="1"]')
            await pg.wait_for_timeout(150); await pg.screenshot(path=f'w{W}_nightsel.png',full_page=True)
            if await pg.query_selector('[data-act="wnight"]:not([disabled])'): await pg.click('[data-act="wnight"]')
            else: await pg.click('[data-act="wskip"]')
        else: await pg.click('[data-act="wnight"]')
        await pg.wait_for_timeout(400); await pg.screenshot(path=f'w{W}_nightdone.png',full_page=True)
        print('me info:',await pg.inner_text('.wwinfo') if await pg.query_selector('.wwinfo') else '-')
        for i,u in enumerate(info['ids']):
            if i==me:continue
            await as_(u,f"hubMove({mv(i)})"); await pg.wait_for_timeout(120)
        await pg.wait_for_timeout(800)
        print('phase',await pg.evaluate("cur.st.phase"),'final',await pg.evaluate("wwFinal(cur.st).join('')"))
        await pg.screenshot(path=f'w{W}_day.png',full_page=True)
        # votes: everyone votes player 0 except player0 votes 1
        for i,u in enumerate(info['ids']):
            t=1 if i==0 else 0
            if i==me:
                await pg.click(f'.rpchip.pick[data-i="{t}"]'); await pg.wait_for_timeout(100); await pg.click('[data-act="wvoteok"]'); await pg.wait_for_timeout(300)
                if i==me and W>500: await pg.screenshot(path=f'w{W}_voted.png',full_page=True)
            else: await as_(u,f"hubMove({{type:'vote',target:{t}}})")
            await pg.wait_for_timeout(120)
        await pg.wait_for_timeout(1500)
        print('status',await pg.evaluate("cur.st.status"),await pg.evaluate("cur.st.winBy"))
        await pg.screenshot(path=f'w{W}_endmodal.png')
        await pg.click('#mbox [data-act="close"]'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'w{W}_end.png',full_page=True)
        await pg.wait_for_timeout(500)
        gid=await pg.evaluate("cur.gid")
        r=json.loads(await pg.evaluate(f"JSON.stringify(__store['results/g_{gid}']||null)"))
        print('result',r and {k:r[k] for k in ['variant','winner','winBy']}, r and [(x['nick'],x['rank'],x['orig'],x['role'],x['dead']) for x in r['players']])
        print('stats',await pg.evaluate("JSON.stringify(__store['stats/u_me'].rec.online)"))
        await pg.evaluate("openHistory()"); await pg.wait_for_timeout(600); await pg.click('.hrow'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'w{W}_hdet.png')
        print('errors',errs); await b.close()
asyncio.run(main())
