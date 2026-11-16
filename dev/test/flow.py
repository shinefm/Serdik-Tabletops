import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1300,'height':1000})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate("c0delay=()=>20")
        await pg.click('[data-act="localSetup"]'); await pg.select_option('#lpN','1'); await pg.select_option('#lpLv','hard')
        await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(500)
        t=await pg.evaluate("""async()=>{const t0=Date.now();let g=0;while(cur.st.status==='playing'&&g++<400){ if(cur.st.turn===cur.human&&!ui.busy){const mv=botMove(cur.st,cur.human,'normal');await runMove(mv);} await new Promise(r=>setTimeout(r,40)); } return {status:cur.st.status,round:cur.st.round,ms:Date.now()-t0,rec:ui.rec.length,model:!!cur.model};}""")
        print('bot game',t)
        await pg.wait_for_timeout(800)
        keys=await pg.evaluate("Object.keys(__store)")
        print('store keys',keys)
        await pg.screenshot(path='end_dark.png',clip={'x':0,'y':0,'width':1300,'height':420})
        # seed fake online results
        await pg.evaluate("""()=>{const wk=weekKey(Date.now());const old='2026-W30';
          const mk=(id,week,ps,rounds)=>{const st={status:'ended',round:rounds,players:ps.map(([uid,nick,pts,cards])=>({id:uid,nick,cards:Array(cards).fill('1w0'),pat:[],t:{},res:[]}))};
            st.players.forEach((p,i)=>{p.cards=[];});
            const fake={}; ps.forEach(([uid,nick,pts,cards],i)=>{fake[uid]={pts,cards};});
            const r=[...ps].sort((a,b)=>b[2]-a[2]||a[3]-b[3]);const BASE={2:[20,4],3:[30,12,3],4:[40,20,8,2]}[ps.length];const award={};
            r.forEach(([uid,nick,pts,cards],k)=>{const margin=k===0?Math.min(10,2*(pts-r[1][2])):0;const speed=k===0?Math.min(20,Math.max(0,(28-rounds)*2)):0;const score=Math.min(pts,25);award[uid]={rank:k+1,base:BASE[k],score,margin,speed,total:BASE[k]+score+margin+speed};});
            __store['results/'+id]={mode:'online',name:'Meja Serdik',endedAt:Date.now()-Math.random()*1e6,week,rounds,ids:ps.map(x=>x[0]),players:ps.map(([uid,nick,pts,cards])=>({id:uid,nick,bot:false,pts,cards,rank:award[uid].rank})),award,log:[{p:0,m:'mengambil 1 Mutiara, 1 Safir, 1 Zamrud'},{p:1,m:'membeli kartu Rubi Tingkat I'}]};};
          mk('g_a',wk,[['u_me','Farhan',17,14],['u_b','Dina',13,12],['u_c','Raka',9,10],['u_d','Sinta',6,8]],21);
          mk('g_b',wk,[['u_b','Dina',16,13],['u_me','Farhan',15,15],['u_c','Raka',11,11]],24);
          mk('g_c',old,[['u_c','Raka',18,15],['u_me','Farhan',12,12]],26);}""")
        await pg.click('#lbBtn'); await pg.wait_for_timeout(500)
        el=await pg.query_selector('.mbox'); await el.screenshot(path='lb_week.png')
        await pg.click('[data-act="lbtab"][data-t="all"]'); await pg.wait_for_timeout(400)
        el=await pg.query_selector('.mbox'); await el.screenshot(path='lb_all.png')
        await pg.click('[data-act="close"]')
        await pg.click('#histBtn'); await pg.wait_for_timeout(500)
        el=await pg.query_selector('.mbox'); await el.screenshot(path='hist.png')
        await pg.click('.hrow'); await pg.wait_for_timeout(300)
        el=await pg.query_selector('.mbox'); await el.screenshot(path='hist_detail.png')
        await pg.click('[data-act="close"]')
        # light mode board
        await pg.click('#themeBtn'); await pg.click('[data-act="localSetup"]'); await pg.select_option('#lpN','3'); await pg.click('[data-act="localStart"]'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='light.png')
        await pg.click('[data-act="lobby"]'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='light_lobby.png',clip={'x':0,'y':0,'width':1300,'height':520})
        print('errors',errs)
        await b.close()
asyncio.run(main())
