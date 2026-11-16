import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for mode in ['klasik','duel']:
            pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js'); await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
            cdp=await pg.context.new_cdp_session(pg); await cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
            await pg.evaluate("c0delay=()=>50")
            await pg.click('[data-act="localSetup"]'); await pg.wait_for_timeout(300)
            if mode=='duel': await pg.click('[data-act="lpmode"][data-m="duel"]')
            else: await pg.select_option('#lpN','3')
            await pg.select_option('#lpLv','hard'); await pg.evaluate("document.querySelector('#lpOrd').value='0'"); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(500)
            await pg.evaluate("""(()=>{window.__bt=[];const H=hardBotMove,D=duelBotMove;window.hardBotMove=function(){const t=performance.now();const r=H.apply(this,arguments);__bt.push(performance.now()-t);return r};
              window.duelBotMove=function(s,pi,l){const t=performance.now();const r=D.apply(this,arguments);if(l==='hard')__bt.push(performance.now()-t);return r};})()""")
            for k in range(60):
                if await pg.evaluate("cur.st.status")!='playing' or await pg.evaluate("cur.st.round")>=8: break
                if await pg.evaluate("cur.st.turn===cur.human"): await pg.evaluate("(async()=>{await runMove({type:'pass'});})()")
                await pg.wait_for_timeout(300)
            bt=await pg.evaluate("__bt")
            print(mode,'hard moves',len(bt),'avg ms',round(sum(bt)/max(1,len(bt))),'max ms',round(max(bt or [0])),'round',await pg.evaluate("cur.st.round"),errs)
        await b.close()
asyncio.run(main())
