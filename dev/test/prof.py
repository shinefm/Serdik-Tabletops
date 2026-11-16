import asyncio
from playwright.async_api import async_playwright
SEED="""()=>{const wk=weekKey(Date.now());
 const mk=(id,week,ps,rounds,mode,level)=>{const r=[...ps].sort((a,b)=>b[2]-a[2]);const BASE={2:[20,4],3:[30,12,3],4:[40,20,8,2]}[ps.length];const award={};
  if(mode==='online')r.forEach(([uid,n,pts],k)=>{const margin=k===0?Math.min(10,2*(pts-r[1][2])):0;const speed=k===0?Math.min(20,Math.max(0,(28-rounds)*2)):0;award[uid]={rank:k+1,base:BASE[k],score:Math.min(pts,25),margin,speed,total:BASE[k]+Math.min(pts,25)+margin+speed};});
  __store['results/'+id]={mode,level,name:'Meja Serdik',endedAt:Date.now()-Math.random()*1e6,week,rounds,ids:ps.filter(p=>p[0]).map(p=>p[0]),players:ps.map(([uid,nick,pts],i)=>({id:uid,nick,bot:!uid,pts,cards:10,rank:r.findIndex(x=>x===ps[i])+1})),award,log:[]};};
 mk('g_a',wk,[['u_me','Farhan',17],['u_b','Dina',13],['u_c','Raka',9],['u_d','Sinta',6]],21,'online');
 mk('g_b',wk,[['u_b','Dina',16],['u_me','Farhan',15],['u_c','Raka',11]],24,'online');
 mk('g_c','2026-W30',[['u_c','Raka',18],['u_me','Farhan',12]],26,'online');
 mk('b_1',wk,[['u_me','Kamu',16],[null,'Bot Komodo',12]],25,'bot','hard');
 db.doc('games/tx1').set({name:'Meja Serdik',host:'u_b',createdAt:Date.now(),status:'lobby',players:[newPlayer('u_b','Dina')],v:1});}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,name in [((1300,900),'d'),((390,844),'m')]:
            ctx=await b.new_context(viewport={'width':vw[0],'height':vw[1]},device_scale_factor=1 if name=='d' else 2)
            pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mock.js')
            await pg.goto('file:///home/claude/serdik-tabletops/dev/saudagar-permata.html'); await pg.wait_for_timeout(1000)
            await pg.evaluate(SEED); await pg.evaluate("render()"); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'lobby_{name}.png',clip={'x':0,'y':0,'width':vw[0],'height':min(vw[1],600)} if name=='d' else None)
            print(name,'wa href ok:', 'meja-tx1' in (await pg.get_attribute('.trow a.wa','href')))
            await pg.click('#profBtn'); await pg.wait_for_timeout(600)
            el=await pg.query_selector('.mbox'); await el.screenshot(path=f'prof_{name}.png')
            print(name,errs); await ctx.close()
        await b.close()
asyncio.run(main())
