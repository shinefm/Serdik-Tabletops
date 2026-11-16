import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.type+': '+m.text[:200]) if m.type in('error','warning') else None)
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/out/index.html'); await pg.wait_for_timeout(6000)
        print('firebase',await pg.evaluate("typeof firebase"),'sdk',await pg.evaluate("firebase.SDK_VERSION"),'online',await pg.evaluate("online"),'claude',await pg.evaluate("typeof claude"))
        print('gate',await pg.evaluate("!!document.querySelector('[data-act=fblogin]')"))
        print('fns',await pg.evaluate("[typeof firebase.auth.GoogleAuthProvider,typeof firebase.firestore().runTransaction,typeof firebase.firestore().batch,typeof firebase.database.ServerValue.TIMESTAMP,typeof firebase.auth().signInWithPopup]"))
        await pg.screenshot(path='real_gate.png')
        for e in errs[:8]: print(e)
        await b.close()
asyncio.run(main())
