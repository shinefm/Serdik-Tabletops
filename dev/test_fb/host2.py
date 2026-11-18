import asyncio,json
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
async def newpg(b):
    pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js'); await pg.goto(U); await pg.wait_for_timeout(1500); return pg,errs
async def addp(pg,js):
    await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();"""+js+""";s.v++;await r.set(s);}"""); await pg.wait_for_timeout(600)
async def ev(pg,js): return await pg.evaluate(js)
async def try_(pg,uid,js): return await pg.evaluate(f"(async()=>{{myId='{uid}';try{{await commitOnline(s=>{js});return 'ok'}}catch(e){{return e.message}}finally{{myId='u_me';render()}}}})()")
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        # ---------- RAPAT ----------
        pg,errs=await newpg(b)
        await pg.click('[data-act="hubnew"][data-g="rapat"]'); await pg.wait_for_timeout(600)
        await addp(pg,"['Dina','Raka','Sari','Bima'].forEach(n=>s.players.push({id:'u_'+n.toLowerCase(),nick:n}))")
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200); await ev(pg,"closeModal()")
        print('R btn',await ev(pg,"$('#hostBtn').style.display!=='none'"),'phase',await ev(pg,"cur.st.phase"),'pend',await ev(pg,"rapatPending(cur.st)"),'me',await ev(pg,"meIdx(cur.st)"))
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.screenshot(path='h2_rapat_modal.png')
        await pg.click('#modal [data-act="hpause"]'); await pg.wait_for_timeout(800)
        print('R paused bar',await ev(pg,"($('#afkBar')||{}).textContent"))
        print('R act while paused',await try_(pg,'u_dina',"hubAct(s,meIdx(s),{type:'vote',yes:true})"))
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="hresume"]'); await pg.wait_for_timeout(800)
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="hskip"]'); await pg.wait_for_timeout(900)
        print('R after skip phase',await ev(pg,"cur.st.phase"),'pend',await ev(pg,"rapatPending(cur.st)"))
        me=await ev(pg,"meIdx(cur.st)")
        others=await ev(pg,f"cur.st.players.map((p,i)=>i).filter(i=>i!=={me})")
        for i in others:
            await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click(f'#modal [data-act="hbot"][data-i="{i}"]'); await pg.wait_for_timeout(700)
        print('R auto',await ev(pg,"cur.st.players.map(p=>!!p.auto)"),'phase',await ev(pg,"cur.st.phase"),'pend',await ev(pg,"rapatPending(cur.st)"))
        if await ev(pg,"cur.st.phase")=='vote' and me in await ev(pg,"rapatPending(cur.st)"):
            await ev(pg,"(async()=>{await commitOnline(s=>hubAct(s,meIdx(s),{type:'vote',yes:true}))})()"); await pg.wait_for_timeout(2600)
        print('R after my vote phase',await ev(pg,"cur.st.phase"),'mi',await ev(pg,"cur.st.mi"),'log',await ev(pg,"cur.st.log.slice(-3).map(l=>l.m)"))
        print('dina bar',await ev(pg,"(myId='u_dina',render(),afkTick(),$('#afkBar').textContent)")); await ev(pg,"myId='u_me';render()")
        print('R errs',errs)
        # ---------- WEREWOLF ----------
        pg,errs=await newpg(b)
        await pg.click('[data-act="hubnew"][data-g="werewolf"]'); await pg.wait_for_timeout(600)
        await addp(pg,"['Dina','Raka'].forEach(n=>s.players.push({id:'u_'+n.toLowerCase(),nick:n}))")
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200); await ev(pg,"closeModal()")
        print('W phase',await ev(pg,"cur.st.phase"),'btn',await ev(pg,"$('#hostBtn').style.display!=='none'"))
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="hskip"]'); await pg.wait_for_timeout(900)
        print('W after skip',await ev(pg,"cur.st.phase"))
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="hskip"]'); await pg.wait_for_timeout(900)
        print('W after skip2',await ev(pg,"cur.st.phase"),await ev(pg,"cur.st.status"),'errs',errs)
        # ---------- JUALAN ----------
        pg,errs=await newpg(b)
        await pg.click('[data-act="hubnew"][data-g="jualan"]'); await pg.wait_for_timeout(900)
        await addp(pg,"s.players.push({id:'u_dina',nick:'Dina',team:1})")
        print('J players',await ev(pg,"JSON.stringify(cur.st.players.map(p=>[p.id,p.team]))"))
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200); await ev(pg,"closeModal()")
        print('J teams',await ev(pg,"JSON.stringify(cur.st.teams.map(T=>[T.name,T.members,T.bot]))"),'btn',await ev(pg,"$('#hostBtn').style.display!=='none'"))
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.screenshot(path='h2_jy_modal.png')
        await pg.click('#modal [data-act="hpause"]'); await pg.wait_for_timeout(800)
        print('J dina ready while paused',await try_(pg,'u_dina',"hubAct(s,meIdx(s),{type:'ready'})"))
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="hresume"]'); await pg.wait_for_timeout(800)
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="htbot"][data-i="1"]'); await pg.wait_for_timeout(2500)
        print('J team1 auto',await ev(pg,"cur.st.teams[1].auto"),'step',await ev(pg,"cur.st.teams.map(T=>T.step)"))
        print('J dina act on auto team',await try_(pg,'u_dina',"hubAct(s,meIdx(s),{type:'draft',d:{H:1}})"))
        print('dina bar',await ev(pg,"(myId='u_dina',render(),afkTick(),$('#afkBar').textContent)")); await ev(pg,"myId='u_me';render()")
        print('J dina takes over',await try_(pg,'u_dina',"afkHere(s,meIdx(s))"),await ev(pg,"[cur.st.teams[1].auto,cur.st.players.map(p=>!!p.auto)]"))
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="htbot"][data-i="1"]'); await pg.wait_for_timeout(600)
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="hskip"]'); await pg.wait_for_timeout(2500)
        print('J after skip phase',await ev(pg,"cur.st.phase"),'round',await ev(pg,"cur.st.round"))
        for k in range(30):
            if await ev(pg,"cur.st.phase")!='sell': break
            if await ev(pg,"jyPending(cur.st).includes(meIdx(cur.st))"): await try_(pg,'u_me',"hubAct(s,meIdx(s),{type:'stop'})")
            await pg.wait_for_timeout(900)
        print('J later phase',await ev(pg,"cur.st.phase"),'round',await ev(pg,"cur.st.round"),'log',await ev(pg,"cur.st.log.slice(-2).map(l=>l.m)"),'errs',errs)
        await b.close()
asyncio.run(main())
