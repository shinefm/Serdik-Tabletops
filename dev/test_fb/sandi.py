import asyncio,json
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js'); await pg.goto(U); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        async def as_(uid,js): return await ev(f"(async()=>{{myId='{uid}';try{{await commitOnline(s=>{js});return 'ok'}}catch(e){{return e.message}}finally{{myId='u_me';render()}}}})()")
        print('card btns',await ev("[...document.querySelectorAll('.hubcard')].filter(c=>c.textContent.includes('Sandi')).map(c=>[...c.querySelectorAll('button')].map(b=>b.textContent.trim()))"))
        await pg.click('[data-act="hubnew"][data-g="sandi"]'); await pg.wait_for_timeout(800)
        print('created',await ev("JSON.stringify({g:cur.st.game,t:cur.st.timer,pk:cur.st.pack,p:cur.st.players})"))
        for uid,nick in [('u_dina','Dina'),('u_raka','Raka'),('u_sari','Sari')]:
            await as_(uid,"(()=>{})()")  # noop
            await ev(f"(async()=>{{myId='{uid}';ui.nick='{nick}';await tableAction('join');myId='u_me';ui.nick='Farhan';render()}})()"); await pg.wait_for_timeout(400)
        print('teams',await ev("JSON.stringify(cur.st.players.map(p=>[p.id,p.team,!!p.ketua]))"))
        await ev("(async()=>{myId='u_raka';ui.sdKVal=cur.st.players.findIndex(p=>p.id==='u_raka');await tableAction('sdketua');myId='u_me';render()})()"); await pg.wait_for_timeout(400)
        await pg.select_option('#sdPack','MK02'); await pg.wait_for_timeout(500)
        print('after ketua/pack',await ev("JSON.stringify({p:cur.st.players.map(p=>[p.id,p.team,!!p.ketua]),pk:cur.st.pack})"))
        await pg.screenshot(path='sd_lobby.png',full_page=True)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='sd_role.png'); await ev("closeModal()")
        st=json.loads(await ev("JSON.stringify({T:cur.st.turnTeam,ph:cur.st.phase,p:cur.st.players.map(p=>[p.id,p.team,!!p.ketua]),mk:[...new Set(cur.st.words.map(w=>w.mk))]})")); print(st)
        T=st['T']; me=[x for x in st['p'] if x[0]=='u_me'][0]
        kt=[x[0] for x in st['p'] if x[1]==T and x[2]][0]; gs=[x[0] for x in st['p'] if x[1]==T and not x[2]][0]
        ok=[x[0] for x in st['p'] if x[1]!=T and x[2]][0]; og=[x[0] for x in st['p'] if x[1]!=T and not x[2]][0]
        print('turn team',T,'ketua',kt,'guesser',gs,'me',me)
        w0=await ev("termOf(cur.st.words[0]).w")
        print('bad clue (board word):',await as_(kt,f"hubAct(s,meIdx(s),{{type:'clue',word:'{w0}',num:1}})"))
        # ketua view screenshot
        await ev(f"myId='{kt}';render()"); await pg.wait_for_timeout(300); await ev("closeModal()")
        await pg.fill('#sdW','Investasi'); await pg.select_option('#sdN','2'); await pg.screenshot(path='sd_ketua.png',full_page=True)
        await pg.click('[data-act="sdclue"]'); await pg.wait_for_timeout(800)
        print('clue',await ev("JSON.stringify([cur.st.phase,cur.st.clue,cur.st.left])"))
        await ev("myId='u_me';render()")
        # guesser: correct card via UI
        key=await ev("sandiKey(cur.st)")
        mine=[i for i,c in enumerate(key) if c==T]; neutral=[i for i,c in enumerate(key) if c=='n']
        await ev(f"myId='{gs}';render()"); await pg.wait_for_timeout(300); await ev("closeModal()")
        await pg.click(f'.sdcard[data-i="{mine[0]}"]'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='sd_guess_sel.png',full_page=True)
        await pg.click('[data-act="sdguess"]'); await pg.wait_for_timeout(800)
        print('after correct',await ev("JSON.stringify([cur.st.phase,cur.st.left,cur.st.turnTeam,cur.st.rev.filter(Boolean).length])"))
        await pg.click(f'.sdcard[data-i="{neutral[0]}"]'); await pg.wait_for_timeout(150); await pg.click(f'.sdcard[data-i="{neutral[0]}"]'); await pg.wait_for_timeout(800)
        print('after neutral (double tap)',await ev("JSON.stringify([cur.st.phase,cur.st.turnTeam])"))
        await ev("myId='u_me';render()"); await pg.wait_for_timeout(300)
        # host menu
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.screenshot(path='sd_host.png')
        print('host btns',await ev("[...document.querySelectorAll('#modal button')].map(b=>b.textContent.trim())"))
        await pg.click('#modal [data-act="hskip"]'); await pg.wait_for_timeout(800)
        print('after host skip',await ev("JSON.stringify([cur.st.phase,cur.st.turnTeam,cur.st.log.slice(-1)[0].m])"))
        T=await ev("cur.st.turnTeam")
        newk=await ev(f"cur.st.players.findIndex(p=>p.team==='{T}'&&!p.ketua)")
        await pg.click('#hostBtn'); await pg.wait_for_timeout(300); await pg.click(f'#modal [data-act="sdhk"][data-i="{newk}"]'); await pg.wait_for_timeout(800)
        print('ketua changed',await ev("JSON.stringify(cur.st.players.map(p=>[p.id,p.team,!!p.ketua]))"))
        # play to the end: current team clue then open audit card -> lose
        kt=await ev(f"cur.st.players.find(p=>p.team==='{T}'&&p.ketua).id"); gs=await ev(f"cur.st.players.find(p=>p.team==='{T}'&&!p.ketua).id")
        print('clue2',await as_(kt,"hubAct(s,meIdx(s),{type:'clue',word:'Modal',num:3})"))
        x=key.index('x')
        print('audit',await as_(gs,f"hubAct(s,meIdx(s),{{type:'guess',i:{x}}})")); await pg.wait_for_timeout(1500)
        print('ended',await ev("JSON.stringify([cur.st.status,cur.st.winner,cur.st.winBy])"))
        await pg.screenshot(path='sd_end.png')
        await ev("closeModal()"); await pg.wait_for_timeout(300); await pg.screenshot(path='sd_board_end.png',full_page=True)
        await pg.click(f'.sdcard[data-i="{x}"]'); await pg.wait_for_timeout(300)
        print('info',(await ev("$('#modal').textContent"))[:160])
        print('rules',(await ev("(openTutorial('sandi'),$('#modal').textContent.slice(0,120))")))
        print('errs',errs)
        await b.close()
asyncio.run(main())
