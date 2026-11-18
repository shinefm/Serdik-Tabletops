import asyncio,json,sys
from playwright.async_api import async_playwright
V=sys.argv[1] if len(sys.argv)>1 else '{}'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""(V)=>{const P=Object.assign({},P_KV,V);const out=[];for(let g=0;g<30;g++){out.push(withSeed(1+g*7919,()=>{const s={mode:'kota',status:'lobby',players:[newPlayer('A','A'),newPlayer('B','B')],v:1};startGame(s);
            let k=0,takes=0,buys=0,res=0;while(!s.players[0].kota&&k<60){const mv=kotaMoveD(s,0,P);if(mv.type==='take')takes++;if(mv.type==='buy')buys++;if(mv.type==='reserve')res++;doMove(s,0,mv);doMove(s,1,{type:'pass'});k++;}
            const p=s.players[0];const t={1:0,2:0,3:0};p.cards.forEach(id=>t[CARDS[id].tier]++);return {k,city:p.kota&&KOTA[p.kota].name,pts:ptsOf(p),cards:p.cards.length,t1:t[1],t2:t[2],t3:t[3],takes,buys,res};}));}
          const avg=f=>+(out.reduce((a,x)=>a+x[f],0)/out.length).toFixed(1);
          return {rounds:avg('k'),pts:avg('pts'),cards:avg('cards'),t1:avg('t1'),t2:avg('t2'),t3:avg('t3'),takes:avg('takes'),buys:avg('buys'),res:avg('res'),cities:out.map(x=>x.city).join(',')};}""",json.loads(V))
        print(r); print('errs',errs); await b.close()
asyncio.run(main())
