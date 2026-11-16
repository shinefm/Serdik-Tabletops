import re
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n>=1,('tidak ketemu',a[:80])
    if cnt==1: assert n==1,('lebih dari satu',a[:80],n)
    s=s.replace(a,b)

# 1. Nama: Serdik Tabletop, P3MDI
assert 'P3MDI' not in s
s=s.replace('Serdik Games','Serdik Tabletop')
s=s.replace('P3MD','P3MDI')

# 2. Saudagar Permata terinspirasi Splendor
rep("name:'Saudagar Permata',ply:'2–4 pemain · Duel 2',dur:'20–40 menit',kind:'Strategi ekonomi'",
    "name:'Saudagar Permata',ply:'2–4 pemain · Duel 2',dur:'20–40 menit',kind:'Strategi ekonomi · terinspirasi Splendor'")

# 3. Unggulan dipisah dari game lainnya
rep("return `<div class=\"hubcard ${g.soon?'soon':''}\">",
    "return `<div class=\"hubcard ${g.soon?'soon':''} ${FEAT.includes(k)?'feat':''}\">${FEAT.includes(k)?'<span class=\"featb\">⭐ Unggulan</span>':''}")
rep("""<h2 style="font-size:22px">🎲 Pilih permainan</h2><span class="bd">Game papan online untuk syndicate P3MDI</span></div>
    <div class="hubgrid">${['permata','jualan','pemukim','rapat','werewolf','sandi'].map(card).join('')}</div></section>`;""",
    """<h2 style="font-size:22px">⭐ Game unggulan</h2><span class="bd">Game papan online untuk syndicate P3MDI</span></div>
    <div class="hubgrid featgrid">${FEAT.map(card).join('')}</div>
    <div class="hubsep"><h3>🎲 Game lainnya</h3></div>
    <div class="hubgrid">${['pemukim','rapat','werewolf','sandi'].map(card).join('')}</div></section>`;""")
rep("function hubGridHTML(){","const FEAT=['permata','jualan'];\nfunction hubGridHTML(){")
css="""
.featgrid{grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.hubcard.feat{position:relative;padding:18px 16px 16px;border:2px solid var(--gold);background:linear-gradient(160deg,rgba(230,184,76,.20),var(--panel2) 55%);box-shadow:0 6px 18px rgba(0,0,0,.18)}
.hubcard.feat .hi{font-size:44px}.hubcard.feat .hh b{font-size:19px}.hubcard.feat .hd{font-size:14.5px}
.featb{position:absolute;top:-11px;right:14px;background:linear-gradient(180deg,#f0c55e,#d9a63a);color:#2b1f05;font-size:11.5px;font-weight:800;padding:3px 10px;border-radius:999px;border:1px solid #b5861b;letter-spacing:.3px}
.hubsep{margin:22px 0 0;padding-top:14px;border-top:1px dashed var(--line)}.hubsep h3{margin:0;font-size:17px;opacity:.85}
body.light .hubcard.feat{background:linear-gradient(160deg,#fbe7b0,#fbf5e6 60%);border-color:#d9a63a}
"""
rep(".hubp{grid-column:1/-1}",".hubp{grid-column:1/-1}"+css)

# 4. Tema terang sebagai bawaan
rep("try{ui.mode=localStorage.getItem('sp_mode')||'dark';}catch(e){ui.mode='dark';}",
    "try{ui.mode=localStorage.getItem('sp_mode')||'light';}catch(e){ui.mode='light';}")
rep('<button class="btn sm" id="themeBtn" data-act="theme" aria-label="Ganti tema">☀️ <span class="lbl">Terang</span></button>',
    '<button class="btn sm" id="themeBtn" data-act="theme" aria-label="Ganti tema">🌙 <span class="lbl">Gelap</span></button>')
open(F,'w').write(s)
print('ok hub2')
