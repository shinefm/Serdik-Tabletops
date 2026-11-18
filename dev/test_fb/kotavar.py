import asyncio,json,sys
from playwright.async_api import async_playwright
VARS=json.loads(sys.argv[1]); N=int(sys.argv[2]) if len(sys.argv)>2 else 30
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("""()=>{window.solo=(P,N,seed)=>{let tot=0,R=[];const t0=performance.now();let moves=0;for(let g=0;g<N;g++){const k=withSeed(seed+g*7919,()=>{const s={mode:'kota',status:'lobby',players:[newPlayer('A','A'),newPlayer('B','B')],v:1};startGame(s);
            let k=0;while(!s.players[0].kota&&k<60){doMove(s,0,kotaMoveD(s,0,P));doMove(s,1,{type:'pass'});k++;}return k;});R.push(k);moves+=k;}R.sort((a,b)=>a-b);
            return {mean:+(R.reduce((a,b)=>a+b,0)/N).toFixed(2),med:R[N>>1],p10:R[Math.floor(N*.1)],ms:+((performance.now()-t0)/moves).toFixed(1)};};}""")
        for name,v in VARS.items():
            r=await pg.evaluate(f"solo(Object.assign({{}},P_KV,{json.dumps(v)}),{N},1)")
            print(name,r,flush=True)
        print('errs',errs); await b.close()
asyncio.run(main())
