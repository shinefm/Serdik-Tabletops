# Perluas menu ⚙️ Atur meja ke Jualan Yuk, Rapat Rahasia, Werewolf (Satu Malam & Klasik)
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b):
    global s
    n=s.count(a); assert n==1,(n,a[:90]); s=s.replace(a,b)

PAUSED="'⏸️ Permainan sedang dijeda tuan rumah'"
HUBG="['pemukim','jualan','rapat','werewolf','wwk']"

# --- game mana saja ---
rep("function hostName(st){",
    "const HOST_GAMES="+HUBG+";\nfunction hostGameOk(st){return st&&!cur.local&&st.status==='playing'&&(!st.game||HOST_GAMES.includes(st.game));}\nfunction hostName(st){")
rep("canWrite!==false&&afkGameOk(st)&&st.host===myId);}","canWrite!==false&&hostGameOk(st)&&st.host===myId);}")
# bilah jeda/autopilot tampil di semua game itu (lapor AFK tetap khusus Permata & Pemukim)
rep("if(view!=='table'||!cur||!st||!afkGameOk(st)||online!=='on'){if(bar)bar.remove();return;}",
    "if(view!=='table'||!cur||!st||!hostGameOk(st)||online!=='on'){if(bar)bar.remove();return;}")

# --- penjaga jeda untuk game hub ---
rep("function hubAct(st,pi,mv){return ","function hubAct(st,pi,mv){if(st.paused&&st.status==='playing')fail("+PAUSED+");return ")
rep("function jyAct(st,pi,mv){\n  if(st.status!=='playing')fail('Permainan belum/ sudah selesai');",
    "function jyAct(st,pi,mv){\n  if(st.status!=='playing')fail('Permainan belum/ sudah selesai');\n  if(st.paused)fail("+PAUSED+");")
rep("  const st=cur.st; if(st.status!=='playing')return; const nx=jyBotNext(st,false); if(!nx)return;",
    "  const st=cur.st; if(st.status!=='playing'||st.paused)return; const nx=jyBotNext(st,false); if(!nx)return;")
rep("function tickTimer(){\n  if(view!=='table'||!cur||!cur.st)return;\n  const st=cur.st, l=tmrLeft(st);",
    "function tickTimer(){\n  if(view!=='table'||!cur||!cur.st)return;\n  const st=cur.st, l=tmrLeft(st);\n  hostAutoTick(st);")

# --- Jualan Yuk: tim diganti bot (T.auto) ---
rep("function jyHolder(st,t,div){const T=st.teams[t];if(!T)return [];if(T.bot)return [];",
    "function jyHolder(st,t,div){const T=st.teams[t];if(!T)return [];if(T.bot||T.auto)return [];")
rep("    if(!(T.bot||all))continue;","    if(!(T.bot||T.auto||all))continue;")
rep("      if(T.bot)return jyApplyBot(s,{t,mv:{type:'plan',d:jyBotPlan(s,t)}});",
    "      if(T.bot||T.auto)return jyApplyBot(s,{t,mv:{type:'plan',d:jyBotPlan(s,t)}});")
rep("function jyNames(st,t){const T=st.teams[t];if(T.bot)return '🤖 Tim bot';return T.members.map(i=>esc(nm(st,i))).join(', ');}",
    "function jyNames(st,t){const T=st.teams[t];if(T.bot)return '🤖 Tim bot';return T.members.map(i=>esc(nm(st,i))).join(', ')+(T.auto?' · 🤖 dimainkan bot':'');}")
# "Ambil alih" oleh anggota tim mengembalikan timnya
rep("function afkHere(s,me){const uid=s.players[me].id;",
    "function afkHere(s,me){const uid=s.players[me].id;if(s.game==='jualan'&&s.teams){const T=s.teams[jyTeamOf(s,me)];if(T&&T.auto){delete T.auto;T.members.forEach(i=>{delete s.players[i].auto;});s.afkNote={m:'🙋 '+nm(s,me)+' mengambil alih '+T.name+' dari bot',at:Date.now()};return;}}")

# --- operasi tuan rumah: lewati & ganti bot untuk game hub ---
rep("""  if(kind==='skip'){if(s.paused)fail('Lanjutkan permainan dulu sebelum melewati giliran');const t=s.turn,name=nm(s,t);
    if(s.game==='pemukim')pmTimeoutRun(s);else doMove(s,t,{type:'pass'});
    note('⏭ '+who+' melewati giliran '+name);return;}""",
"""  if(kind==='skip'){if(s.paused)fail('Lanjutkan permainan dulu sebelum melewati giliran');
    if(s.game==='jualan'){jyTimeoutRun(s);s.turnAt=Date.now();note('⏭ '+who+' melewati tahap ini (diisi otomatis)');return;}
    if(s.game&&s.game!=='pemukim'){hubAct(s,me,{type:'timeout',forced:true});note('⏭ '+who+' melewati tahap ini');return;}
    const t=s.turn,name=nm(s,t);
    if(s.game==='pemukim')pmTimeoutRun(s);else doMove(s,t,{type:'pass'});
    note('⏭ '+who+' melewati giliran '+name);return;}
  if(kind==='tbot'||kind==='thuman'){const T=s.teams&&s.teams[i];if(!T||T.bot)fail('Tim tidak ditemukan');
    if(kind==='tbot'){if(T.auto)throw NOOP;T.auto=true;T.members.forEach(j=>{s.players[j].auto=true;});note('🤖 '+T.name+' kini dimainkan bot (diatur tuan rumah)');}
    else{if(!T.auto)throw NOOP;delete T.auto;T.members.forEach(j=>{delete s.players[j].auto;});note('🙋 '+T.name+' kembali dimainkan anggotanya');}
    return;}""")

# --- pemain otomatis di Rapat/Werewolf: kalau yang ditunggu tinggal pemain otomatis, tahap langsung diselesaikan ---
rep("function hostDo(kind,i,ok){","""function hostAutoTick(st){
  if(!cur||cur.local||!st||st.status!=='playing'||st.paused||canWrite===false||!myId)return;
  if(!['rapat','werewolf','wwk'].includes(st.game))return;
  const pend=rapatPending(st); if(!pend.length||!pend.every(i=>st.players[i]&&(st.players[i].auto||st.players[i].bot)))return;
  const me=meIdx(st); if(me<0)return;
  const humans=st.players.filter(q=>!q.bot&&!q.auto).map(q=>q.id), order=[st.host,...humans.filter(x=>x!==st.host)];
  const runner=order.find(id=>id===myId||ONLINE.has(id)), stalled=st.turnAt&&Date.now()-st.turnAt>8000;
  if(runner!==myId&&!stalled)return;
  const key=cur.gid+':'+st.v; if(ui.hauto===key)return; ui.hauto=key; const v=st.v;
  setTimeout(()=>{if(!cur||!cur.st||cur.st.v!==v)return;
    commitOnline(s=>{if(s.v!==v||s.status!=='playing'||s.paused)throw NOOP;const p2=rapatPending(s);if(!p2.length||!p2.every(i=>s.players[i].auto||s.players[i].bot))throw NOOP;
      s.log.push({p:-1,m:'🤖 Pilihan pemain otomatis diambil (bawaan).'});hubAct(s,meIdx(s),{type:'timeout',auto:true});}).catch(()=>{ui.hauto=null;});
  },1500);
}
function hostDo(kind,i,ok){""")

# --- isi menu untuk game hub ---
rep("function hostModal(){\n  if(!hostCan())return;",
    "function hostModal(){\n  if(!hostCan())return;\n  if(cur.st.game&&cur.st.game!=='pemukim')return hostModalHub();")
rep("function hostConfirm(i){","""function hostModalHub(){
  const st=cur.st, me=meIdx(st), JY_=st.game==='jualan';
  const pend=JY_?jyPending(st):rapatPending(st);
  const skipLbl=JY_?'⏭ Lewati tahap ini (isi otomatis)':'⏭ Lewati tahap ini';
  let teamRows='';
  if(JY_)teamRows='<div class="hsub">Tim</div>'+st.teams.map((T,t)=>{
    const tag=T.bot?'<span class="htag">🤖 Tim bot</span>':T.auto?'<span class="htag auto">🤖 Dimainkan bot</span>':'';
    const btn=T.bot?'':T.auto?`<button class="btn sm" data-act="hthuman" data-i="${t}">🙋 Kembalikan</button>`:`<button class="btn sm" data-act="htbot" data-i="${t}">🤖 Ganti bot</button>`;
    return `<div class="hrow"><div class="hname"><b>${esc(T.name)}</b> <span class="mute">${T.bot?'':T.members.map(i=>esc(nm(st,i))).join(', ')}</span> ${tag}</div><div class="hbtn">${btn}</div></div>`;}).join('');
  const rows=st.players.map((p,i)=>{
    if(p.bot)return '';
    const tag=p.auto?'<span class="htag auto">🤖 Otomatis</span>':'', crown=p.id===st.host?' 👑':'', you=i===me?' <span class="mute">(kamu)</span>':'';
    const wait=pend.includes(i)?' <span class="htag turnt">⏳ ditunggu</span>':'';
    let btns='';
    if(!JY_)btns+=p.auto?`<button class="btn sm" data-act="hhuman" data-i="${i}">🙋 Kembalikan</button>`:`<button class="btn sm" data-act="hbot" data-i="${i}">🤖 Ganti bot</button>`;
    if(p.id!==st.host)btns+=`<button class="btn sm" data-act="hhost" data-i="${i}">👑 Jadikan tuan rumah</button>`;
    return `<div class="hrow ${pend.includes(i)?'cur':''}"><div class="hname"><b>${esc(nm(st,i))}</b>${crown}${you} ${tag}${wait}</div><div class="hbtn">${btns}</div></div>`;}).join('');
  const help=JY_?'🤖 <b>Ganti bot</b>: rencana dan jualan tim itu dimainkan bot; kasnya tetap milik tim. Anggota tim bisa mengambil alih lagi lewat tombol “Ambil alih”.'
    :'🤖 <b>Ganti bot</b>: pemain itu tidak lagi ditunggu. Kalau tinggal dia yang belum memilih, pilihan bawaan diambil otomatis (sama seperti saat waktu habis). Dia bisa mengambil alih lagi lewat tombol “Ambil alih”.';
  openModal(`<h3>⚙️ Atur meja</h3><p class="mute" style="font-size:13.5px;margin:0 0 10px">Hanya tuan rumah yang melihat menu ini. Semua pemain mendapat pemberitahuan setiap ada perubahan.</p>
    <div class="hacts">${st.paused?'<button class="btn pri" data-act="hresume">▶ Lanjutkan permainan</button>':'<button class="btn" data-act="hpause">⏸️ Jeda permainan</button>'}
    <button class="btn" data-act="hskip" ${st.paused?'disabled':''}>${skipLbl}</button></div>
    <div class="hlist">${teamRows}<div class="hsub">Pemain</div>${rows}</div>
    <div class="mute" style="font-size:12.5px;line-height:1.5;margin-top:8px">${help} 👑 <b>Jadikan tuan rumah</b>: kendali meja pindah ke pemain itu.</div>
    <div class="mbtns"><button class="btn" data-act="close">Tutup</button></div>`);
}
function hostConfirm(i){""")
rep("    case 'hhost':hostConfirm(+el.dataset.i);break;",
    """    case 'hhost':hostConfirm(+el.dataset.i);break;
    case 'htbot':hostDo('tbot',+el.dataset.i,'🤖 Tim diganti bot');break;
    case 'hthuman':hostDo('thuman',+el.dataset.i,'🙋 Tim kembali dimainkan anggotanya');break;""")
rep(".afkbar.paused{border-color:#6aa7ff}",".afkbar.paused{border-color:#6aa7ff}\n.hsub{font-size:12.5px;font-weight:700;opacity:.75;margin:6px 2px 0;text-transform:uppercase;letter-spacing:.4px}")
open(F,'w').write(s)
print('ok host2')
