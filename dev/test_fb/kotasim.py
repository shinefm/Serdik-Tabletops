import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""()=>{const out=[];
          for(const [n,lv] of [[2,'normal'],[3,'normal'],[4,'normal'],[2,'hard'],[3,'hard'],[4,'hard'],[3,'easy']])for(let g=0;g<25;g++){
            const s={mode:'kota',status:'lobby',players:Array.from({length:n},(_,i)=>Object.assign(newPlayer('B'+i,'Bot'+i),{bot:true})),v:1};
            startGame(s);let steps=0;
            while(s.status==='playing'&&steps<800){const t=s.turn;let mv;try{mv=lv==='hard'?hardBotMove(s,t,null):botMove(s,t,lv);doMove(s,t,mv);}catch(e){doMove(s,t,{type:'pass'});}steps++;}
            const r=ranking(s);out.push({n,lv,ended:s.status==='ended',rounds:s.round,cities:s.players.filter(p=>p.kota).length,win:r[0].k,winPts:r[0].pts,winBy:s.winBy||''});}
          return out;}""")
        import collections
        g=collections.defaultdict(list)
        for x in r: g[(x['n'],x['lv'])].append(x)
        for k,v in g.items():
            print(k,'ended',sum(x['ended'] for x in v),'/',len(v),'avg rounds',round(sum(x['rounds'] for x in v)/len(v),1),'max',max(x['rounds'] for x in v),'winner has city',sum(x['win'] for x in v),'avg cities',round(sum(x['cities'] for x in v)/len(v),2),'winPts',round(sum(x['winPts'] for x in v)/len(v),1))
        print([x['winBy'] for x in r[:6]],'errs',errs)
        await b.close()
asyncio.run(main())
