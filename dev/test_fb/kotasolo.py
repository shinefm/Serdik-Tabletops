import asyncio,json,sys
from playwright.async_api import async_playwright
JS=open('/tmp/kotasolo.js').read() if len(sys.argv)>1 else None
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""()=>{
          window.soloRounds=(pol,N,seed0)=>{const R=[];for(let g=0;g<N;g++){const s={mode:'kota',status:'lobby',players:[newPlayer('A','A'),newPlayer('B','B')],v:1};startGame(s);
            let k=0;while(!s.players[0].kota&&k<120){doMove(s,0,pol(s,0));doMove(s,1,{type:'pass'});k++;if(s.status!=='playing')break;}R.push(k);}R.sort((a,b)=>a-b);
            return {mean:+(R.reduce((a,b)=>a+b,0)/N).toFixed(1),med:R[N>>1],p90:R[Math.floor(N*.9)],fail:R.filter(x=>x>=120).length};};
          return {old:soloRounds((s,t)=>botMove(s,t,'hard',BOT_HARD),60),v2:soloRounds((s,t)=>kotaMove2(s,t,P_KV),60),v3:soloRounds((s,t)=>kotaMove3(s,t,P_KV),60),d2:soloRounds((s,t)=>kotaMoveD(s,t,P_KV),60),d3:(()=>{const t0=performance.now();const r=soloRounds((s,t)=>kotaMoveD(s,t,Object.assign({},P_KV,{depth:3,beam:5,beam2:4})),40);r.msPerMove=+((performance.now()-t0)/(r.mean*40)).toFixed(1);return r;})()};}""")
        for k,v in r.items(): print(k,v)
        print('errs',errs); await b.close()
asyncio.run(main())
