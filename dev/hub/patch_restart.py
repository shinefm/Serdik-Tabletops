import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:90])
    s=s.replace(a,b)
# 1. Permata: pindahkan isi localStart ke fungsi yang bisa dipanggil ulang
a=s.index("      ui.lastLocal={me,bots,level,mode:lmode,order:ord,timer:tmr};\n")
b=s.index("      if(level==='hard'&&lmode!=='duel')loadModel(); break;}",a)+len("      if(level==='hard'&&lmode!=='duel')loadModel(); break;}")
s=s[:a]+"""      ui.lastLocal={me,bots,level,mode:lmode,order:ord,timer:tmr};
      startLocalCfg(ui.lastLocal); break;}
    case 'restartlocal':restartLocal();break;
    case 'restartlocalok':{closeModal();const L=restartCfg();if(cur&&cur.lid)ui.saved[cur.lid]=true;if(L.pm)pmStartCfg(L);else startLocalCfg(L);toast('🆕 Game baru dimulai — kartu dikocok ulang');break;}"""+s[b:]
rep("async function leaveTable(next){","""function startLocalCfg(L){
  const me=L.me, bots=L.bots, level=L.level, lmode=L.mode||'klasik', ord=L.order||'random', tmr=L.timer||0;
  const botPl=bots.slice(0,lmode==='duel'?1:bots.length).map((n,i)=>Object.assign(newPlayer('B'+i,n),{bot:true}));
  const total=botPl.length+1, hpos=ord==='random'?Math.floor(Math.random()*total):Math.min(+ord,total-1);
  const players=[...botPl]; players.splice(hpos,0,newPlayer('H',me));
  const s={name:'Lawan bot',status:'lobby',players,v:1};
  if(lmode==='duel'){s.players=s.players.slice(0,2);s.name='Duel lawan bot';startDuel(s);}else startGame(s);
  s.players.forEach((p,i)=>{p.bot=players[i].bot||false;});
  s.timer=tmr; s.turnAt=Date.now();
  if(cur&&cur.unsub)cur.unsub(); if(cur&&cur.botTimer)clearTimeout(cur.botTimer); ui.guideFrom=null;
  ui.dsel=[];ui.dpriv=false;
  s.log.push({p:-1,m:`Urutan giliran${ord==='random'?' (diacak)':''}: kamu ${ORD_NAMES[hpos].toLowerCase()}.`});
  cur={local:true,st:s,human:hpos,level,lid:'b'+Date.now().toString(36)+Math.random().toString(36).slice(2,6)}; ui.rec=[]; view='table'; ui.sel={}; closeModal(); render();
  if(level==='hard'&&lmode!=='duel')loadModel();
}
function restartCfg(){
  const st=cur.st, h=cur.human, bots=st.players.filter((p,i)=>i!==h).map(p=>p.nick||'Bot');
  if(st.game==='pemukim'){const L=ui.lastPm||{};return {pm:true,me:L.me||st.players[h].nick||'Kamu',bots:L.bots&&L.bots.length===bots.length?L.bots:bots,level:L.level||cur.level||'normal',order:L.order||String(h),timer:L.timer!=null?L.timer:(st.timer||0)};}
  const L=ui.lastLocal||{};
  return {me:L.me||st.players[h].nick||'Kamu',bots:L.bots&&L.bots.length>=bots.length?L.bots:bots,level:L.level||cur.level||'normal',mode:st.mode==='duel'?'duel':'klasik',order:L.order||String(h),timer:L.timer!=null?L.timer:(st.timer||0)};
}
function restartLocal(){
  if(!cur||!cur.local)return;
  const L=restartCfg(), ended=cur.st.status!=='playing';
  openModal(`<h3>🔁 Ulang dari awal?</h3><p style="font-size:14px;line-height:1.55;margin:0">Mulai game baru dengan pengaturan yang sama: <b>${L.pm?'🏝️ Pemukim':L.mode==='duel'?'⚔️ Duel':'💎 Klasik'}</b> · ${L.bots.length} bot (${esc(L.bots.join(', '))}) · level <b>${LVNAME[L.level]||L.level}</b> · urutan ${L.order==='random'?'diacak':'tetap'}.</p>
    ${ended?'':'<p class="bd" style="margin:8px 0 0">Game yang sedang berjalan tidak akan disimpan dan tidak tercatat.</p>'}
    <div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="restartlocalok">🔁 Ulang sekarang</button></div>`);
}
async function leaveTable(next){""")
# 2. tombol di modal keluar
rep("""    <div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn" data-act="nosavequit">Keluar tanpa simpan</button><button class="btn pri" data-act="savequit">💾 Simpan &amp; keluar</button></div>`);""",
"""    <div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn" data-act="restartlocalok" title="Kartu dikocok ulang, bot dan level sama">🆕 Main game baru</button><button class="btn" data-act="nosavequit">Keluar tanpa simpan</button><button class="btn pri" data-act="savequit">💾 Simpan &amp; keluar</button></div>`);""")
# 3. Pemukim: pisahkan start dari form
rep("""  const bots=randomBots(nb); ui.lastPm={me,bots,level,order:ord,timer:tmr};
  const total=nb+1,""","""  const bots=randomBots(nb); ui.lastPm={me,bots,level,order:ord,timer:tmr};
  pmStartCfg(ui.lastPm);
}
function pmStartCfg(L){
  const me=L.me, bots=L.bots, nb=bots.length, level=L.level, ord=L.order||'random', tmr=L.timer||0;
  const total=nb+1,""")
rep("""${cur.local&&!cur.guided?'<button class="btn" data-act="localSetup">Main lagi</button>':''}""","""${cur.local&&!cur.guided?'<button class="btn" data-act="restartlocalok">🆕 Main game baru</button><button class="btn" data-act="localSetup">Ganti bot/level</button>':''}""")
rep("""${cur.local?'<button class="btn" data-act="pmagain">🔁 Main lagi</button>':''}""","""${cur.local?'<button class="btn" data-act="restartlocalok">🆕 Main game baru</button><button class="btn" data-act="pmagain">Ganti bot/level</button>':''}""")
rep("  next=next||backToLobby;\n  if(!localGameActive()){next();return;}","  next=next||backToLobby;\n  if(!(cur&&cur.local&&!cur.guided&&cur.st&&cur.st.status==='playing')){next();return;}")
rep("function backToLobby(){\n","function backToLobby(){\n  {const rp=$('#rankpop');if(rp)rp.classList.remove('show');}\n")
rep("  openModal(`<h3>💾 Simpan progres dulu?</h3>","  openModal(`<h3>🚪 Keluar dari game lawan bot?</h3>")
open(p,'w').write(s); print('restart ok')
