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
rep("function hardBotMove(st,pi,model,opt){\n","function hardBotMove(st,pi,model,opt){\n  if(st.mode==='kota')return kotaMoveD(st,pi,P_KV);\n")
rep("function botMove(st,pi,level,P){\n","function botMove(st,pi,level,P){\n  if(st.mode==='kota'&&level!=='easy'&&!P)return kotaMoveD(st,pi,level==='hard'?P_KV:P_KV_N);\n")

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
# Main game baru / ulang: pertahankan mode Kota
rep("order:L.order||String(h),timer:L.timer!=null?L.timer:(st.timer||0)};\n}\nfunction restartLocal(){",
    "order:L.order||String(h),timer:L.timer!=null?L.timer:(st.timer||0)};\n}\nfunction restartLocal(){")
rep("level:L.level||cur.level||'normal',mode:st.mode==='duel'?'duel':'klasik',order:",
    "level:L.level||cur.level||'normal',mode:st.mode==='duel'?'duel':st.mode==='kota'?'kota':'klasik',order:")
rep("${L.pm?'🏝️ Pemukim':L.mode==='duel'?'⚔️ Duel':'💎 Klasik'}","${L.pm?'🏝️ Pemukim':L.mode==='duel'?'⚔️ Duel':L.mode==='kota'?'🏙️ Ekspansi Kota':'💎 Klasik'}")
# klik
rep("    case 'sdteam':","    case 'kotainfo':kotaInfo(el.dataset.id);break;\n    case 'sdteam':")
rep("</style>","""/* --- Ekspansi Kota --- */
.kotas{display:flex;flex-wrap:wrap;gap:12px;margin:2px 4px 14px;align-items:stretch}
.kota{position:relative;cursor:pointer;display:flex;align-items:stretch;background:#f4efe3;border:2px solid #3b2a20;border-radius:9px;overflow:hidden;box-shadow:0 0 0 2px var(--kt,#1f5f6b),3px 4px 0 2px rgba(0,0,0,.4);transition:transform .12s}
.kota:hover{transform:translateY(-2px)}
.kota.kt-k{--kt:#4a4858}.kota.kt-u{--kt:#2f6fe0}.kota.kt-r{--kt:#d63645}.kota.kt-w{--kt:#b39e74}.kota.kt-g{--kt:#1b9460}.kota.kt-x{--kt:#9b4fd6}
.kart{position:relative;flex:0 0 auto;width:104px;height:104px;background:#ddd}
.kart svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.kart .kn{position:absolute;left:0;bottom:0;padding:2px 6px 2px 4px;background:#3b2a20;color:#f4efe3;font:700 11.5px/1.25 Fraunces,serif;border-top-right-radius:7px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.kstamp{position:absolute;top:3px;left:3px;padding:1px 6px;border-radius:6px;background:rgba(59,42,32,.88);color:#f4efe3;font:700 10.5px/1.3 system-ui,sans-serif;max-width:90%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.kstamp.ok{background:#1b9460}
.kside{flex:0 0 auto;width:34px;display:flex;flex-direction:column;align-items:center;gap:3px;padding:4px 0 5px;background:#f4efe3;border-left:2px solid #3b2a20}
.kp{display:inline-flex;align-items:center;justify-content:center;min-width:26px;height:26px;padding:0 3px;border-radius:7px;font:800 17px/1 Fraunces,serif;color:#3b2a05;background:linear-gradient(180deg,#f6d77a,#e0a92e);border:1.5px solid #8a6212;box-shadow:inset 0 1px 0 #fff3c4,1px 1px 0 rgba(0,0,0,.3)}
.kplus{font:800 13px/.8 system-ui,sans-serif;color:#3b2a20;opacity:.7}
.kside.many{width:50px;flex-direction:row;flex-wrap:wrap;justify-content:center;align-content:flex-start;gap:4px 3px}.kside.many .kplus{flex-basis:100%;text-align:center}
.kc{display:inline-flex;align-items:center;justify-content:center;width:20px;height:25px;border-radius:4px;border:1.5px solid #3b2a20;font:800 12.5px/1 system-ui,sans-serif;color:#fff;text-shadow:0 1px 1px rgba(0,0,0,.45);box-shadow:1px 1px 0 rgba(0,0,0,.35)}
.kc.c-w{background:#efe5cf;color:#3b2a20;text-shadow:none}.kc.c-u{background:#2f6fe0}.kc.c-g{background:#1b9460}.kc.c-r{background:#d63645}.kc.c-k{background:#4a4858}
.kc.kany{background:repeating-linear-gradient(135deg,#9a968a 0 4px,#b9b5a8 4px 8px)}
.kc.keach{background:linear-gradient(180deg,#efe5cf 0 20%,#2f6fe0 20% 40%,#1b9460 40% 60%,#d63645 60% 80%,#4a4858 80%)}
.kota .ok{outline:2px solid #1b9460;outline-offset:1px}
.kota.ready{box-shadow:0 0 0 3px #1b9460,0 0 14px #1b946088,3px 4px 0 2px rgba(0,0,0,.4)}
.kota.taken .kart svg{filter:grayscale(.85) brightness(.9)}.kota.taken .kside{opacity:.5}
.kinfoart{border-radius:10px;overflow:hidden;border:2px solid #3b2a20;aspect-ratio:100/50;margin:0 0 8px}.kinfoart svg{width:100%;height:100%;display:block}
.kirows{display:flex;flex-direction:column;gap:6px}
.kirow{display:flex;gap:10px;align-items:center;padding:6px 8px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);font-size:14px;line-height:1.4}
.kirow.ok{border-color:#1b9460;box-shadow:inset 3px 0 0 #1b9460}.kirow.no{box-shadow:inset 3px 0 0 #d9a63a}
.kiico{flex:0 0 32px;display:flex;justify-content:center}.kiico .kc{width:22px;height:28px;font-size:13px}
.kileg{margin-top:10px;font-size:13.5px}.kileg summary{cursor:pointer;font-weight:700;margin-bottom:6px}.kileg .kirow{margin:4px 0;background:transparent}
.m-field .kotas{gap:7px;margin:0 2px 8px}
@media(max-width:560px){.kotas{gap:6px;margin:0 0 8px;justify-content:space-between}.kota{border-radius:7px;box-shadow:0 0 0 1.5px var(--kt,#1f5f6b),2px 3px 0 1px rgba(0,0,0,.4)}.kart{width:70px;height:70px}.kart .kn{font-size:9px;padding:1px 4px 1px 3px}.kstamp{font-size:8px;padding:1px 3px}.kside{width:24px;gap:2px;padding:3px 0 4px;border-left-width:1.5px}.kp{min-width:20px;height:19px;font-size:12.5px;border-radius:5px;border-width:1px;padding:0 2px}.kplus{font-size:9px}.kc{width:15px;height:18px;font-size:10px;border-width:1px;border-radius:3px}.kside.many{width:36px;gap:3px 2px}}

</style>""")
open(F,'w').write(s)
print('ok kota')
