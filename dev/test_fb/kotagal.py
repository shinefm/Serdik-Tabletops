import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for vw,tag,dsf in [({'width':1000,'height':900},'d',1.5),({'width':390,'height':844},'m',2)]:
            pg=await b.new_page(viewport=vw,device_scale_factor=dsf); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
            await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
            await pg.evaluate("""()=>{const st={players:[newPlayer('a','Farhan'),newPlayer('b','Dina')],cities:Object.keys(KOTA),kotaBy:{plg:1},mode:'kota'};
              const p=st.players[0];['1g0','1g1','1g2','1u0','1u1','1u2','1w0','1w1'].forEach(x=>p.cards.push(x));
              cur={local:true,st,human:0};
              $('#app').innerHTML='<section class="panel">'+kotaPanel(st)+'</section>';}""")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'kota_gal_{tag}.png',full_page=True); print(tag,errs)
        await b.close()
asyncio.run(main())
