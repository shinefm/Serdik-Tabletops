import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate("""()=>{const st={players:[newPlayer('a','Farhan'),newPlayer('b','Dina')],cities:['plg','yog','smg'],kotaBy:{},mode:'kota',status:'playing'};
          const p=st.players[0];['1g0','1g1','1g2','1w0','1w1','1r0','3k0','3u1'].forEach(x=>p.cards.push(x));
          cur={local:true,st,human:0};kotaInfo('plg');document.querySelector('.kileg').open=true;}""")
        await pg.wait_for_timeout(300); await pg.screenshot(path='kota_infomodal.png'); print(errs)
        await b.close()
asyncio.run(main())
