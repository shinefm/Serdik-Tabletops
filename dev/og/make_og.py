# Membuat gambar pratinjau link (Open Graph) 1200x630 dari elemen situs sendiri.
import asyncio,sys
from playwright.async_api import async_playwright
F='file:///home/claude/ogfonts/node_modules/@fontsource'
OUT=sys.argv[1] if len(sys.argv)>1 else '/home/claude/serdik-tabletops/og-image.jpg'
CSS=f"""
@font-face{{font-family:'Bangers';src:url('{F}/bangers/files/bangers-latin-400-normal.woff2')}}
@font-face{{font-family:'PJS';font-weight:500;src:url('{F}/plus-jakarta-sans/files/plus-jakarta-sans-latin-500-normal.woff2')}}
@font-face{{font-family:'PJS';font-weight:700;src:url('{F}/plus-jakarta-sans/files/plus-jakarta-sans-latin-700-normal.woff2')}}
@font-face{{font-family:'PJS';font-weight:800;src:url('{F}/plus-jakarta-sans/files/plus-jakarta-sans-latin-800-normal.woff2')}}
@font-face{{font-family:'Fr';font-weight:800;src:url('{F}/fraunces/files/fraunces-latin-800-normal.woff2')}}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
#og{{position:fixed;left:0;top:0;z-index:99999;width:1200px;height:630px;overflow:hidden;font-family:PJS,sans-serif;color:#3b2a20;
  background:radial-gradient(520px 520px at 1040px 120px,#f6c76a 0,#f6c76a 38%,transparent 39%),linear-gradient(160deg,#f7dcb4 0%,#f1c896 55%,#e9b47e 100%)}}
#og .hill{{position:absolute;left:-80px;right:-80px;bottom:-260px;height:420px;border-radius:50%;background:#d9a26b;opacity:.55}}
#og .hill2{{position:absolute;left:380px;right:-200px;bottom:-300px;height:420px;border-radius:50%;background:#c98d57;opacity:.45}}
#og .left{{position:absolute;left:60px;top:44px;width:660px}}
#og .logo{{display:flex;align-items:center;gap:18px}}
#og .dice{{font-size:92px;line-height:1;filter:drop-shadow(3px 4px 0 rgba(59,42,32,.35));transform:rotate(-8deg)}}
#og h1{{margin:0;font-family:Bangers;font-weight:400;font-size:104px;line-height:.92;letter-spacing:3px;color:#c4582f;text-shadow:5px 5px 0 #3b2a20,-2px -2px 0 #3b2a20,2px -2px 0 #3b2a20,-2px 2px 0 #3b2a20}}
#og .tag{{margin:20px 0 6px;font-family:Fr;font-weight:800;font-size:46px;letter-spacing:.5px}}
#og .sub{{font-size:25px;font-weight:700;color:#5a3f2c}}
#og .games{{display:flex;flex-wrap:wrap;gap:9px;margin-top:22px;width:640px}}
#og .g{{display:inline-flex;align-items:center;gap:7px;padding:6px 13px;border-radius:999px;background:#fbf3e3;border:2.5px solid #3b2a20;font-size:19px;font-weight:800;box-shadow:3px 3px 0 #3b2a20}}
#og .free{{position:absolute;left:60px;bottom:28px;font-size:22px;font-weight:700;color:#3b2a20;background:#ffe14d;border:2.5px solid #3b2a20;border-radius:12px;padding:8px 16px;box-shadow:3px 3px 0 #3b2a20}}
#og .fan{{position:absolute;left:740px;top:84px;width:420px;height:440px}}
#og .fan .card{{position:absolute;width:170px;cursor:default}}
#og .fan .c1{{left:0;top:70px;transform:rotate(-14deg)}}
#og .fan .c2{{left:118px;top:28px;transform:rotate(-2deg);z-index:2}}
#og .fan .c3{{left:236px;top:62px;transform:rotate(12deg)}}
#og .ogk{{position:absolute;left:112px;top:268px;z-index:3;width:250px;transform:rotate(-5deg);border:3px solid #3b2a20;border-radius:12px;overflow:hidden;background:#f4efe3;box-shadow:0 0 0 3px #f0c55e,6px 8px 0 rgba(59,42,32,.45)}}
#og .ogk .kart{{width:100%;height:150px;aspect-ratio:auto}}
#og .ogk .kart .kn{{font-size:19px;padding:3px 12px 3px 9px}}
#og .url{{position:absolute;right:40px;bottom:30px;font-size:22px;font-weight:800;color:#3b2a20;background:#fbf3e3;border:2.5px solid #3b2a20;border-radius:12px;padding:7px 14px;box-shadow:3px 3px 0 #3b2a20;z-index:5}}
"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1200,'height':630}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(path='/home/claude/serdik-tabletops/dev/test/mockfb.js')
        await pg.goto('file:///home/claude/serdik-tabletops/dev/fbapp/test_out/index.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate("""(css)=>{
          document.body.classList.add('light'); try{ui.theme='retro';}catch(e){}
          const st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
          const pick=(t,b)=>TIER_IDS[t].find(id=>CARDS[id].b===b&&CARDS[id].pts>0)||TIER_IDS[t].find(id=>CARDS[id].b===b);
          const cards=[pick(2,'u'),pick(3,'r'),pick(2,'g')].map(id=>cardHTML(id,{}));
          const og=document.createElement('div');document.body.appendChild(og);og.outerHTML=`<div id="og"><div class="hill"></div><div class="hill2"></div>
            <div class="left"><div class="logo"><span class="dice">🎲</span><h1>SERDIK<br>TABLETOP</h1></div>
            <div class="tag">Play. Think. Execute.</div>
            <div class="sub">Board game strategi online untuk P3MDI SBM ITB</div>
            <div class="games"><span class="g">💎 Saudagar Permata</span><span class="g">🛍️ Jualan Yuk</span><span class="g">🏛️ Rapat Rahasia</span><span class="g">🕵️ Sandi Syndicate</span><span class="g">🐺 Werewolf</span><span class="g">🏝️ Pemukim</span></div></div>
            <div class="fan">${cards.map((h,i)=>h.replace('class="card','class="c'+(i+1)+' card')).join('')}
              <div class="ogk"><div class="kart">${kotaArt('jkt')}<div class="kn">Kota Jakarta</div></div></div></div>
            <div class="free">✨ Gratis · langsung di browser · lawan teman atau bot</div>
            <div class="url">serdik-tabletops.vercel.app</div></div>`;
        }""",CSS)
        await pg.wait_for_timeout(1500)
        await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=OUT,type='jpeg',quality=86,clip={'x':0,'y':0,'width':1200,'height':630})
        print('ok',OUT,'errs',errs); await b.close()
asyncio.run(main())
