import asyncio,json
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,tag in [({'width':390,'height':844},'m'),({'width':1300,'height':900},'d')]:
            pg=await b.new_page(viewport=vw,device_scale_factor=2 if tag=='m' else 1); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js'); await pg.goto(U); await pg.wait_for_timeout(1500)
            ev=pg.evaluate
            await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
            await pg.click('[data-act="lpmode"][data-m="kota"]'); await pg.wait_for_timeout(200)
            if tag=='m': await pg.screenshot(path='kota_setup.png')
            await ev("document.querySelector('#lpOrd').value='0'")
            await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1500); await ev("closeModal()")
            print(tag,'mode',await ev("cur.st.mode"),'cities',await ev("cur.st.cities"),'patrons',await ev("cur.st.patrons.length"),'name',await ev("cur.st.name"))
            # beri pemain kartu supaya hampir memenuhi satu kota
            await ev("""(()=>{const st=cur.st,p=st.players[cur.human];const id=st.cities[0],K=KOTA[id];
              const want=Object.assign({},K.need);if(K.same)want.r=K.same;if(K.each)COLORS.forEach(c=>want[c]=Math.max(want[c]||0,1));
              for(const c in want){const ids=TIER_IDS[1].filter(x=>CARDS[x].b===c);for(let k=0;k<want[c];k++)p.cards.push(ids[k%ids.length]);}
              const t3=TIER_IDS[3].filter(x=>CARDS[x].pts>=4);let i=0;while(ptsOf(p)<K.pts-3)p.cards.push(t3[i++%t3.length]);
              p.t={w:2,u:2,g:2,r:1,k:1,y:0};render();})()""")
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'kota_board_{tag}.png',full_page=(tag=='m'))
            await pg.click('.kota >> nth=0'); await pg.wait_for_timeout(300)
            print(' info:',(await ev("$('#modal').innerText")).replace('\n',' | ')[:260])
            await pg.screenshot(path=f'kota_info_{tag}.png'); await ev("closeModal()")
            # beli kartu 3 poin supaya merebut kota
            await ev("""(()=>{const st=cur.st,p=st.players[cur.human];const t3=TIER_IDS[3].filter(x=>CARDS[x].pts>=4);let i=0;while(ptsOf(p)<KOTA[st.cities[0]].pts)p.cards.push(t3[i++%t3.length]);render();})()""")
            await ev("attemptMove({type:'pass'})"); await pg.wait_for_timeout(5000)
            print(' after buy kota:',await ev("cur.st.players[cur.human].kota"),'end',await ev("cur.st.endTriggered"),'status',await ev("cur.st.status"),'log',await ev("cur.st.log.slice(-6).map(l=>l.m)"))
            for k in range(20):
                if await ev("cur.st.status")=='ended': break
                await pg.wait_for_timeout(1000)
            print(' status',await ev("cur.st.status"),'winBy',await ev("cur.st.winBy"),'rank',await ev("JSON.stringify(ranking(cur.st))"))
            await pg.wait_for_timeout(1200); await pg.screenshot(path=f'kota_end_{tag}.png')
            print(' end modal:',(await ev("($('#modal')||{}).innerText||''")).replace('\n',' | ')[:200])
            print(' errs',errs)
        # online
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js'); await pg.goto(U); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        await pg.select_option('#modeIn','kota'); await pg.click('#createBtn'); await pg.wait_for_timeout(800)
        print('online mode',await ev("cur.st.mode"),'wait text',[l for l in (await ev("$('#app').innerText")).split('\n') if 'Kota' in l][:2])
        await ev("""(async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push(newPlayer('u_dina','Dina'));s.v++;await r.set(s);})()"""); await pg.wait_for_timeout(500)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200)
        print('online started',await ev("JSON.stringify([cur.st.status,cur.st.mode,cur.st.cities,cur.st.patrons])"),'kotas shown',await ev("document.querySelectorAll('.kota').length"))
        await ev("closeModal();backToLobby&&backToLobby()"); await pg.wait_for_timeout(1500)
        print('lobby pill',await ev("[...document.querySelectorAll('.trow .pill')].map(x=>x.textContent)"))
        print('tutorial',(await ev("(openTutorial('kota'),$('#modal').innerText.slice(0,200))")).replace('\n',' | '))
        print('errs',errs)
        await b.close()
asyncio.run(main())
