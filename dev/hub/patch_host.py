# Kontrol tuan rumah meja online (Saudagar Permata & Pemukim Nusantara):
# jeda/lanjutkan, lewati giliran, ganti pemain (termasuk tuan rumah) dengan bot, pindahkan tuan rumah
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b):
    global s
    n=s.count(a); assert n==1,(n,a[:90]); s=s.replace(a,b)

PAUSED="'⏸️ Permainan sedang dijeda tuan rumah'"
# --- penjaga jeda ---
rep("function doMove(st,pi,mv){\n  const t0=st.turn,",
    "function doMove(st,pi,mv){\n  if(st.paused)fail("+PAUSED+");\n  const t0=st.turn,")
rep("function pmAct(st,pi,mv){\n  if(st.status!=='playing')fail('Permainan sudah selesai');",
    "function pmAct(st,pi,mv){\n  if(st.status!=='playing')fail('Permainan sudah selesai');\n  if(st.paused)fail("+PAUSED+");")
rep("return st&&st.timer&&st.status==='playing'&&st.turnAt?st.turnAt+st.timer*1000-Date.now():null;}",
    "return st&&st.timer&&st.status==='playing'&&st.turnAt?st.turnAt+st.timer*1000-(st.paused?st.paused.at:Date.now()):null;}")
rep("  const st=cur.st; if(st.status!=='playing')return;\n  const p=st.players[st.turn]; if(!p||!(p.bot||p.auto)){return;}",
    "  const st=cur.st; if(st.status!=='playing'||st.paused)return;\n  const p=st.players[st.turn]; if(!p||!(p.bot||p.auto)){return;}")
rep("  const st=cur.st; if(st.status!=='playing')return; const nx=pmBotNext(st); if(!nx)return;\n  const key=cur.gid+':'+st.v; if(ui.obKey===key)return;",
    "  const st=cur.st; if(st.status!=='playing'||st.paused)return; const nx=pmBotNext(st); if(!nx)return;\n  const key=cur.gid+':'+st.v; if(ui.obKey===key)return;")
rep("function afkResolve(s){\n  const a=s.afk; if(!a)throw NOOP;",
    "function afkResolve(s){\n  const a=s.afk; if(!a||s.paused)throw NOOP;")
# bilah jeda ditampilkan lewat bilah AFK
rep("function afkBarHTML(st){\n  const me=meIdx(st); if(me<0)return '';",
    """function afkBarHTML(st){
  if(st.paused){const host=st.host===myId;
    return `<div class="afkbar top paused"><span>⏸️ <b>Permainan dijeda</b> oleh tuan rumah${host?'':' ('+esc(hostName(st))+')'}.</span>${host?'<button class="btn sm pri" data-act="hresume">▶ Lanjutkan</button>':''}</div>`;}
  const me=meIdx(st); if(me<0)return '';""")

# --- logika & UI ---
rep("function afkCommit(fn,okMsg){","""function hostName(st){const i=st.players.findIndex(q=>q.id===st.host);return i>=0?nm(st,i):'tuan rumah';}
function hostCan(){const st=cur&&cur.st;return !!(st&&!cur.local&&online==='on'&&canWrite!==false&&afkGameOk(st)&&st.host===myId);}
function hostOp(s,kind,i){
  if(s.host!==myId)fail('Hanya tuan rumah yang bisa mengatur meja');
  if(s.status!=='playing')fail('Permainan sudah selesai');
  const me=meIdx(s), who=me>=0?nm(s,me):'Tuan rumah', note=m=>{s.afkNote={m,at:Date.now()};};
  if(kind==='pause'){if(s.paused)throw NOOP;s.paused={at:Date.now(),by:myId};note('⏸️ '+who+' menjeda permainan');return;}
  if(kind==='resume'){if(!s.paused)throw NOOP;const d=Date.now()-s.paused.at;if(s.turnAt)s.turnAt+=d;if(s.afk&&s.afk.until)s.afk.until+=d;s.paused=null;note('▶ '+who+' melanjutkan permainan');return;}
  if(kind==='skip'){if(s.paused)fail('Lanjutkan permainan dulu sebelum melewati giliran');const t=s.turn,name=nm(s,t);
    if(s.game==='pemukim')pmTimeoutRun(s);else doMove(s,t,{type:'pass'});
    note('⏭ '+who+' melewati giliran '+name);return;}
  const P=s.players[i]; if(!P)fail('Pemain tidak ditemukan');
  if(kind==='bot'){if(P.bot||P.auto)throw NOOP;P.auto=true;if(s.afk&&s.afk.tid===P.id)s.afk=null;note('🤖 '+nm(s,i)+' kini dimainkan bot (diatur tuan rumah)');return;}
  if(kind==='human'){if(!P.auto)throw NOOP;delete P.auto;note('🙋 '+nm(s,i)+' kembali bermain sendiri');return;}
  if(kind==='host'){if(P.bot)fail('Bot tidak bisa jadi tuan rumah');if(P.id===myId)throw NOOP;s.host=P.id;note('👑 '+nm(s,i)+' kini menjadi tuan rumah');return;}
  fail('Perintah tidak dikenal');
}
function hostDo(kind,i,ok){closeModal();commitOnline(s=>hostOp(s,kind,i)).then(()=>{if(ok)toast(ok);}).catch(e=>{if(!e||!e.noop)toast((e&&e.message)||'Gagal, coba lagi');});}
function hostModal(){
  if(!hostCan())return;
  const st=cur.st, t=st.turn, me=meIdx(st);
  const rows=st.players.map((p,i)=>{
    const tag=p.bot?'<span class="htag">🤖 Bot</span>':p.auto?'<span class="htag auto">🤖 Autopilot</span>':'';
    const crown=p.id===st.host?' 👑':'', you=i===me?' <span class="mute">(kamu)</span>':'';
    let btns='';
    if(!p.bot){btns+=p.auto?`<button class="btn sm" data-act="hhuman" data-i="${i}">🙋 Kembalikan</button>`:`<button class="btn sm" data-act="hbot" data-i="${i}">🤖 Ganti bot</button>`;
      if(p.id!==st.host)btns+=`<button class="btn sm" data-act="hhost" data-i="${i}">👑 Jadikan tuan rumah</button>`;}
    return `<div class="hrow ${i===t?'cur':''}"><div class="hname"><span class="ordn ${i===me?'me':''}">${i+1}</span><b>${esc(nm(st,i))}</b>${crown}${you} ${tag}${i===t?' <span class="htag turnt">▶ giliran</span>':''}</div><div class="hbtn">${btns}</div></div>`;}).join('');
  openModal(`<h3>⚙️ Atur meja</h3><p class="mute" style="font-size:13.5px;margin:0 0 10px">Hanya tuan rumah yang melihat menu ini. Semua pemain mendapat pemberitahuan setiap ada perubahan.</p>
    <div class="hacts">${st.paused?'<button class="btn pri" data-act="hresume">▶ Lanjutkan permainan</button>':'<button class="btn" data-act="hpause">⏸️ Jeda permainan</button>'}
    <button class="btn" data-act="hskip" ${st.paused?'disabled':''}>⏭ Lewati giliran ${esc(nm(st,t))}</button></div>
    <div class="hlist">${rows}</div>
    <div class="mute" style="font-size:12.5px;line-height:1.5;margin-top:8px">🤖 <b>Ganti bot</b>: giliran pemain itu dimainkan bot dan poinnya tetap miliknya. Pemain bisa mengambil alih lagi lewat tombol “Ambil alih”. 👑 <b>Jadikan tuan rumah</b>: kendali meja pindah ke pemain itu.</div>
    <div class="mbtns"><button class="btn" data-act="close">Tutup</button></div>`);
}
function hostConfirm(i){
  const st=cur.st;
  openModal(`<h3>👑 Pindahkan tuan rumah?</h3><p style="font-size:14.5px;margin:0 0 8px"><b>${esc(nm(st,i))}</b> akan menjadi tuan rumah. Setelah itu kamu tidak bisa lagi menjeda, melewati giliran, atau mengganti pemain dengan bot.</p>
    <div class="mbtns"><button class="btn" data-act="hostset">Batal</button><button class="btn pri" data-act="hhostok" data-i="${i}">👑 Pindahkan</button></div>`);
}
function hostTick(){const b=$('#hostBtn');if(!b)return;const on=view==='table'&&hostCan();if(b._on!==on){b._on=on;b.style.display=on?'':'none';}
  if(!on&&$('#modal .hlist')&&!(cur&&cur.st&&cur.st.host===myId))closeModal();}
setInterval(hostTick,500);
function afkCommit(fn,okMsg){""")

# tombol di header
rep('<button class="btn sm" id="themeBtn" data-act="theme" aria-label="Ganti tema">',
    '<button class="btn sm hostbtn" id="hostBtn" data-act="hostset" style="display:none" aria-label="Atur meja">⚙️ <span class="lbl">Atur meja</span></button>\n      <button class="btn sm" id="themeBtn" data-act="theme" aria-label="Ganti tema">')

# klik
rep("    case 'afkpl':afkPlModal(+el.dataset.i);break;",
    """    case 'afkpl':afkPlModal(+el.dataset.i);break;
    case 'hostset':hostModal();break;
    case 'hpause':hostDo('pause',0,'⏸️ Permainan dijeda');break;
    case 'hresume':hostDo('resume',0,'▶ Permainan dilanjutkan');break;
    case 'hskip':hostDo('skip',0,'⏭ Giliran dilewati');break;
    case 'hbot':hostDo('bot',+el.dataset.i,'🤖 Pemain diganti bot');break;
    case 'hhuman':hostDo('human',+el.dataset.i,'🙋 Pemain kembali bermain sendiri');break;
    case 'hhost':hostConfirm(+el.dataset.i);break;
    case 'hhostok':hostDo('host',+el.dataset.i,'👑 Tuan rumah dipindahkan');break;""")

rep("</style>","""/* --- kontrol tuan rumah --- */
.hostbtn{border-color:#b98f2c!important}
.hacts{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}.hacts .btn{flex:1 1 180px}
.hlist{display:flex;flex-direction:column;gap:6px}
.hrow{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 10px;padding:8px 10px;border:1px solid var(--line);border-radius:12px;background:var(--panel2)}
.hrow.cur{border-color:#ffd25e;box-shadow:0 0 0 1px #ffd25e}
.hname{font-size:14.5px}.hbtn{display:flex;gap:6px;flex-wrap:wrap}
.htag{font-size:11.5px;padding:2px 7px;border-radius:999px;background:var(--panel);border:1px solid var(--line);white-space:nowrap}
.htag.auto{border-color:#b98f2c}.htag.turnt{border-color:#ffd25e}
.afkbar.paused{border-color:#6aa7ff}
</style>""")
open(F,'w').write(s)
print('ok host')
