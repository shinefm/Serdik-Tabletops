import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js'); await pg.goto(U); await pg.wait_for_timeout(1500)
        ev=pg.evaluate
        # Klasik: pahlawan
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
        await ev("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        print('overlay at start:',await ev("!!document.querySelector('.awov')"))
        await ev("""(()=>{const st=cur.st,p=st.players[cur.human],id=st.patrons[0],nd=PAT[id].need;for(const c in nd){const ids=TIER_IDS[1].filter(x=>CARDS[x].b===c);for(let k=0;k<nd[c];k++)p.cards.push(ids[k%ids.length]);}render();})()""")
        await pg.wait_for_timeout(300); print('overlay after render only:',await ev("!!document.querySelector('.awov')"))
        await ev("attemptMove({type:'pass'})"); await pg.wait_for_timeout(700)
        print('patron overlay:',await ev("(document.querySelector('.awov')||{}).innerText"))
        await pg.screenshot(path='award_pat.png')
        await pg.wait_for_timeout(3500); print('gone:',not await ev("!!document.querySelector('.awov')"))
        # Kota
        await ev("closeModal&&closeModal()")
        await pg.click('.brand'); await pg.wait_for_timeout(800)
        if await ev("!!document.querySelector('#modal [data-act=\"nosavequit\"]')"): await pg.click('#modal [data-act="nosavequit"]'); await pg.wait_for_timeout(800)
        await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300); await pg.click('[data-act="lpmode"][data-m="kota"]')
        await ev("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(1200); await ev("closeModal()")
        await ev("""(()=>{const st=cur.st,p=st.players[cur.human],K=KOTA[st.cities[0]];const want=Object.assign({},K.need);if(K.same)want.r=K.same;if(K.each)COLORS.forEach(c=>want[c]=Math.max(want[c]||0,1));
          for(const c in want){const ids=TIER_IDS[1].filter(x=>CARDS[x].b===c);for(let k=0;k<want[c];k++)p.cards.push(ids[k%ids.length]);}
          const t3=TIER_IDS[3].filter(x=>CARDS[x].pts>=4);let i=0;while(ptsOf(p)<K.pts)p.cards.push(t3[i++%t3.length]);render();})()""")
        await ev("attemptMove({type:'pass'})"); await pg.wait_for_timeout(600); await pg.screenshot(path='award_kota_mid.png'); await pg.wait_for_timeout(500)
        print('kota overlay:',await ev("(document.querySelector('.awov')||{}).innerText"))
        await pg.screenshot(path='award_kota.png')
        await pg.click('.awov'); await pg.wait_for_timeout(600); print('dismiss on tap:',not await ev("!!document.querySelector('.awov')"))
        print('errs',errs); await b.close()
asyncio.run(main())
