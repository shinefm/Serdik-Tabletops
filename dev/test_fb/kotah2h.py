import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""()=>{
          const pol={old:(s,t)=>botMove(s,t,'hard',BOT_HARD),hard:(s,t)=>kotaMoveD(s,t,P_KV),normal:(s,t)=>kotaMoveD(s,t,P_KV_N)};
          function play(names){const s={mode:'kota',status:'lobby',players:names.map((x,i)=>Object.assign(newPlayer('B'+i,x),{bot:true})),v:1};
            startGame(s);let k=0;while(s.status==='playing'&&k<900){const t=s.turn;try{doMove(s,t,pol[names[t]](s,t));}catch(e){doMove(s,t,{type:'pass'});}k++;}
            const r=ranking(s);return {win:names[r[0].i],rounds:s.round};}
          const out={};
          for(const [a,bb,N] of [['hard','old',24],['hard','normal',24]])for(const n of [2,3,4]){
            const w={},R=[];for(let g=0;g<N;g++){const names=[];for(let i=0;i<n;i++)names.push(i===(g%n)?a:bb);const res=play(names);w[res.win]=(w[res.win]||0)+1;R.push(res.rounds);}
            out[a+' vs '+bb+' '+n+'p']={winA:+((w[a]||0)/N).toFixed(2),fair:+(1/n).toFixed(2),rounds:+(R.reduce((x,y)=>x+y,0)/N).toFixed(1)};}
          for(const x of ['old','normal','hard']){const R=[];for(let g=0;g<16;g++)R.push(play([x,x,x]).rounds);out['self '+x+' 3p rounds']=+(R.reduce((a,b)=>a+b,0)/16).toFixed(1);}
          return out;}""")
        for k,v in r.items(): print(k,v)
        print('errs',errs); await b.close()
asyncio.run(main())
