import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""()=>{let single=0,blocked=0,multi=0,none=0;const ex=[];
          for(let g=0;g<40;g++){const s={mode:'kota',status:'lobby',players:[newPlayer('B','Bot'),newPlayer('H','Human')],v:1};startGame(s);
            s.cities=['bdg','jkt','sby'];
            const H=s.players[1];H.cards=['1g0','1g1','1g2','1u0','1u1','3k1','3w1','3r0'];
            const card=TIER_IDS[2].find(id=>CARDS[id].b==='u'&&CARDS[id].pts>=1);
            s.market.t2[1]=card;H.t=emptyTok();for(const c of COLORS)H.t[c]=Math.min(7,(CARDS[card].cost[c]||0));
            s.players[0].t={w:1,u:1,g:1,r:1,k:1,y:0};s.turn=0;
            const all=kotaThreats(s,0),th=kotaThreat(s,0);const mv=hardBotMove(s,0,null);
            if(!all.length)none++;else if(!th)multi++;else{single++;if((mv.type==='buy'||mv.type==='reserve')&&mv.tier===th.tier&&mv.slot===th.slot)blocked++;else ex.push(JSON.stringify(mv));}}
          return {single,blocked,multi,none,ex:ex.slice(0,3)};}""")
        print(r); print('errs',errs); await b.close()
asyncio.run(main())
