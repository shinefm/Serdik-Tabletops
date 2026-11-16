import asyncio
from playwright.async_api import async_playwright
# drive the guide to its last step using the same automatic player
async def drive(pg,stop_at_last=True):
    for it in range(220):
        info=await pg.evaluate("""()=>{const g=ui.guide;if(!g)return null;const s=g.steps[g.i];const st=cur.st;const myT=st.turn===cur.human;
           return {i:g.i,last:!!s.last,next:!!s.next,wait:!!s.wait||(s.turn&&!myT),sels:(s.sel&&!(s.wait||(s.turn&&!myT)))?s.sel(g):[]};}""")
        if info is None or (info['last'] and stop_at_last): return info
        if info['wait']: await pg.wait_for_timeout(300); continue
        if info['next']: await pg.click('#gd [data-act="guidenext"]'); await pg.wait_for_timeout(250); continue
        i0=info['i']
        for sel in info['sels']:
            await pg.evaluate("s=>{const e=document.querySelector(s);if(e)e.click();}",sel); await pg.wait_for_timeout(120)
            if await pg.evaluate("ui.guide?ui.guide.i:null")!=i0: break
        await pg.wait_for_timeout(300)
async def startguide(pg,w):
    await pg.click('#tutBtn, [data-act="tutorial"] >> nth=0'); await pg.wait_for_timeout(300)
    if w=='duel': await pg.click('.tabs [data-w="duel"]'); await pg.wait_for_timeout(200)
    await pg.click('[data-act="guided"]'); await pg.wait_for_timeout(400)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        async def page(vw):
            pg=await b.new_page(viewport=vw); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
            await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
            await pg.evaluate("c0delay=()=>150"); return pg,errs
        # 1 lobby -> guide finish -> back to lobby
        pg,errs=await page({'width':1280,'height':860})
        await startguide(pg,'klasik'); info=await drive(pg)
        btn=await pg.inner_text('#gd [data-act="guidehome"]'); await pg.screenshot(path='ret_last.png')
        await pg.click('#gd [data-act="guidehome"]'); await pg.wait_for_timeout(400)
        print('1 lobby:',btn,'->',await pg.evaluate("({view,cur:!!cur,gd:!!document.getElementById('gd')})"),errs)
        # 2 local bot game mid-play -> guide -> quit midway -> same game back
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
        await pg.evaluate("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
        await pg.evaluate("(async()=>{await runMove({type:'pass'});})()"); await pg.wait_for_timeout(900)
        lid=await pg.evaluate("cur.lid+'|'+cur.st.log.length")
        await startguide(pg,'duel'); await pg.wait_for_timeout(300)
        lab=await pg.inner_text('#backBtn .lbl')
        await pg.click('#gd [data-act="next"], #gd [data-act="guidenext"]'); await pg.wait_for_timeout(200)
        await pg.click('#gd [data-act="guidequit"]'); await pg.wait_for_timeout(1200)
        print('2 local: header label during guide =',lab,'| back to',await pg.evaluate("({view,same:cur.lid,guided:!!cur.guided,mode:cur.st.mode,turn:cur.st.turn,log:cur.st.log.length})"),'was',lid,errs)
        # 3 online table -> guide finish -> back to table
        await pg.evaluate("""()=>{const st={name:'Meja Uji',host:'u_b',createdAt:Date.now(),status:'lobby',players:[newPlayer('u_b','Dina'),newPlayer('u_me','Farhan')],v:1};startGame(st);st.turn=0;__store['games/tuji']=st;}""")
        await pg.evaluate("backToLobby();openTable('tuji')"); await pg.wait_for_timeout(500)
        await startguide(pg,'duel'); info=await drive(pg)
        btn=await pg.inner_text('#gd [data-act="guidehome"]')
        await pg.click('#gd [data-act="guidehome"]'); await pg.wait_for_timeout(600)
        print('3 online:',btn,'->',await pg.evaluate("({view,gid:cur&&cur.gid,local:cur&&cur.local,name:cur&&cur.st&&cur.st.name})"),errs)
        # 4 online -> guide finish -> main terus -> header back -> table
        await startguide(pg,'klasik'); info=await drive(pg)
        await pg.click('#gd [data-act="guidenext"]'); await pg.wait_for_timeout(300)
        lab=await pg.inner_text('#backBtn .lbl'); still=await pg.evaluate("({guided:!!cur.guided,gd:!!document.getElementById('gd')})")
        await pg.click('#backBtn'); await pg.wait_for_timeout(600)
        print('4 main terus:',still,'header=',lab,'->',await pg.evaluate("({view,gid:cur&&cur.gid})"),errs)
        # 5 mobile from lobby finish
        pg2,e2=await page({'width':390,'height':844})
        await startguide(pg2,'duel'); await drive(pg2); await pg2.screenshot(path='ret_last_m.png')
        await pg2.click('#gd [data-act="guidehome"]'); await pg2.wait_for_timeout(400)
        print('5 mobile:',await pg2.evaluate("({view})"),e2)
        await b.close()
asyncio.run(main())
