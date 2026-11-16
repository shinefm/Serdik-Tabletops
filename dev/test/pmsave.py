import asyncio,json
from playwright.async_api import async_playwright
async def run(url,mock,tag):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        if mock: await pg.add_init_script(path=mock)
        await pg.goto(url); await pg.wait_for_timeout(1500)
        await pg.click('[data-act="pmlocal"]'); await pg.wait_for_timeout(200); await pg.click('[data-act="pmlocalgo"]')
        for k in range(300):
            st=json.loads(await pg.evaluate("JSON.stringify({ph:cur.st.phase,t:cur.st.turn,h:cur.human,r:cur.st.round})"))
            if st['r']>=3 and st['t']==st['h'] and st['ph']=='main':break
            if st['t']==st['h'] or (st['ph']=='discard'):
                await pg.evaluate("(()=>{const s=cur.st,j=cur.human;if(s.phase==='discard'&&!(s.disc&&s.disc[j]))return;pmMove(s.phase==='discard'?pmBotDiscard(s,j):pmBotMove(s,j,'normal'));})()")
            await pg.wait_for_timeout(200)
        before=await pg.evaluate("JSON.stringify({r:cur.st.round,vp:pmVP(cur.st,cur.human,true)})")
        await pg.click('header [data-act="lobby"]') if await pg.query_selector('header [data-act="lobby"]') else await pg.evaluate("leaveTable()")
        await pg.wait_for_timeout(300); print(tag,'leave modal:',(await pg.inner_text('#mbox'))[:160].replace('\n',' / '))
        await pg.click('#mbox [data-act="savequit"]'); await pg.wait_for_timeout(800)
        await pg.evaluate("openProfile()"); await pg.wait_for_timeout(600)
        print(tag,'savecard:',(await pg.inner_text('.savecard'))[:160].replace('\n',' / ') if await pg.query_selector('.savecard') else 'NONE')
        await pg.click('[data-act="resume"]'); await pg.wait_for_timeout(1500)
        after=await pg.evaluate("JSON.stringify({g:cur.st.game,r:cur.st.round,vp:pmVP(cur.st,cur.human,true),board:!!document.querySelector('.pmboard')})")
        print(tag,'before',before,'after',after)
        await pg.evaluate("pmMove({type:'end'})"); await pg.wait_for_timeout(4000)
        print(tag,'bots continued:',await pg.evaluate("JSON.stringify({t:cur.st.turn,h:cur.human,ph:cur.st.phase})"),'errors',errs)
        await b.close()
async def main():
    await run('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html','/home/claude/serdik-tabletops/dev/test/mock.js','LIGA')
    await run('file:///home/claude/pub/latihan/index.html',None,'LATIHAN')
asyncio.run(main())
