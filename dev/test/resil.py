import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.click('#createBtn'); await pg.wait_for_timeout(800)
        gid=await pg.evaluate("cur&&cur.gid"); print('gid',gid, await pg.evaluate("view"))
        # 1. error listener -> badge, auto-reconnect
        await pg.evaluate("globalThis.__failSnap=2; watchTable(cur.gid)")
        await pg.wait_for_timeout(300)
        print('badge',await pg.evaluate("!!document.querySelector('#connBadge')"), 'retry',await pg.evaluate("cur.retry"))
        await pg.screenshot(path='resil_badge.png')
        await pg.wait_for_timeout(5000)
        print('after',await pg.evaluate("view"),await pg.evaluate("!!document.querySelector('#connBadge')"),await pg.evaluate("cur&&cur.retry"))
        # update arrives?
        await pg.evaluate("""async()=>{const r=db.doc('games/'+cur.gid);const s=(await r.get()).data();s.name='Meja X';s.v++;await r.set(s);}""")
        await pg.wait_for_timeout(300); print('name',await pg.evaluate("cur.st.name"))
        # 2. transient missing -> should stay
        await pg.evaluate("globalThis.__goneOnce=1; watchTable(cur.gid)")
        await pg.wait_for_timeout(2500); print('transient gone, view',await pg.evaluate("view"))
        # 3. really deleted -> back to lobby
        await pg.evaluate("db.doc('games/'+cur.gid).delete()")
        await pg.wait_for_timeout(9000); print('deleted, view',await pg.evaluate("view"))
        print('errs',errs)
        await b.close()
asyncio.run(main())
