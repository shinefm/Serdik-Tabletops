import asyncio
from playwright.async_api import async_playwright
async def run(b,vw,tag,mode):
    ctx=await b.new_context(viewport={'width':vw[0],'height':vw[1]},device_scale_factor=1 if vw[0]>800 else 2)
    pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
    await pg.add_init_script(script=f"try{{localStorage.setItem('sp_mode','{mode}')}}catch(e){{}}")
    await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1200)
    await pg.evaluate("c0delay=()=>15")
    await pg.click('[data-act="localSetup"]'); await pg.click('[data-act="lpmode"][data-m="duel"]'); await pg.select_option('#lpLv','hard'); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
    # human: select a valid line by clicking cells
    cells=await pg.evaluate("(()=>{for(const L of DLINES){if(L.length===3&&L.every(i=>cur.st.board[i]&&cur.st.board[i]!=='y'))return L;}})()")
    for c in cells: await pg.click(f'.dcell[data-i="{c}"]')
    await pg.screenshot(path=f'duel_{tag}_sel.png',full_page=True)
    await pg.click('[data-act="dtake"]'); await pg.wait_for_timeout(500)
    await pg.screenshot(path=f'duel_{tag}.png',full_page=True)
    r=await pg.evaluate("""async()=>{let g=0;while(cur.st.status==='playing'&&g++<600){if(cur.st.turn===cur.human&&!ui.busy){await runMove(duelBotMove(cur.st,cur.human,'normal'));}await new Promise(r=>setTimeout(r,20));}await new Promise(r=>setTimeout(r,500));
       const k=Object.keys(__store).find(x=>x.startsWith('results/'));return {st:cur.st.status,by:cur.st.winBy,winner:cur.st.winner,round:cur.st.round,res:k&&__store[k].variant};}""")
    await pg.screenshot(path=f'duel_{tag}_end.png')
    print(tag,r,errs); await ctx.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        await run(b,(1366,900),'desk','dark')
        await run(b,(390,844),'mob','light')
        await b.close()
asyncio.run(main())
