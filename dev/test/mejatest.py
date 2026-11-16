import asyncio
from playwright.async_api import async_playwright
async def page(b,vw={'width':1280,'height':860}):
    pg=await b.new_page(viewport=vw); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js'); await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
    await pg.evaluate("c0delay=()=>120"); return pg,errs
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg,errs=await page(b)
        # 1 meja per akun
        await pg.fill('#tblIn','Meja Satu'); await pg.click('#createBtn'); await pg.wait_for_timeout(600)
        await pg.click('#backBtn'); await pg.wait_for_timeout(400)
        await pg.fill('#tblIn','Meja Dua'); await pg.click('#createBtn'); await pg.wait_for_timeout(700)
        print('second create modal:',(await pg.inner_text('#mbox'))[:110].replace('\n',' | '))
        await pg.screenshot(path='m_one.png')
        await pg.click('#mbox [data-act="openmine"]'); await pg.wait_for_timeout(400)
        print('opened mine:',await pg.evaluate("cur.st.name"))
        await pg.click('#backBtn'); await pg.wait_for_timeout(300)
        await pg.click('#createBtn'); await pg.wait_for_timeout(600); await pg.click('#mbox [data-act="replacetbl"]'); await pg.wait_for_timeout(900)
        print('replace -> games:',await pg.evaluate("Object.values(__store).filter(x=>x&&x.host==='u_me'&&x.status).map(x=>x.name)"),'view',await pg.evaluate("view"))
        await pg.click('#backBtn'); await pg.wait_for_timeout(300)
        # 2 jam idle + ended hidden & cleaned
        await pg.evaluate("""()=>{const now=Date.now();const g=(id,status,age)=>{__store['games/'+id]={name:id,host:'u_x'+id,createdAt:now-age,updatedAt:now-age,status,players:[newPlayer('u_x'+id,'X')],v:1};};
          g('idleLobby','lobby',2.1*3600e3);g('idlePlay','playing',2.2*3600e3);g('okPlay','playing',1.5*3600e3);g('justEnded','ended',30e3);}""")
        await pg.evaluate("cleanupGames()"); await pg.wait_for_timeout(800)
        print('after cleanup:',await pg.evaluate("Object.keys(__store).filter(k=>k.startsWith('games/')).map(k=>__store[k].name)"))
        await pg.evaluate("lobbyGames=Object.keys(__store).filter(k=>k.startsWith('games/')).map(k=>({...__store[k],_id:k.slice(6)}));render()")
        print('lobby list:',(await pg.inner_text('#tableList')).replace('\n',' | ')[:200])
        # online game end -> table deleted after ~20s, player stays on result
        await pg.evaluate("""()=>{const st={name:'Meja Final',host:'u_me',createdAt:Date.now(),status:'lobby',players:[newPlayer('u_me','Farhan'),newPlayer('u_b','Dina')],v:1};
          startGame(st); st.players[0].cards=['3r1','3k1','3u1','2g4']; st.endTriggered=true; st.turn=1; st.round=19; __store['games/tfin']=st;}""")
        await pg.evaluate("openTable('tfin')"); await pg.wait_for_timeout(600)
        await pg.evaluate("(async()=>{const s=__store['games/tfin'];doMove(s,1,{type:'pass'});s.v++;await db.doc('games/tfin').set(s);})()"); await pg.wait_for_timeout(1500)
        print('ended:',await pg.evaluate("cur.st.status"),'popup',await pg.evaluate("document.getElementById('modal').classList.contains('open')"))
        await pg.wait_for_timeout(21000)
        print('table doc gone:',await pg.evaluate("!__store['games/tfin']"),'still viewing result:',await pg.evaluate("view+' '+(cur&&cur.st.status)"),'results saved',await pg.evaluate("!!__store['results/g_tfin']"))
        print('errs',errs)
        # rank pop in local game
        pm,e2=await page(b,{'width':390,'height':844})
        await pm.click('[data-act="localSetup"]'); await pm.wait_for_timeout(250); await pm.evaluate("document.querySelector('#lpOrd').value='0'"); await pm.click('[data-act="localStart"]'); await pm.wait_for_timeout(500)
        chip=await pm.inner_text('.rankchip')
        await pm.evaluate("(()=>{const st=cur.st;st.players[1].cards=['3r1'];render();})()"); await pm.wait_for_timeout(400)
        t1=await pm.evaluate("(document.getElementById('rankpop')||{}).innerText")
        await pm.screenshot(path='m_rank_down.png')
        await pm.evaluate("(()=>{const st=cur.st;st.players[0].cards=['3r1','3k1'];render();})()"); await pm.wait_for_timeout(400)
        t2=await pm.evaluate("document.getElementById('rankpop').innerText")
        await pm.evaluate("(()=>{const st=cur.st;st.players[1].cards=['3r1','3k1','3u1','2g4','3w1'];st.endTriggered=true;render();})()"); await pm.wait_for_timeout(400)
        t3=await pm.evaluate("document.getElementById('rankpop').innerText")
        await pm.screenshot(path='m_rank_last.png')
        print('chip',chip,'| down:',t1.replace('\n',' / '),'| up:',t2.replace('\n',' / '),'| last:',t3.replace('\n',' / '),e2)
        await b.close()
asyncio.run(main())
