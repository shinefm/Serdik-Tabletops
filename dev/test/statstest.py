import asyncio, json
from playwright.async_api import async_playwright
async def page(b,path='/home/claude/serdik-tabletops/dev/saudagar-permata.html',mock='mock.js',vw={'width':1280,'height':860}):
    pg=await b.new_page(viewport=vw); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/'+mock)
    await pg.goto('file://'+path); await pg.wait_for_timeout(1200); await pg.evaluate("c0delay=()=>120"); return pg,errs
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg,errs=await page(b)
        # seed old results (pre-stats) + stale games
        await pg.evaluate("""()=>{const now=Date.now();const mk=(id,mode,rank,t,award)=>{__store['results/'+id]={variant:'klasik',mode,level:mode==='bot'?'normal':null,name:'x',endedAt:t,week:weekKey(t),rounds:20,ids:mode==='online'?['u_me','u_b']:['u_me'],
          players:[{id:'u_me',nick:'Farhan',pts:rank===1?16:9,cards:9,rank},{id:mode==='online'?'u_b':null,nick:'Dina',pts:12,cards:9,rank:rank===1?2:1}],award:award||{},log:[]};};
          mk('o1','online',1,now-3e5,{u_me:{rank:1,base:20,score:16,margin:8,speed:16,total:60},u_b:{rank:2,base:4,score:12,margin:0,speed:0,total:16}});
          mk('o2','online',2,now-2e5,{u_me:{rank:2,base:4,score:9,margin:0,speed:0,total:13},u_b:{rank:1,base:20,score:12,margin:6,speed:10,total:48}});
          mk('b1','bot',1,now-1e5);
          const g=(id,status,age)=>{__store['games/'+id]={name:id,host:'u_b',createdAt:now-age,updatedAt:now-age,status,players:[newPlayer('u_b','Dina')],v:1};};
          g('gOldEnded','ended',3600e3);g('gOldLobby','lobby',13*3600e3);g('gFresh','lobby',60e3);g('gPlay','playing',120e3);g('gDead','playing',50*3600e3);}""")
        await pg.evaluate("isOwnerFlag=true")
        await pg.click('[data-act="leaderboard"]'); await pg.wait_for_timeout(1200)
        print('lb week:',(await pg.inner_text('#mbox table.lb')).replace('\n',' | ').replace('\t',' '))
        st=await pg.evaluate("__store['stats/u_me']")
        print('stats u_me after auto-rebuild:',{k:st[k] for k in ['pts','games','wins','wkPts','best','streak','top','fast']},st['rec'])
        await pg.click('#mbox [data-act="lbtab"][data-t="all"]'); await pg.wait_for_timeout(500)
        print('lb all:',(await pg.inner_text('#mbox table.lb')).replace('\n',' | ').replace('\t',' ')[:200])
        await pg.click('#mbox [data-act="close"]')
        # play a bot game to the end -> stats bump
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(250); await pg.evaluate("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
        await pg.evaluate("(()=>{const st=cur.st;st.players[cur.human].cards=['3r1','3k1','3u1','2g4'];st.endTriggered=true;})()")
        for k in range(30):
            if await pg.evaluate("cur.st.status")=='ended': break
            if await pg.evaluate("cur.st.turn===cur.human"): await pg.evaluate("(async()=>{await runMove({type:'pass'});})()")
            await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(1200)
        st=await pg.evaluate("__store['stats/u_me']"); print('after bot win: bot klasik',st['rec']['bot']['klasik'],'streak',st['streak'],'pts',st['pts'])
        print('replay ids:',await pg.evaluate("Object.keys(__store).filter(k=>k.startsWith('replays/'))"))
        await pg.click('#mbox [data-act="lobby"]'); await pg.wait_for_timeout(4500)
        print('games left after cleanup:',await pg.evaluate("Object.keys(__store).filter(k=>k.startsWith('games/'))"),'| lobby:',await pg.inner_text('#lobbyStatus'))
        await pg.click('[data-act="profile"]'); await pg.wait_for_timeout(800)
        print('profile rec:',(await pg.inner_text('table.rec')).replace('\n',' | ').replace('\t',' ')[:220])
        await pg.click('#mbox [data-act="close"]')
        # online game end with 2 humans + bot -> stats for both
        await pg.evaluate("""()=>{const st={name:'Meja Uji',host:'u_b',createdAt:Date.now(),status:'lobby',timer:0,players:[newPlayer('u_b','Dina'),newPlayer('u_me','Farhan')],v:1};const bb=newPlayer('bot_q','Raffles');bb.bot=true;st.players.push(bb);
          startGame(st); st.players[1].cards=['3r1','3k1','3u1','2g4']; st.endTriggered=true; st.turn=2; st.round=19; __store['games/tuji']=st;}""")
        await pg.evaluate("openTable('tuji')"); await pg.wait_for_timeout(5000)
        sb=await pg.evaluate("__store['stats/u_b']"); sm=await pg.evaluate("__store['stats/u_me']")
        print('online end status:',await pg.evaluate("cur.st.status"),'u_b pts',sb['pts'],'games',sb['games'],'| u_me pts',sm['pts'],'online rec',sm['rec']['online'])
        # idempotent: call onGameEnded again
        await pg.evaluate("ui.saved={};onGameEnded(cur.st)"); await pg.wait_for_timeout(800)
        print('idempotent:',(await pg.evaluate("__store['stats/u_me'].pts"))==sm['pts'])
        print('errs',errs)
        # latihan edition
        h=open('/home/claude/serdik-tabletops/dev/saudagar-permata.html').read().replace("const EDITION='liga';","const EDITION='latihan';")
        open('/tmp/latihan.html','w').write(h)
        pl,e2=await page(b,'/tmp/latihan.html')
        print('latihan: create visible',await pl.evaluate("getComputedStyle(document.getElementById('createBtn')).display"),'tables panel',await pl.evaluate("getComputedStyle(document.getElementById('tableList').parentElement).display"),'guest',await pl.evaluate("isGuest()"),'profBtn',await pl.inner_text('#profBtn'),e2)
        await pl.screenshot(path='latihan.png')
        await b.close()
asyncio.run(main())
