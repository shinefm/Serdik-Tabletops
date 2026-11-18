import asyncio,json,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""()=>{
          const pol={old:(s,t)=>botMove(s,t,'hard',BOT_HARD),hard:(s,t)=>kotaMove(s,t,P_KOTA),normal:(s,t)=>kotaMove(s,t,P_KOTA_N)};
          function play(names){const n=names.length;const s={mode:'kota',status:'lobby',players:names.map((x,i)=>Object.assign(newPlayer('B'+i,x),{bot:true})),v:1};
            startGame(s);let k=0;while(s.status==='playing'&&k<900){const t=s.turn;try{doMove(s,t,pol[names[t]](s,t));}catch(e){doMove(s,t,{type:'pass'});}k++;}
            const r=ranking(s);return {win:names[r[0].i],seatW:r[0].i,rounds:s.round,pts:r[0].pts,ok:s.status==='ended'};}
          const out={};
          for(const [a,bb] of [['hard','old'],['normal','old'],['hard','normal']])for(const n of [2,3,4]){
            const key=a+' vs '+bb+' ('+n+'p)';const w={},R=[];
            for(let g=0;g<40;g++){const names=[];for(let i=0;i<n;i++)names.push(i===(g%n)?a:bb);const res=play(names);w[res.win]=(w[res.win]||0)+1;R.push(res.rounds);}
            out[key]={winA:(w[a]||0)/40,expect:+(1/n).toFixed(2),rounds:+(R.reduce((x,y)=>x+y,0)/R.length).toFixed(1)};}
          const solo={};for(const pol2 of ['old','normal','hard']){const R=[];for(let g=0;g<30;g++)R.push(play([pol2,pol2,pol2]).rounds);solo[pol2]=+(R.reduce((x,y)=>x+y,0)/R.length).toFixed(1);}
          out.selfplay_rounds_3p=solo;return out;}""")
        for k,v in r.items(): print(k,v)
        print('errs',errs); await b.close()
asyncio.run(main())
