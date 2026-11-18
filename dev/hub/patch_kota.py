# Saudagar Permata: mode Ekspansi Kota (mirip Cities of Splendor)
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b,n=1):
    global s
    k=s.count(a); assert k==n,(k,a[:90]); s=s.replace(a,b)

js=open('hub/kota.js').read()
rep("<div class=\"patrons\">${st.patrons.map(patronHTML).join('')||'<span class=\"mute\">Semua pahlawan sudah memberi dukungan.</span>'}</div>","${patronsOrKota(st)}",2)
rep("function startGame(st){",js+"\nfunction startGame(st){")

# mesin
rep("  st.patrons=shuffle(Object.keys(PAT)).slice(0,n+1);\n",
    "  st.patrons=shuffle(Object.keys(PAT)).slice(0,n+1);\n  if(st.mode==='kota')kotaStart(st);\n")
rep("  if(!st.endTriggered&&ptsOf(p)>=WIN){st.endTriggered=true;st.log.push({p:pi,m:'mencapai '+WIN+' poin — ini ronde terakhir!'});}",
    "  if(st.mode==='kota')kotaCheck(st,pi,p);\n  else if(!st.endTriggered&&ptsOf(p)>=WIN){st.endTriggered=true;st.log.push({p:pi,m:'mencapai '+WIN+' poin — ini ronde terakhir!'});}")
rep("  if(st.turn===0){ if(st.endTriggered){st.status='ended';st.log.push({p:-1,m:'Permainan selesai.'});} else st.round++; }",
    "  if(st.turn===0){ if(st.endTriggered){st.status='ended';st.log.push({p:-1,m:'Permainan selesai.'});if(st.mode==='kota')kotaRanking(st);} else st.round++; }")
rep("  return st.players.map((p,i)=>({i,pts:ptsOf(p),n:p.cards.length})).sort((a,b)=>b.pts-a.pts||a.n-b.n);\n}",
    "  if(st.mode==='kota')return kotaRanking(st);\n  return st.players.map((p,i)=>({i,pts:ptsOf(p),n:p.cards.length})).sort((a,b)=>b.pts-a.pts||a.n-b.n);\n}")
# bot
rep("  const help=card=>st.patrons.reduce(","  const help=card=>st.mode==='kota'?kotaHelp(st,p,b,card):st.patrons.reduce(")
rep("function hardBotMove(st,pi,model,opt){\n","function hardBotMove(st,pi,model,opt){\n  if(st.mode==='kota')return botMove(st,pi,'hard');\n")

# papan: kota menggantikan pahlawan (tampilan HP & desktop)

# pilihan mode: lawan bot
rep('<button class="btn sm ${ui.lpMode===\'duel\'?\'on\':\'\'}" data-act="lpmode" data-m="duel">⚔️ Duel (1 lawan 1)</button>',
    '<button class="btn sm ${ui.lpMode===\'duel\'?\'on\':\'\'}" data-act="lpmode" data-m="duel">⚔️ Duel (1 lawan 1)</button><button class="btn sm ${ui.lpMode===\'kota\'?\'on\':\'\'}" data-act="lpmode" data-m="kota">🏙️ Ekspansi Kota (2–4)</button>')
rep("  const s={name:'Lawan bot',status:'lobby',players,v:1};\n  if(lmode==='duel')",
    "  const s={name:lmode==='kota'?'Kota lawan bot':'Lawan bot',status:'lobby',players,v:1};\n  if(lmode==='kota')s.mode='kota';\n  if(lmode==='duel')")
# pilihan mode: meja online
rep('<option value="duel">⚔️ Permata Duel (2)</option>','<option value="duel">⚔️ Permata Duel (2)</option><option value="kota">🏙️ Permata Ekspansi Kota (2–4)</option>')
rep("status:'lobby',mode:md==='duel'?'duel':'klasik',timer:tmr,","status:'lobby',mode:md==='duel'?'duel':md==='kota'?'kota':'klasik',timer:tmr,")
rep("${st.mode==='duel'?'⚔️ Mode Duel: ajak 1 lawan.':'💎 Mode Klasik: ajak 2–4 orang.'}",
    "${st.mode==='duel'?'⚔️ Mode Duel: ajak 1 lawan.':st.mode==='kota'?'🏙️ Mode Ekspansi Kota: ajak 2–4 orang. Rebut kota, bukan kejar 15 poin.':'💎 Mode Klasik: ajak 2–4 orang.'}")
rep("${g.mode==='duel'?'<span class=\"pill playing\" style=\"background:#5a2a86;color:#f1e1ff\">⚔️ Duel</span>':''}",
    "${g.mode==='duel'?'<span class=\"pill playing\" style=\"background:#5a2a86;color:#f1e1ff\">⚔️ Duel</span>':g.mode==='kota'?'<span class=\"pill playing\" style=\"background:#1f5f6b;color:#dff7fb\">🏙️ Kota</span>':''}")
rep("Ayo main Saudagar Permata${st&&st.mode==='duel'?' ⚔️ Duel':''}!","Ayo main Saudagar Permata${st&&st.mode==='duel'?' ⚔️ Duel':st&&st.mode==='kota'?' 🏙️ Ekspansi Kota':''}!")

# tutorial
rep('data-act="tutorial" data-w="duel">⚔️ Duel</button>','data-act="tutorial" data-w="duel">⚔️ Duel</button><button class="btn sm ${which===\'kota\'?\'on\':\'\'}" data-act="tutorial" data-w="kota">🏙️ Kota</button>')
rep("cur.st.mode==='duel'?'duel':'klasik');","cur.st.mode==='duel'?'duel':cur&&cur.st&&cur.st.mode==='kota'?'kota':'klasik');")
rep("  if(which==='rapat'||which==='werewolf'||which==='pemukim'||which==='wwk'||which==='sandi'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class=\"rules tutrules\">${which==='sandi'?sandiRules():",
    "  if(which==='rapat'||which==='werewolf'||which==='pemukim'||which==='wwk'||which==='sandi'||which==='kota'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class=\"rules tutrules\">${which==='kota'?kotaRules():which==='sandi'?sandiRules():")
# kartu hub
rep("ply:'2–4 pemain · Duel 2',","ply:'2–4 pemain · Duel 2 · Kota',")

# panel pemain: kota yang dimiliki menggantikan baris pahlawan
rep("<span>Pahlawan: ${p.pat.length?p.pat.map(id=>esc(PAT[id].name)).join(', '):'—'}</span>",
    "<span>${cur.st.mode==='kota'?'Kota: '+(p.kota?'🏙️ '+esc(KOTA[p.kota].name):'—'):'Pahlawan: '+(p.pat.length?p.pat.map(id=>esc(PAT[id].name)).join(', '):'—')}</span>")
rep("${p.pat.length?' · 🎖️'+p.pat.length:''}</div><div class=\"pmeta\">","${p.pat.length?' · 🎖️'+p.pat.length:''}${p.kota?' · 🏙️'+esc(KOTA[p.kota].name):''}</div><div class=\"pmeta\">")
# klik
rep("    case 'sdteam':","    case 'kotainfo':kotaInfo(el.dataset.id);break;\n    case 'sdteam':")
rep("</style>","""/* --- Ekspansi Kota --- */
.kotas{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:2px 4px 14px}
.kota{position:relative;cursor:pointer;background:#f4efe3;border:2px solid #3b2a20;border-radius:10px;padding:5px;box-shadow:0 0 0 2px var(--kt,#1f5f6b),3px 4px 0 2px rgba(0,0,0,.4);display:flex;flex-direction:column;gap:5px;transition:transform .12s}
.kota:hover{transform:translateY(-2px)}
.kota.kt-k{--kt:#4a4858}.kota.kt-u{--kt:#2f6fe0}.kota.kt-r{--kt:#d63645}.kota.kt-w{--kt:#b39e74}.kota.kt-g{--kt:#1b9460}.kota.kt-x{--kt:#9b4fd6}
.kart{position:relative;border-radius:6px;overflow:hidden;aspect-ratio:100/62;background:#ddd;border:1.5px solid #3b2a20}
.kart svg{width:100%;height:100%;display:block}
.kart .kn{position:absolute;left:0;bottom:0;padding:2px 8px 2px 6px;background:#3b2a20;color:#f4efe3;font:700 13px/1.25 Fraunces,serif;border-top-right-radius:8px;letter-spacing:.2px}
.kstamp{position:absolute;top:4px;right:4px;padding:2px 6px;border-radius:7px;background:rgba(59,42,32,.88);color:#f4efe3;font:700 11px/1.2 system-ui,sans-serif;max-width:92%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.kstamp.ok{background:#1b9460}
.kota .kr{display:flex;flex-wrap:wrap;gap:4px;align-items:center;padding:0 1px 1px}
.kota .hsq{width:22px;height:22px;font-size:12.5px}
.kreq{display:inline-flex;align-items:center;justify-content:center;height:22px;padding:0 6px;border-radius:7px;font:800 12px/1 system-ui,sans-serif;background:#e6dcc4;color:#3b2a20;border:1.5px solid #3b2a20;white-space:nowrap}
.kreq.kpts{background:#f0c55e;color:#3b2a05}
.kota .ok{box-shadow:0 0 0 2px #1b9460}.kota .no{opacity:.55}
.kota.ready{box-shadow:0 0 0 3px #1b9460,0 0 14px #1b946088,3px 4px 0 2px rgba(0,0,0,.4)}
.kota.taken .kart svg{filter:grayscale(.85) brightness(.9)}.kota.taken .kr{opacity:.5}
.kinfoart{border-radius:10px;overflow:hidden;border:2px solid #3b2a20;aspect-ratio:100/62;margin:0 0 8px}.kinfoart svg{width:100%;height:100%;display:block}
.krow{font-size:14.5px;margin:4px 0}
.m-field .kotas{gap:7px;margin:0 2px 8px}
@media(max-width:560px){.kotas{gap:7px;margin:0 2px 8px}.kota{padding:3px;gap:3px;border-radius:8px;box-shadow:0 0 0 1.5px var(--kt,#1f5f6b),2px 3px 0 1px rgba(0,0,0,.4)}.kart{border-radius:5px}.kart .kn{font-size:10.5px;padding:1px 5px 1px 4px}.kstamp{font-size:9px;padding:1px 4px;top:2px;right:2px}.kreq{height:18px;font-size:10px;padding:0 3px;border-width:1px}.kota .hsq{width:18px;height:18px;font-size:10.5px}.kota .kr{gap:3px}}
</style>""")
open(F,'w').write(s)
print('ok kota')
