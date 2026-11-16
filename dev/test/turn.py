import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for W,H,tag in [(390,844,'m'),(1280,860,'d')]:
            pg=await b.new_page(viewport={'width':W,'height':H},device_scale_factor=2 if tag=='m' else 1)
            errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
            await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
            await pg.click('#createBtn'); await pg.wait_for_timeout(800)
            await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push(newPlayer('u_dina','Dina'),newPlayer('u_budi','Budi'));s.timer=0;s.v++;await r.set(s);}""")
            await pg.wait_for_timeout(400); await pg.click('[data-act="start"]'); await pg.wait_for_timeout(5000)
            ids=json.loads(await pg.evaluate("JSON.stringify(cur.st.players.map(p=>p.id))")); me=ids.index('u_me'); d=ids.index('u_dina')
            async def setst(js):
                await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();"""+js+""";s.v++;await r.set(s);}""")
            print('pre',await pg.evaluate("JSON.stringify({v:view,has:!!(cur&&cur.st),app:$('#app').textContent.slice(0,40)})"))
            await setst(f"s.turn={d};s.round=2;s.turnAt=Date.now()"); await pg.wait_for_timeout(500)
            print('post',await pg.evaluate("JSON.stringify({v:view,has:!!(cur&&cur.st),app:$('#app').textContent.slice(0,40)})"))
            await pg.screenshot(path=f'turn_oth_{tag}.png')
            await setst(f"s.turn={me};s.turnAt=Date.now()"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'turn_me_{tag}.png')
            print(tag,'body',await pg.evaluate("document.body.className"),'ordn',await pg.evaluate("document.querySelectorAll('.ordn').length"),errs)
            await pg.close()
        # 2-player AFK rule
        pg=await b.new_page(viewport={'width':390,'height':844})
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.click('#createBtn'); await pg.wait_for_timeout(800)
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.players.push(newPlayer('u_dina','Dina'));s.timer=0;s.v++;await r.set(s);}""")
        await pg.wait_for_timeout(400); await pg.click('[data-act="start"]'); await pg.wait_for_timeout(1200)
        d=await pg.evaluate("cur.st.players.findIndex(p=>p.id==='u_dina')")
        tr=lambda js: pg.evaluate(f"(async()=>{{try{{await commitOnline(s=>{{{js}}});return 'ok '+JSON.stringify(cur.st.afk&&cur.st.afk.stage)}}catch(e){{return e.message}}}})()")
        print('2p early:',await tr(f"s.turn={d};s.turnAt=Date.now()-30000;afkReport(s,meIdx(s),{d})"))
        print('2p late:',await tr(f"s.turn={d};s.turnAt=Date.now()-130000;afkReport(s,meIdx(s),{d})"))
        await b.close()
asyncio.run(main())
