import asyncio, json
from playwright.async_api import async_playwright
SEED="""()=>{const mk=(id,mode,variant,rank,lvl,t)=>{__store['results/'+id]={variant,mode,level:lvl,name:'x',endedAt:t,week:weekKey(t),rounds:20,ids:['u_me'],
  players:[{id:'u_me',nick:'Farhan',bot:false,pts:rank===1?16:9,cards:10,rank},{id:mode==='online'?'u_b':null,nick:'Dina',bot:mode!=='online',pts:12,cards:9,rank:rank===1?2:1}],award:mode==='online'?{u_me:{total:rank===1?50:10,base:20,score:10,margin:0,speed:0,rank}}:{},log:[]};};
  let t=Date.now()-1e8;[['online','klasik',1],['online','klasik',2],['online','duel',1],['bot','klasik',1,'normal'],['bot','klasik',1,'hard'],['bot','duel',2,'easy'],['bot','klasik',1,'easy']].forEach((x,i)=>mk('r'+i,x[0],x[1],x[2],x[3]||null,t+i*1e5));}"""
async def page(b,vw,mock='mock.js'):
    pg=await b.new_page(viewport=vw,device_scale_factor=1 if vw['width']>800 else 2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/'+mock)
    await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
    await pg.evaluate("c0delay=()=>120"); return pg,errs
async def startLocal(pg,mode='klasik',n=2):
    await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(250)
    if mode=='duel': await pg.click('[data-act="lpmode"][data-m="duel"], [data-act="lpMode"][data-m="duel"]')
    else: await pg.select_option('#lpN',str(n))
    await pg.wait_for_timeout(150); await pg.evaluate("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg,errs=await page(b,{'width':1280,'height':860})
        await pg.evaluate(SEED)
        await startLocal(pg)
        # pick 3 tokens -> pending in meter, screenshot
        for c in ['w','u','g']: await pg.click(f'.bank [data-act="tok"][data-c="{c}"]'); await pg.wait_for_timeout(80)
        print('cap pending:',await pg.inner_text('.pl.mine-pl .cap'))
        await pg.screenshot(path='s_desk_pend.png')
        await pg.click('[data-act="take"]'); await pg.wait_for_timeout(1500)
        snap=await pg.evaluate("({round:cur.st.round,log:cur.st.log.length,turn:cur.st.turn,lid:cur.lid,me:tokTotal(cur.st.players[0])})")
        print('caps:',await pg.evaluate("[...document.querySelectorAll('.pl .cap')].map(e=>e.innerText.replace(/\\n/g,' '))"))
        await pg.click('#backBtn'); await pg.wait_for_timeout(300)
        print('leave modal:',(await pg.inner_text('#mbox'))[:120].replace('\n',' | '))
        await pg.screenshot(path='s_leave.png')
        await pg.click('[data-act="savequit"]'); await pg.wait_for_timeout(500)
        print('after save view:',await pg.evaluate("view"),'db save:',await pg.evaluate("!!__store['saves/u_me']"),'ls:',await pg.evaluate("!!localStorage.getItem('sp_save_u_me')"))
        # history with filters
        await pg.click('[data-act="history"]'); await pg.wait_for_timeout(500)
        print('hist head:',(await pg.inner_text('#mbox'))[:260].replace('\n',' | '))
        await pg.click('[data-act="hfilter"][data-v="bot"]'); await pg.wait_for_timeout(150)
        await pg.click('[data-act="hfilter"][data-v="klasik"]'); await pg.wait_for_timeout(150)
        print('bot+klasik:',await pg.inner_text('#mbox p.bd'))
        await pg.screenshot(path='s_hist.png')
        await pg.click('#mbox [data-act="resume"]'); await pg.wait_for_timeout(600)
        snap2=await pg.evaluate("({round:cur.st.round,log:cur.st.log.length,turn:cur.st.turn,lid:cur.lid,me:tokTotal(cur.st.players[0])})")
        print('resume equal:',snap==snap2 or (snap,snap2))
        # leave without saving
        await pg.click('#backBtn'); await pg.wait_for_timeout(300); await pg.click('[data-act="nosavequit"]'); await pg.wait_for_timeout(300)
        print('nosave view:',await pg.evaluate("view"),'save still:',await pg.evaluate("!!__store['saves/u_me']"))
        # profile record table
        await pg.click('[data-act="profile"]'); await pg.wait_for_timeout(600)
        print('profile rec:',(await pg.inner_text('table.rec')).replace('\n',' | ').replace('\t',' '))
        await pg.screenshot(path='s_prof.png',full_page=False)
        # resume from profile and finish -> save deleted
        await pg.click('#mbox [data-act="resume"]'); await pg.wait_for_timeout(500)
        await pg.evaluate("(()=>{const st=cur.st;st.players[cur.human].cards=['3r1','3k1','3u1','2g4'];st.endTriggered=true;st.turn=cur.human;st.round=19;for(let i=0;i<st.players.length;i++)if(i!==cur.human)st.players[i].cards=[];})()")
        # make human last in round: set turn to last player index
        await pg.evaluate("(()=>{const st=cur.st;})()")
        for k in range(30):
            if await pg.evaluate("cur.st.status")=='ended': break
            if await pg.evaluate("cur.st.turn===cur.human"): await pg.evaluate("(async()=>{await runMove({type:'pass'});})()")
            await pg.wait_for_timeout(300)
        await pg.wait_for_timeout(600)
        print('ended:',await pg.evaluate("cur.st.status"),'save deleted:',await pg.evaluate("!__store['saves/u_me']&&!localStorage.getItem('sp_save_u_me')"),'result recorded:',await pg.evaluate("Object.keys(__store).filter(k=>k.startsWith('results/b')).length"))
        # ended game -> back no prompt
        await pg.click('#backBtn'); await pg.wait_for_timeout(300); print('ended back view:',await pg.evaluate("view"))
        print('errs1',errs)
        # mobile klasik 3 bots
        # guest
        pgst,e4=await page(b,{'width':390,'height':844},'mock_guest.js')
        await startLocal(pgst)
        await pgst.evaluate("(async()=>{await runMove({type:'pass'});})()"); await pgst.wait_for_timeout(800)
        await pgst.click('#backBtn'); await pgst.wait_for_timeout(300)
        g1=await pgst.inner_text('#mbox'); await pgst.click('[data-act="savequit"]'); await pgst.wait_for_timeout(400)
        await pgst.click('#profBtn'); await pgst.wait_for_timeout(400)
        print('guest:', 'Tamu' in g1, 'db', await pgst.evaluate("!!__store['saves/u_me']"), 'ls', await pgst.evaluate("!!localStorage.getItem('sp_save_u_me')"), 'card', await pgst.evaluate("!!document.querySelector('#mbox .savecard')"))
        await pgst.screenshot(path='s_guest_hist.png')
        await pgst.click('#mbox [data-act="resume"]'); await pgst.wait_for_timeout(500); print('guest resumed:',await pgst.evaluate("view+' '+cur.st.status"))
        await pgst.click('#backBtn'); await pgst.wait_for_timeout(300); await pgst.click('[data-act="nosavequit"]'); await pgst.wait_for_timeout(300)
        await pgst.click('#profBtn'); await pgst.wait_for_timeout(300)
        await pgst.click('#mbox [data-act="delsave"]'); await pgst.wait_for_timeout(200); await pgst.click('[data-act="delsaveok"]'); await pgst.wait_for_timeout(300)
        await pgst.wait_for_timeout(300); print('guest card after del:',await pgst.evaluate("!!document.querySelector('#mbox .savecard')"))
        print('guest del:',await pgst.evaluate("!localStorage.getItem('sp_save_u_me')"),'errs',e4)
        await b.close()
asyncio.run(main())
