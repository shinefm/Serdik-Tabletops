import asyncio,json,sys,time
from playwright.async_api import async_playwright
ITER=int(sys.argv[1]) if len(sys.argv)>1 else 30
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("""()=>{window.solo=(P,N,seed)=>{let tot=0;for(let g=0;g<N;g++){tot+=withSeed(seed+g*7919,()=>{const s={mode:'kota',status:'lobby',players:[newPlayer('A','A'),newPlayer('B','B')],v:1};startGame(s);
            let k=0;while(!s.players[0].kota&&k<60){doMove(s,0,kotaMove2(s,0,P));doMove(s,1,{type:'pass'});k++;}return k;});}return tot/N;};}""")
        t=time.time(); base=await pg.evaluate("solo(P_KV,24,1)"); print('base',base,'t',round(time.time()-t,1),flush=True)
        best=json.loads(await pg.evaluate("JSON.stringify(P_KV)")); bestv=base
        import random; random.seed(3)
        keys=['gam','wB','wBd','wPts','wE','wE2','tx','tok','gold','resPen','ptsPer']
        for it in range(ITER):
            cand=dict(best)
            for k in random.sample(keys,3): cand[k]=round(max(0.0,cand[k]*random.choice([0.6,0.8,1.25,1.5])+random.uniform(-0.05,0.05)),3)
            v=await pg.evaluate(f"solo({json.dumps(cand)},24,1)")
            if v<bestv:
                v2=await pg.evaluate(f"solo({json.dumps(cand)},24,500)"); vb2=await pg.evaluate(f"solo({json.dumps(best)},24,500)")
                if v2<=vb2: best,bestv=cand,v; print(it,'improved',v,v2,json.dumps(best),flush=True)
        print('FINAL',bestv,json.dumps(best)); print('errs',errs); await b.close()
asyncio.run(main())
