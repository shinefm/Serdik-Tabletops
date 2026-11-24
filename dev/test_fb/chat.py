import asyncio,json
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
MOCK='/home/claude/serdik-tabletops/dev/test/mockfb.js'
def ck(name,ok,extra=''):
    print(('PASS ' if ok else 'FAIL ')+name,extra)
async def page(b,w,h):
    pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path=MOCK); await pg.goto(U); await pg.wait_for_timeout(1500); return pg,errs
INJ="(t)=>firebase.database().ref('chat/'+cur.gid+'/msg').push().set({u:'u_dina',n:'Dina',t,ts:Date.now()})"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        # ---------- A. Saudagar Permata online, desktop ----------
        pg,errs=await page(b,1300,900); ev=pg.evaluate
        await pg.click('#createBtn'); await pg.wait_for_timeout(1000)
        await ev("commitOnline(s=>{s.players.push(newPlayer('u_dina','Dina'));})"); await pg.wait_for_timeout(400)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        gid=await ev("cur.gid")
        ck('tabs shown',await ev("document.querySelectorAll('.lgtabs [data-lt]').length")==2)
        ck('log tab default',await ev("!document.querySelector('.lglog').hidden && document.getElementById('chatSlot').hidden"))
        await pg.click('.lgtabs [data-lt="chat"]'); await pg.wait_for_timeout(200)
        ck('chat pane visible',await ev("!document.getElementById('chatSlot').hidden && document.querySelector('details.log').open"))
        await pg.fill('.chatin input','Halo semua <b>x</b>'); await pg.press('.chatin input','Enter'); await pg.wait_for_timeout(500)
        ck('my msg shown',await ev("[...document.querySelectorAll('.cmsg.me .ct')].map(e=>e.textContent).join('|')")=='Halo semua <b>x</b>')
        raw=json.loads(await ev(f"JSON.stringify(__RTDB.chat&&__RTDB.chat['{gid}'])"))
        ck('stored in rtdb only',bool(raw and raw.get('msg') and raw.get('m',{}).get('u_me')),json.dumps(raw)[:200])
        ck('not in firestore',await ev("!JSON.stringify(__FS).includes('Halo semua')"))
        await ev(INJ,'gas main'); await pg.wait_for_timeout(400)
        ck('other msg shown, no badge',await ev("JSON.stringify([[...document.querySelectorAll('.cmsg:not(.me) .cn')].map(e=>e.textContent),document.querySelector('.cbadge').hidden])")=='[["Dina"],true]')
        await pg.click('.lgtabs [data-lt="log"]'); await pg.wait_for_timeout(200)
        await ev(INJ,'ayo'); await ev(INJ,'cepet'); await pg.wait_for_timeout(400)
        ck('badge 2 on log tab',await ev("document.querySelector('.cbadge').textContent")=='2')
        # render tidak menghapus ketikan & fokus
        await pg.click('.lgtabs [data-lt="chat"]'); await pg.wait_for_timeout(200)
        ck('badge cleared',await ev("document.querySelector('.cbadge').hidden"))
        await pg.fill('.chatin input','lagi ngetik'); await pg.focus('.chatin input')
        t=await ev("cur.st.turn"); pid=await ev(f"cur.st.players[{t}].id")
        await ev(f"(async()=>{{myId='{pid}';try{{await commitOnline(s=>{{doMove(s,s.turn,botMove(s,s.turn,'normal'));}});}}finally{{myId='u_me';}}}})()"); await pg.wait_for_timeout(600)
        ck('typing kept across render',await ev("document.querySelector('.chatin input').value==='lagi ngetik'&&document.activeElement===document.querySelector('.chatin input')"),await ev("cur.st.v"))
        print('   ',await ev("JSON.stringify([document.querySelector('.chatin input').value,document.activeElement===document.querySelector('.chatin input')])"))
        await pg.fill('.chatin input','')
        await pg.screenshot(path='chat_d.png')
        # spectator tidak bisa kirim
        await ev("myId='u_lihat';render()"); await pg.wait_for_timeout(200)
        ck('spectator disabled',await ev("document.querySelector('.chatin input').disabled"))
        await ev("myId='u_me';render()"); await pg.wait_for_timeout(200)
        # game selesai -> chat dihapus dari server
        await ev("commitOnline(s=>{s.status='ended';s.log.push({p:-1,m:'Permainan selesai.'});})"); await pg.wait_for_timeout(800); await ev("closeModal()"); await pg.wait_for_timeout(200)
        ck('wiped on end',await ev(f"!(__RTDB.chat&&__RTDB.chat['{gid}'])"))
        ck('messages still on screen, input off',await ev("JSON.stringify([document.querySelectorAll('.cmsg').length,document.querySelector('.chatin input').disabled])")=='[4,true]')
        await pg.screenshot(path='chat_end.png')
        await ev("leaveTable()"); await pg.wait_for_timeout(400)
        ck('stopped after leave',await ev("CH.gid===null&&!CH.el"))
        print('errs A',errs); await pg.close()

        # ---------- B. Pemukim online, mobile ----------
        pg,errs=await page(b,390,844); ev=pg.evaluate
        await pg.click('[data-act="hubnew"][data-g="pemukim"]'); await pg.wait_for_timeout(600)
        await pg.click('[data-act="addbot"]'); await pg.wait_for_timeout(300)
        await ev("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push({id:'u_dina',nick:'Dina'});s.v++;await r.set(s);}"""); await pg.wait_for_timeout(400)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1000); await ev("closeModal()")
        ck('pemukim tabs',await ev("document.querySelectorAll('.lgtabs [data-lt]').length")==2)
        await ev(INJ,'siapa punya bata?'); await pg.wait_for_timeout(400)
        ck('pemukim badge',await ev("document.querySelector('.cbadge').textContent")=='1')
        await pg.click('.lgtabs [data-lt="chat"]'); await pg.wait_for_timeout(200)
        await pg.fill('.chatin input','aku ada 2'); await pg.click('.chatin button'); await pg.wait_for_timeout(400)
        el=await pg.query_selector('details.log'); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
        await pg.screenshot(path='chat_m.png')
        ck('pemukim send',await ev("document.querySelectorAll('.cmsg').length")==2)
        print('errs B',errs)
        # ---------- C. Jualan Yuk online ----------
        await pg.close(); pg,errs=await page(b,390,844); ev=pg.evaluate
        await pg.click('[data-act="hubnew"][data-g="jualan"]'); await pg.wait_for_timeout(900)
        await ev("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push({id:'u_dina',nick:'Dina',team:1});s.v++;await r.set(s);}"""); await pg.wait_for_timeout(500)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        ck('jualan tabs',await ev("document.querySelectorAll('.lgtabs [data-lt]').length")==2, await ev("cur.st.status"))
        await pg.click('.lgtabs [data-lt="chat"]'); await pg.wait_for_timeout(200)
        ck('jualan chat open',await ev("!document.getElementById('chatSlot').hidden&&document.getElementById('chatSlot').closest('details').open"))
        el=await pg.query_selector('.jychat'); await el.scroll_into_view_if_needed(); await pg.screenshot(path='chat_jy.png')
        # hapus meja -> chat ikut dihapus
        g2=await ev("cur.gid"); await ev(INJ,'x'); await pg.wait_for_timeout(300)
        await ev("(async()=>{chatClearGid(cur.gid);})()"); await pg.wait_for_timeout(300)
        ck('clear on delete',await ev(f"!(__RTDB.chat&&__RTDB.chat['{g2}'])"))
        print('errs C',errs)
        # ---------- D. lawan bot: tanpa chat ----------
        await ev("leaveTable()"); await pg.wait_for_timeout(400)
        await ev("startLocalCfg({mode:'klasik',me:'Aku',bots:['Bot A'],level:'easy'})"); await pg.wait_for_timeout(600); await ev("closeModal()")
        ck('no chat in local',await ev("view==='table'&&!!cur.local&&document.querySelectorAll('.lgtabs').length===0&&document.querySelectorAll('details.log').length>0"))
        print('errs D',errs)
        await b.close()
asyncio.run(main())
