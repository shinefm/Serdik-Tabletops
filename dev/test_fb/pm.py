import asyncio,json,sys
from playwright.async_api import async_playwright
W=int(sys.argv[1]) if len(sys.argv)>1 else 1300
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':W,'height':950 if W>500 else 844},device_scale_factor=1 if W>500 else 2)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'pm{W}_lobby.png',full_page=True)
        await pg.click('[data-act="pmlocal"]'); await pg.wait_for_timeout(300)
        await pg.select_option('#pmN','3'); await pg.select_option('#pmOrd','1')
        await pg.screenshot(path=f'pm{W}_setupmodal.png')
        await pg.click('[data-act="pmlocalgo"]'); await pg.wait_for_timeout(800)
        # wait until my setup turn
        for k in range(40):
            if await pg.query_selector(".pmhit"): break
            await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'pm{W}_setup.png',full_page=True)
        # human setup via clicks (choose best by bot logic)
        for k in range(200):
            st=json.loads(await pg.evaluate("JSON.stringify({ph:cur.st.phase,turn:cur.st.turn,h:cur.human,st:cur.st.status,need:cur.st.setup&&cur.st.setup.need})"))
            if st['ph']!='setup':break
            if st['turn']==st['h']:
                mv=json.loads(await pg.evaluate("JSON.stringify(pmBotMove(cur.st,cur.human,'normal'))"))
                if mv['type']=='settle': await pg.click(f'circle.pmhit[data-v="{mv["v"]}"]',force=True)
                else: await pg.click(f'line.pmhit[data-e="{mv["e"]}"]',force=True)
            await pg.wait_for_timeout(250)
        print('after setup',await pg.evaluate("JSON.stringify({ph:cur.st.phase,res:cur.st.players[cur.human].res})"))
        shots=set(); turns=0
        for k in range(3000):
            st=json.loads(await pg.evaluate("JSON.stringify({ph:cur.st.phase,turn:cur.st.turn,h:cur.human,st:cur.st.status,disc:cur.st.disc||null,offer:!!cur.st.offer,round:cur.st.round})"))
            if st['st']!='playing':break
            h=st['h']
            if st['ph']=='discard' and st['disc'] and str(h) in st['disc']:
                await pg.wait_for_timeout(200)
                if 'discard' not in shots: await pg.screenshot(path=f'pm{W}_discard.png'); shots.add('discard')
                mv=json.loads(await pg.evaluate("JSON.stringify(pmBotDiscard(cur.st,cur.human))"))
                for r,c in mv['res'].items():
                    for _ in range(c): await pg.click(f'#mbox [data-act="pmdd"][data-r="{r}"][data-d="1"]')
                await pg.click('#mbox [data-act="pmdiscok"]'); await pg.wait_for_timeout(200); continue
            if st['turn']==h and st['ph']!='discard':
                if st['ph']=='roll':
                    await pg.click('[data-act="pmroll"]'); turns+=1
                elif st['ph']=='main':
                    if turns==3 and 'trade' not in shots:
                        await pg.click('[data-act="pmtrade"]'); await pg.wait_for_timeout(150); await pg.screenshot(path=f'pm{W}_trade.png'); shots.add('trade')
                        await pg.click('#mbox [data-act="pmtrade"][data-t="pl"]'); await pg.wait_for_timeout(100)
                        # offer: give 1 of what I have most, get 1 of what I have least
                        res=json.loads(await pg.evaluate("JSON.stringify(cur.st.players[cur.human].res)"))
                        give=max(res,key=lambda r:res[r]); get=min(res,key=lambda r:res[r])
                        if res[give]>0 and give!=get:
                            await pg.click(f'#mbox [data-act="pmo"][data-k="og"][data-r="{give}"][data-d="1"]'); await pg.click(f'#mbox [data-act="pmo"][data-k="ot"][data-r="{get}"][data-d="1"]')
                            await pg.screenshot(path=f'pm{W}_offer.png'); await pg.click('#mbox [data-act="pmoffer"]'); await pg.wait_for_timeout(2500)
                            await pg.screenshot(path=f'pm{W}_offerresp.png',full_page=True)
                            acc=await pg.query_selector('[data-act="pmaccept"]')
                            if acc: await acc.click(); print('trade accepted')
                            elif await pg.query_selector('[data-act="pmcancel"]'): await pg.click('[data-act="pmcancel"]')
                            await pg.wait_for_timeout(300)
                        else: await pg.click('#mbox [data-act="close"]')
                        continue
                    mv=json.loads(await pg.evaluate("JSON.stringify(pmBotMove(cur.st,cur.human,'normal'))"))
                    t=mv['type']
                    if t=='build':
                        await pg.click(f'[data-act="pmmode"][data-w="{mv["what"]}"]'); await pg.wait_for_timeout(120)
                        if mv['what'] not in shots: await pg.screenshot(path=f'pm{W}_mode_{mv["what"]}.png',full_page=True); shots.add(mv['what'])
                        sel=f'line.pmhit[data-e="{mv["e"]}"]' if mv['what']=='road' else f'circle.pmhit[data-v="{mv["v"]}"]'
                        await pg.click(sel,force=True)
                    elif t=='end': await pg.click('[data-act="pmend"]')
                    elif t=='buydev': await pg.click('[data-act="pmbuydev"]')
                    elif t=='bank': await pg.evaluate(f"pmMove({json.dumps(mv)})")
                    elif t=='dev':
                        await pg.evaluate(f"pmMove({json.dumps(mv)})")
                    elif t=='cancel': await pg.evaluate("pmMove({type:'cancel'})")
                    else: await pg.evaluate(f"pmMove({json.dumps(mv)})")
                elif st['ph']=='robber':
                    if 'robber' not in shots: await pg.screenshot(path=f'pm{W}_robber.png',full_page=True); shots.add('robber')
                    mv=json.loads(await pg.evaluate("JSON.stringify(pmBotRobber(cur.st,cur.human,'normal'))"))
                    await pg.click(f'polygon.pmhl[data-h="{mv["h"]}"]',force=True); await pg.wait_for_timeout(150)
                    if await pg.query_selector('#mbox [data-act="pmrobv"]'): await pg.click('#mbox [data-act="pmrobv"]')
                elif st['ph']=='freeroad':
                    await pg.evaluate("pmMove(pmBotMove(cur.st,cur.human,'normal'))")
                elif st['ph']=='steal':
                    await pg.click('[data-act="pmsteal"]')
                await pg.wait_for_timeout(120)
            else:
                await pg.wait_for_timeout(250)
            if st['round']==6 and 'mid' not in shots: await pg.screenshot(path=f'pm{W}_mid.png',full_page=True); shots.add('mid')
        await pg.wait_for_timeout(1500)
        print('status',await pg.evaluate("JSON.stringify({s:cur.st.status,w:cur.st.winner,h:cur.human,r:cur.st.round,vp:cur.st.players.map((p,i)=>pmVP(cur.st,i,true))})"))
        await pg.screenshot(path=f'pm{W}_end.png',full_page=True)
        await pg.wait_for_timeout(800)
        print('stats',await pg.evaluate("JSON.stringify(__store['stats/u_me']&&__store['stats/u_me'].rec)"))
        print('errors',errs); await b.close()
asyncio.run(main())
