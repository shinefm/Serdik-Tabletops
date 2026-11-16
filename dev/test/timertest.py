import asyncio
from playwright.async_api import async_playwright
async def page(b,vw={'width':1280,'height':860}):
    pg=await b.new_page(viewport=vw,device_scale_factor=1 if vw['width']>800 else 2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
    await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
    await pg.evaluate("c0delay=()=>150"); return pg,errs
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        # A. local
        pg,errs=await page(b)
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(250)
        dflt=await pg.evaluate("document.querySelector('#lpTmr').value")
        names=await pg.evaluate("[...document.querySelectorAll('.lpName')].map(x=>x.value)")
        await pg.select_option('#lpTmr','30'); await pg.evaluate("document.querySelector('#lpOrd').value='0'")
        await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(500)
        pill=await pg.inner_text('.tmr')
        await pg.evaluate("cur.st.turnAt=Date.now()-31000"); await pg.wait_for_timeout(900)
        print('A local default timer:',dflt,'bot names:',names,'pill:',pill,'-> after timeout:',await pg.evaluate("cur.st.log.filter(l=>l.p===0).map(l=>l.m)"),errs)
        await pg.wait_for_timeout(2500)
        print('   names in log:',await pg.evaluate("cur.st.log.slice(-3).map(l=>l.p>=0?nm(cur.st,l.p)+': '+l.m:l.m)"))
        # B. online table with bots
        pg,errs=await page(b)
        dsel=await pg.evaluate("document.querySelector('#timerIn').value")
        await pg.fill('#tblIn','Meja Uji Bot'); await pg.click('#createBtn'); await pg.wait_for_timeout(600)
        await pg.select_option('#obLv','easy'); await pg.click('[data-act="addbot"]'); await pg.wait_for_timeout(400)
        await pg.click('[data-act="addbot"]'); await pg.wait_for_timeout(400)
        await pg.select_option('#tmrSel','60'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='t_wait.png')
        gid=await pg.evaluate("cur.gid")
        st=await pg.evaluate(f"__store['games/{gid}']")
        print('B create default:',dsel,'timer now',st['timer'],'players',[(x['nick'],x.get('bot'),x.get('level')) for x in st['players']])
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(500)
        for k in range(40):
            s=await pg.evaluate("({turn:cur.st.turn,mi:meIdx(cur.st),bot:cur.st.players[cur.st.turn].bot,round:cur.st.round})")
            if s['round']>=3: break
            if s['turn']==s['mi']: await pg.evaluate("(async()=>{await runMove({type:'pass'});})()")
            await pg.wait_for_timeout(500)
        log=await pg.evaluate("cur.st.log.map(l=>(l.p>=0?nm(cur.st,l.p)+': ':'')+l.m)")
        print('B bots moved:',len([l for l in log if 'mengambil' in l or 'membeli' in l or 'mencadangkan' in l]),'round',s['round']); print('   ',log[-4:])
        await pg.screenshot(path='t_online.png')
        # timeout on my turn
        for k in range(20):
            if await pg.evaluate("cur.st.turn===meIdx(cur.st)"): break
            await pg.wait_for_timeout(400)
        await pg.evaluate(f"(async()=>{{const s=__store['games/{gid}'];s.turnAt=Date.now()-61000;s.v++;await db.doc('games/{gid}').set(s);}})()"); await pg.wait_for_timeout(1500)
        print('B my timeout:',await pg.evaluate("cur.st.log.filter(l=>l.m.includes('kehabisan')).map(l=>nm(cur.st,l.p)+': '+l.m)"),errs)
        # C. another human times out -> I pass for them after grace; D. award with bots
        await pg.evaluate("""(async()=>{const st={name:'Meja Dua',host:'u_b',createdAt:Date.now(),status:'lobby',timer:60,players:[newPlayer('u_b','Dina'),newPlayer('u_me','Farhan')],v:1};
           const b=newPlayer('bot_x','Daendels');b.bot=true;b.level='easy';st.players.push(b);startGame(st);st.turn=0;st.turnAt=Date.now()-66000;__store['games/tdua']=st;})()""")
        await pg.evaluate("backToLobby();openTable('tdua')"); await pg.wait_for_timeout(2500)
        print('C other timeout passed by me:',await pg.evaluate("cur.st.log.filter(l=>l.m.includes('kehabisan')).map(l=>nm(cur.st,l.p))"))
        aw=await pg.evaluate("""(()=>{const st=clone(cur.st);st.status='ended';st.players[0].cards=['3r1','3k1'];st.players[2].cards=['3r1','3k1','3u1','2g4'];st.players[1].cards=['1w1'];return awardPoints(st);})()""")
        print('D award (bot won, 2 humans):',aw)
        # E. join replaces bot
        await pg.evaluate("""(()=>{const st={name:'Penuh',host:'u_b',createdAt:Date.now(),status:'lobby',mode:'duel',timer:180,players:[newPlayer('u_b','Dina')],v:1};const b=newPlayer('bot_y','Raffles');b.bot=true;st.players.push(b);__store['games/tpenuh']=st;})()""")
        await pg.evaluate("backToLobby();openTable('tpenuh')"); await pg.wait_for_timeout(500)
        jt=await pg.inner_text('[data-act="join"]'); await pg.click('[data-act="join"]'); await pg.wait_for_timeout(500)
        print('E join:',jt,'->',await pg.evaluate("__store['games/tpenuh'].players.map(p=>p.nick||p.id)"),errs)
        await b.close()
asyncio.run(main())
