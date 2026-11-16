import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1200,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("c0delay=()=>20")
        res={}
        for mode,n,ord_ in [('klasik','3','2'),('klasik','2','0'),('duel',None,'1'),('klasik','3','random'),('klasik','3','random'),('klasik','3','random'),('duel',None,'random')]:
            await pg.evaluate("closeModal()"); await pg.click('[data-act="localSetup"]')
            await pg.click(f'[data-act="lpmode"][data-m="{mode}"]')
            if n: await pg.select_option('#lpN',n)
            opts=await pg.evaluate("[...document.querySelectorAll('#lpOrd option')].map(o=>o.textContent)")
            await pg.select_option('#lpOrd',ord_); await pg.select_option('#lpLv','easy')
            await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(300)
            r=await pg.evaluate("({h:cur.human,np:cur.st.players.length,first:cur.st.log.slice(-1)[0].m,botsMoved:cur.st.log.length})")
            # play out quickly
            fin=await pg.evaluate("""async()=>{let g=0;while(cur.st.status==='playing'&&g++<800){if(cur.st.turn===cur.human&&!ui.busy){await runMove(cur.st.mode==='duel'?duelBotMove(cur.st,cur.human,'normal'):botMove(cur.st,cur.human,'normal'));}await new Promise(r=>setTimeout(r,8));}return cur.st.status;}""")
            print(mode,n,ord_,'options',opts,'->',r,fin)
            await pg.click('[data-act="lobby"]'); await pg.wait_for_timeout(200)
        # online host order setting
        await pg.fill('#tblIn','Meja'); await pg.click('[data-act="create"]'); await pg.wait_for_timeout(500)
        await pg.select_option('#ordSel','seat'); await pg.wait_for_timeout(500)
        print('online order saved:',await pg.evaluate("cur.st.order"))
        await pg.evaluate("(async()=>{const ref=db.doc('games/'+cur.gid);const s=(await ref.get()).data();s.players.push(newPlayer('u_b','Dina'),newPlayer('u_c','Raka'));s.v++;await ref.set(s);})()"); await pg.wait_for_timeout(400)
        await pg.click('[data-act="start"]'); await pg.wait_for_timeout(500)
        print('seat order:',await pg.evaluate("cur.st.players.map(p=>p.id).join(',')+' | '+cur.st.log.slice(-1)[0].m"))
        print('errs',errs); await b.close()
asyncio.run(main())
