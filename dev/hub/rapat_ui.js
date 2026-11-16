/* ================= HUB · MENU GAME & RAPAT RAHASIA DIREKSI ================= */
const HUB_INFO={
  permata:{icon:'💎',name:'Saudagar Permata',ply:'2–4 pemain · Duel 2',dur:'20–40 menit',kind:'Strategi ekonomi',desc:'Kumpulkan permata, beli kartu tambang sampai istana, dan raih dukungan pahlawan nasional. Bisa lawan bot.',mk:[['MK02','investasi bertahap']]},
  rapat:{icon:'🏛️',name:'Rapat Rahasia Direksi',ply:'5–10 pemain',dur:'20–30 menit',kind:'Deduksi sosial · mirip Avalon',desc:'Direksi menjalankan 5 proyek dari kasus kuliah, tapi diam-diam ada Oknum yang ingin proyeknya gagal. Siapa yang bisa dipercaya?',mk:[['MK01','power & politics'],['MK05','keputusan kelompok']]},
  pemukim:{icon:'🏝️',name:'Pemukim Nusantara',ply:'3–4 pemain · bisa lawan bot',dur:'45–90 menit',kind:'Strategi & dagang · aturan Catan',desc:'Bangun pemukiman, jalan, dan kota di pulau acak. Hasil bumi keluar sesuai lemparan dadu. Berdagang, hindari perampok, dan raih 10 poin duluan.',mk:[['MK02','investasi & ROI'],['MK04','rantai pasok']]},
  werewolf:{icon:'🐺',name:'Werewolf',ply:'Satu Malam 3–10 · Klasik 6–20',dur:'10–60 menit',kind:'Deduksi sosial · 2 mode',desc:'<b>Satu Malam</b>: cepat, kartu peran bisa tertukar diam-diam, voting sekali. <b>Klasik</b>: banyak malam & siang untuk grup besar (sampai 20 orang), aplikasi jadi moderatornya.',mk:[['MK05','keputusan dengan info tak lengkap']]},
  sandi:{icon:'🕵️',name:'Sandi Syndicate',ply:'4–8 pemain · 2 tim',dur:'15–20 menit',kind:'Tebak kata · mirip Codenames',desc:'Ketua tim memberi petunjuk satu kata untuk menebak istilah materi MK di papan 5×5.',mk:[['MK01–06','istilah materi']],soon:true}
};
function mkChip(mk,t){const c=(MK_INFO[mk]||{}).c||'#8a7fc0';return `<span class="mkchip" style="--mk:${c}">${esc(mk)}${t?' · '+esc(t):''}</span>`;}
function hubGridHTML(){
  const card=k=>{const g=HUB_INFO[k];let b='';
    if(k==='permata')b=`${EDITION!=='latihan'?'<button class="btn pri sm" data-act="hubnew" data-g="klasik">Buat meja</button>':''}<button class="btn sm" data-act="localSetup">🤖 Lawan bot</button><button class="btn sm" data-act="tutorial" data-w="klasik">🎬 Tutorial</button>`;
    else if(k==='pemukim')b=`${EDITION!=='latihan'?'<button class="btn pri sm" data-act="hubnew" data-g="pemukim">Buat meja</button>':''}<button class="btn sm" data-act="pmlocal">🤖 Lawan bot</button><button class="btn sm" data-act="tutorial" data-w="pemukim">📖 Cara main</button>`;
    else if(k==='rapat'||k==='werewolf')b=EDITION==='latihan'?`<button class="btn sm" data-act="tutorial" data-w="${k}">📖 Cara main</button>${LEAGUE_URL?`<a class="btn sm" href="${LEAGUE_URL}" target="_blank" rel="noopener">Khusus Liga online →</a>`:''}`
      :k==='werewolf'?`<button class="btn pri sm" data-act="hubnew" data-g="werewolf">Meja Satu Malam</button><button class="btn pri sm" data-act="hubnew" data-g="wwk">Meja Klasik</button><button class="btn sm" data-act="tutorial" data-w="werewolf">📖 Cara main</button>`
      :`<button class="btn pri sm" data-act="hubnew" data-g="${k}">Buat meja</button><button class="btn sm" data-act="tutorial" data-w="${k}">📖 Cara main</button>`;
    else b='<span class="pill soonpill">Segera hadir</span>';
    return `<div class="hubcard ${g.soon?'soon':''}"><div class="hh"><span class="hi">${g.icon}</span><div><b>${g.name}</b><div class="bd">${g.kind}</div></div></div>
      <div class="hmeta"><span>👥 ${g.ply}</span><span>⏱ ${g.dur}</span></div><p class="hd">${g.desc}</p>
      <div class="hmk">${g.mk.map(x=>mkChip(x[0],x[1])).join('')}</div><div class="row hbt">${b}</div></div>`;};
  return `<section class="panel hubp"><div class="row" style="justify-content:space-between"><h2 style="font-size:22px">🎲 Pilih permainan</h2><span class="bd">Game papan online untuk syndicate P3MD</span></div>
    <div class="hubgrid">${['permata','pemukim','rapat','werewolf','sandi'].map(card).join('')}</div></section>`;
}
const VLAB={klasik:'💎 Klasik',duel:'⚔️ Duel',pemukim:'🏝️ Pemukim',rapat:'🏛️ Rapat Rahasia',werewolf:'🐺 Werewolf',wwk:'🐺 WW Klasik',sandi:'🕵️ Sandi'};
function vOf(r){return ['duel','sandi','rapat','werewolf','pemukim','wwk'].includes(r&&r.variant)?r.variant:'klasik';}
function hubV(r){const v=vOf(r);return v==='rapat'||v==='werewolf'||v==='sandi'||v==='wwk';}
function roleName(v,c){return v==='wwk'?(WK_ROLES[c]?WK_ROLES[c].i+' '+WK_ROLES[c].n:''):v==='werewolf'?(WW_ROLES[c]?WW_ROLES[c].i+' '+WW_ROLES[c].n:''):(ROLE[c]?ROLE[c].n:'');}
const ROLE_UI={
  I:{icon:'🛡️',s:'i',goal:'Pastikan <b>3 proyek berhasil</b>. Kamu tidak tahu siapa Oknum, jadi perhatikan siapa menyetujui tim yang gagal dan siapa yang ikut di proyek gagal.'},
  A:{icon:'🔍',s:'i',goal:'Kamu <b>tahu siapa Oknum</b>. Arahkan diskusi diam-diam supaya Oknum tidak masuk tim, tapi jangan sampai ketahuan: kalau 3 proyek berhasil, Dalang akan mencoba menebakmu.'},
  O:{icon:'🦹',s:'o',goal:'Gagalkan <b>3 proyek</b>. Masuk ke tim proyek lalu kirim kartu Sabotase, atau buat rapat buntu (5 penolakan). Pura-pura jadi Integritas.'},
  D:{icon:'🎭',s:'o',goal:'Pemimpin Oknum. Gagalkan 3 proyek. Kalau Integritas berhasil 3 proyek, kamu dapat <b>satu tebakan</b>: tunjuk Auditor Internal. Benar → Oknum menang.'}
};
function rapatKnown(st,mi){
  if(mi<0||!st.rk)return {};
  const r=rapatRoles(st), me=r[mi], out={};
  if(me==='A')r.forEach((x,i)=>{if(i!==mi&&ROLE[x].s==='O')out[i]='Oknum';});
  if(me==='O'||me==='D')r.forEach((x,i)=>{if(i!==mi&&ROLE[x].s==='O')out[i]=x==='D'?'Dalang':'Oknum';});
  return out;
}
function teamNames(st,t){return (t||[]).map(i=>'<b>'+esc(nm(st,i))+'</b>').join(', ')||'—';}
function openRoleModal(first){
  const st=cur.st, mi=meIdx(st); if(mi<0||!st.rk)return;
  const r=rapatRoles(st)[mi], R=ROLE_UI[r], kn=rapatKnown(st,mi), ks=Object.keys(kn);
  const names=ks.map(i=>`<b>${esc(nm(st,+i))}</b>${kn[i]==='Dalang'?' <span class="rtag o">Dalang</span>':''}`).join(', ');
  let know='';
  if(r==='A')know=`<p class="rknow">🔎 Oknum di rapat ini: ${names||'—'}</p>`;
  else if(r==='O'||r==='D')know=`<p class="rknow">🤝 Rekan Oknum: ${names||'— (kamu sendirian)'}</p>`;
  else know=`<p class="rknow mute">Kamu tidak punya informasi rahasia. Andalkan diskusi dan pola voting.</p>`;
  const n=st.players.length, k=RAPAT_OKNUM[n];
  openModal(`${first?'<p class="bd" style="text-align:center;margin:0 0 8px">🤫 Jangan tunjukkan layar ini ke orang lain</p>':''}
    <div class="rolecard ${R.s}"><div class="ri">${R.icon}</div><div class="bd" style="letter-spacing:2px;font-weight:700">PERAN RAHASIAMU</div>
      <h3 style="font-size:26px;margin:2px 0">${ROLE[r].n}</h3><div class="rtag ${R.s}">${R.s==='o'?'Pihak Oknum':'Pihak Integritas'}</div>
      <p style="font-size:14.5px;line-height:1.55;margin:12px 0 0">${R.goal}</p>${know}</div>
    <p class="bd" style="margin:10px 0 0;text-align:center">${n} pemain: ${n-k} Integritas vs ${k} Oknum${st.special!==false?' · ada Auditor Internal & Dalang':''}. Peran bisa dilihat lagi lewat tombol 🎭 Peranku.</p>
    <div class="mbtns"><button class="btn pri" data-act="close">Mengerti</button></div>`);
}
function rapatRules(){
  const comp=[5,6,7,8,9,10].map(n=>`<tr><td>${n}</td><td>${n-RAPAT_OKNUM[n]}</td><td>${RAPAT_OKNUM[n]}</td><td>${RAPAT_SIZES[n].map((x,j)=>n>=7&&j===3?x+'*':x).join(' · ')}</td></tr>`).join('');
  return `<h3>🏛️ Rapat Rahasia Direksi (5–10 pemain)</h3>
  <p>Direksi menjalankan <b>5 proyek</b> yang diambil dari kasus kuliah. Sebagian besar pemain adalah <b>Tim Integritas</b> yang ingin proyek berhasil. Beberapa pemain adalah <b>Oknum</b> yang diam-diam ingin proyek gagal. Sesama Oknum saling kenal, sementara Integritas tidak tahu siapa Oknum.</p>
  <p><b>Tiap proyek berjalan begini:</b></p>
  <ul><li><b>Usulkan tim.</b> Pemimpin rapat 👑 memilih anggota tim proyek. Jumlah anggotanya tertera di tiap proyek, dan pemimpin boleh memasukkan dirinya sendiri.</li>
  <li><b>Voting.</b> Semua pemain memilih Setuju atau Tolak, dan suara dibuka bersamaan. Kalau lebih dari separuh setuju, tim berangkat. Kalau ditolak, kepemimpinan pindah ke pemain berikutnya. <b>5 penolakan berturut-turut</b> dalam satu proyek membuat Oknum menang.</li>
  <li><b>Jalankan proyek.</b> Anggota tim diam-diam mengirim kartu <b>Dukung</b> atau <b>Sabotase</b>. Integritas wajib Dukung, Oknum bebas memilih. Satu sabotase sudah membuat proyek gagal. Yang diumumkan hanya <b>jumlah</b> sabotase, bukan pelakunya.</li></ul>
  <p><b>Menang:</b> kalau 3 proyek berhasil, Integritas menang. Kalau 3 proyek gagal, Oknum menang.</p>
  <p><b>Peran khusus</b> (bisa dimatikan tuan rumah untuk pemula):</p>
  <ul><li>🔍 <b>Auditor Internal</b> (Integritas): tahu siapa saja Oknum, tapi harus menyamar.</li>
  <li>🎭 <b>Dalang</b> (Oknum): kalau Integritas berhasil 3 proyek, Dalang menunjuk satu orang sebagai Auditor Internal. Kalau tebakannya benar, Oknum merebut kemenangan.</li></ul>
  <table class="rec" style="margin-top:6px"><tr><th>Pemain</th><th>Integritas</th><th>Oknum</th><th>Ukuran tim proyek 1–5</th></tr>${comp}</table>
  <p class="bd" style="margin:6px 0 0">* Untuk 7 pemain atau lebih, proyek ke-4 baru gagal kalau ada 2 sabotase.</p>
  <p class="mute">Main sambil ngobrol, di satu ruangan atau lewat telepon/WA call. Serunya ada di debat: siapa yang menyetujui tim yang gagal?</p>`;
}
function renderWaitingHub(){
  const st=cur.st, mi=meIdx(st), isHost=st.host===myId, G=GAMES[st.game], n=st.players.length;
  refreshNames(st.players.map(p=>p.id));
  const seats=st.players.map((p,i)=>`<div class="seat"><span class="dot ${p.bot||ONLINE.has(p.id)?'on':''}"></span><b>${p.bot?'🤖':''}${esc(nm(st,i))}</b>${p.bot?`<span class="bd">${LVNAME[p.level]||''}</span>${isHost?`<button class="btn sm" style="margin-left:auto" data-act="rmbot" data-id="${p.id}">✕</button>`:''}`:''}${p.id===st.host?'<span class="crown">· tuan rumah</span>':''}${i===mi?'<span class="mute">(kamu)</span>':''}</div>`).join('')
    +(n<G.max?`<div class="seat emptyseat">${n<G.min?`Butuh ${G.min-n} pemain lagi untuk mulai · muat sampai ${G.max} orang`:`Masih ada ${G.max-n} kursi kosong (maks. ${G.max} orang)`}</div>`:'');
  const canAct=canWrite!==false&&myId;
  const WK=st.game==='wwk', WW=st.game==='werewolf'||WK, PMG=st.game==='pemukim';
  const comp=PMG?`${n<G.min?`Butuh minimal ${G.min} pemain (sekarang ${n}). Ajak teman atau isi kursi kosong dengan bot.`:`${n} pemain siap. Urutan giliran diacak saat mulai.`}`
    +(isHost&&n<G.max?`<div class="row" style="margin-top:10px;align-items:center;gap:8px"><button class="btn sm" data-act="addbot">🤖 Tambah bot</button><select id="obLv" class="ordsel"><option value="easy" ${ui.obLevel==='easy'?'selected':''}>Santai</option><option value="normal" ${!ui.obLevel||ui.obLevel==='normal'?'selected':''}>Normal</option><option value="hard" ${ui.obLevel==='hard'?'selected':''}>Sulit</option></select></div>`:'')
    :WK?wkCompHTML(st,isHost):WW?wwCompHTML(st,isHost):n>=G.min?`${n} pemain → <b>${n-RAPAT_OKNUM[n]} Integritas</b> vs <b>${RAPAT_OKNUM[n]} Oknum</b> · tim proyek ${RAPAT_SIZES[n].join('–')} orang${n>=7?' · proyek ke-4 butuh 2 sabotase':''}`:`Butuh minimal ${G.min} pemain untuk mulai (sekarang ${n}).`;
  $('#app').innerHTML=`<section class="panel" style="max-width:640px;margin:0 auto">
    <h2 style="font-size:24px">${G.icon} ${esc(st.name||'Meja')}</h2>
    <p class="mute" style="font-size:14px;margin:6px 0 0">${G.name} · ${G.min}–${G.max} pemain. Kirim link meja ini ke syndicate, teman langsung masuk ke meja.</p>
    ${shareBox(st)}
    <div class="seats">${seats}</div>
    <p class="bd" style="margin:2px 0 12px">${comp}</p>
    <div class="row">
      ${mi<0&&n<G.max&&canAct?'<button class="btn pri" data-act="join">Duduk di meja ini</button>':''}
      ${mi>=0&&!isHost?'<button class="btn" data-act="leave">Tinggalkan kursi</button>':''}
      ${isHost?`<button class="btn pri" data-act="start" ${n<G.min?'disabled':''}>${WW?'Mulai malam':PMG?'Mulai main':'Mulai rapat'}</button>`:''}
      <button class="btn" data-act="tutorial" data-w="${st.game}">📖 Cara main</button>
      ${(isHost||isOwnerFlag)?'<button class="btn danger sm" data-act="delete">Hapus meja</button>':''}
    </div>
    ${WW||PMG?'':`<div class="row" style="margin-top:12px;align-items:center;gap:8px"><span class="bd">🎭 Peran khusus:</span>
      ${isHost?`<label class="chk"><input type="checkbox" id="spSel" ${st.special!==false?'checked':''}> Auditor Internal &amp; Dalang</label>`:`<b>${st.special!==false?'Auditor Internal & Dalang':'Tanpa peran khusus'}</b>`}</div>`}
    <div class="row" style="margin-top:10px;align-items:center;gap:8px"><span class="bd">⏱ ${WK?'Waktu diskusi siang':WW?'Waktu diskusi pagi':PMG?'Waktu per giliran':'Waktu per tahap'}:</span>
      ${isHost?`<select id="tmrSel" class="ordsel">${timerOptions(st.timer||0)}</select>`:`<b>${timerLabel(st.timer||0)}</b>`}</div>
    <p class="hint" style="text-align:left">${WK?'Urutan duduk dan peran diacak saat mulai. Malam berakhir saat semua pemain hidup selesai. Siang hari voting terbuka.'+(st.timer?' Saat waktu diskusi habis, suara langsung dihitung.':''):PMG?'Pulau diacak saat mulai. Bot berjalan otomatis di gilirannya dan bisa diajak dagang.'+(st.timer?' Kalau waktu habis, giliran diakhiri otomatis.':''):WW?'Urutan duduk diacak saat mulai, lalu kartu peran dibagikan acak (3 sisanya di tengah). Malam berakhir saat semua sudah bertindak.'+(st.timer?' Saat waktu diskusi habis, suara langsung dihitung.':''):'Urutan duduk dan pemimpin rapat pertama diacak saat mulai. Peran rahasia dibagikan otomatis.'+(st.timer?' Kalau waktu habis, suara/kartu yang belum masuk dihitung Setuju/Dukung.':'')}</p>
    ${mi<0&&!isHost?'<p class="hint" style="text-align:left">Kamu bisa ikut sebelum tuan rumah memulai rapat.</p>':''}
  </section>`;
}
function rapatPending(st){
  if(st.status!=='playing')return [];
  if(st.game==='werewolf')return st.players.map((p,i)=>i).filter(i=>!(st.phase==='night'?st.done:st.voted).includes(i));
  if(st.game==='wwk'){if(st.phase==='hunter')return [st.hunter.p];return st.players.map((p,i)=>i).filter(i=>st.alive[i]&&(st.phase==='night'?!st.done.includes(i):st.votes[i]==null));}
  if(st.phase==='propose')return [st.leader];
  if(st.phase==='vote')return st.players.map((p,i)=>i).filter(i=>st.votes[i]==null);
  if(st.phase==='mission')return st.team.filter(i=>!st.played.includes(i));
  if(st.phase==='shoot')return [rapatRoles(st).indexOf('D')];
  return [];
}
function renderRapat(){
  const st=cur.st, mi=meIdx(st), n=st.players.length, roles=rapatRoles(st), mis=st.missions[Math.min(st.mi,4)], M=MISSIONS[mis.m];
  refreshNames(st.players.map(p=>p.id));
  const ended=st.status!=='playing', myRole=mi>=0?roles[mi]:null, side=myRole?ROLE[myRole].s:null;
  const kn=rapatKnown(st,mi), pend=rapatPending(st);
  const pkKey=st.mi+':'+st.rejects+':'+st.phase; if(ui.rpKey!==pkKey){ui.rpKey=pkKey;ui.rpick=[];ui.rtarget=null;}
  const canLead=!ended&&st.phase==='propose'&&mi===st.leader&&canWrite!==false;
  const canShoot=!ended&&st.phase==='shoot'&&myRole==='D'&&canWrite!==false;
  const lv=st.lastVote, showLV=lv&&st.phase!=='vote';
  const chips=st.players.map((p,i)=>{
    const lead=!ended&&i===st.leader&&st.phase!=='shoot', team=(st.phase==='vote'||st.phase==='mission')?st.team.includes(i):(canLead&&ui.rpick.includes(i));
    let tag='';
    if(ended&&st.reveal){const r=st.reveal[i];tag=`<span class="rtag ${ROLE[r].s==='O'?'o':'i'}">${ROLE_UI[r].icon} ${ROLE[r].n}</span>`;}
    else if(st.phase==='shoot'&&ROLE[roles[i]].s==='O')tag=`<span class="rtag o">${roles[i]==='D'?'🎭 Dalang':'🦹 Oknum'}</span>`;
    else if(kn[i])tag=`<span class="rtag o">${kn[i]==='Dalang'?'🎭 Dalang':'🦹 Oknum'}</span>`;
    else if(i===mi&&myRole)tag=`<span class="rtag ${side==='O'?'o':'i'}">${ROLE_UI[myRole].icon} kamu</span>`;
    let st2='';
    if(st.phase==='vote'&&!ended)st2=st.votes[i]!=null?'<span class="rbd">✔ sudah memilih</span>':'<span class="rbd">… memilih</span>';
    else if(st.phase==='mission'&&!ended&&st.team.includes(i))st2=st.played.includes(i)?'<span class="rbd">✔ kartu masuk</span>':'<span class="rbd">… menentukan</span>';
    else if(showLV&&lv.votes[i]!=null)st2=`<span class="rbd">${lv.votes[i]?'👍 setuju':'👎 tolak'} <span style="opacity:.7">(voting terakhir)</span></span>`;
    const act=canLead?`data-act="rpick" data-i="${i}"`:canShoot&&i!==mi?`data-act="rtgt" data-i="${i}"`:'';
    return `<div class="rpchip ${lead?'lead':''} ${team?'team':''} ${act?'pick':''} ${ui.rtarget===i&&canShoot?'tgt':''} ${i===mi?'me':''} ${pend.includes(i)?'pend':''}" ${act}>
      <div class="rh"><span class="dot ${ONLINE.has(p.id)?'on':''}"></span><span class="rno">${i+1}</span><b>${esc(nm(st,i))}</b>${i===mi?'<span class="mine" style="font-size:11px">(kamu)</span>':''}</div>
      <div class="rbadges">${lead?'<span class="rtag ld">👑 Pemimpin</span>':''}${team?'<span class="rtag tm">📋 Tim</span>':''}${tag}</div>${st2}</div>`;}).join('');
  const track=st.missions.map((m,j)=>{const X=MISSIONS[m.m], r=st.res[j];
    return `<div class="rmis ${r==='s'?'ok':r==='f'?'bad':(!ended&&j===st.mi)?'cur':''}" data-act="rmis" data-j="${j}"><div class="rn">${r==='s'?'✅':r==='f'?'❌':j+1}</div>
      <div class="rt">${esc(X[0])}</div>${mkChip(X[1],X[2])}<div class="rsz">👥 ${m.size}${m.need2?' · ⚠️ 2 sabotase':''}</div></div>`;}).join('');
  const rej=`<div class="rrej" title="5 penolakan berturut-turut = Oknum menang"><span class="bd">Penolakan:</span>${[0,1,2,3,4].map(k=>`<i class="${k<st.rejects?'on':''}"></i>`).join('')}<span class="bd">${st.rejects}/5</span></div>`;
  let head, act='';
  if(ended){head=`🏁 ${st.winner==='I'?'🛡️ Tim Integritas menang':'🦹 Oknum menang'}`;
    act=`<div>${esc(st.winBy||'')}.</div><button class="btn pri" data-act="showend">Lihat hasil &amp; semua peran</button>`;}
  else if(st.phase==='propose'){head=`👑 Proyek ${st.mi+1}: <b>${esc(nm(st,st.leader))}</b> menyusun tim ${mis.size} orang`;
    act=canLead?`<div><b>Kamu pemimpin rapat.</b> Ketuk <b>${mis.size} pemain</b> (boleh termasuk dirimu) untuk proyek “${esc(M[0])}”, lalu ajukan ke voting.</div>
      <div class="row"><button class="btn pri" data-act="rpropose" ${ui.rpick.length===mis.size?'':'disabled'}>Ajukan tim (${ui.rpick.length}/${mis.size})</button>${ui.rpick.length?'<button class="btn" data-act="rpickclr">Kosongkan</button>':''}</div>`
      :`<div>Menunggu <b>${esc(nm(st,st.leader))}</b> memilih ${mis.size} orang. Diskusikan siapa yang layak dipercaya!</div>`;}
  else if(st.phase==='vote'){const voted=n-pend.length, my=mi>=0?st.votes[mi]:null;
    head=`🗳 Voting tim proyek ${st.mi+1} · ${voted}/${n} sudah memilih`;
    act=`<div>Usulan <b>${esc(nm(st,st.leader))}</b>: ${teamNames(st,st.team)}.${st.rejects===4?' <b style="color:var(--bad)">⚠️ Kalau ditolak lagi, Oknum menang!</b>':''}</div>`
      +(mi>=0&&my==null&&canWrite!==false?'<div class="rbig"><button class="btn ok" data-act="rvote" data-y="1">👍 Setuju</button><button class="btn danger" data-act="rvote" data-y="0">👎 Tolak</button></div>'
       :mi>=0?`<div class="bd">Kamu memilih <b>${my?'👍 Setuju':'👎 Tolak'}</b>. Semua suara dibuka setelah semua memilih.</div>`:'');}
  else if(st.phase==='mission'){const inT=st.team.includes(mi), done=st.played.includes(mi);
    head=`🛠 Proyek ${st.mi+1} berjalan · ${st.played.length}/${st.team.length} kartu masuk`;
    act=`<div>Tim proyek “${esc(M[0])}”: ${teamNames(st,st.team)}.${mis.need2?' Proyek ini baru gagal kalau ada <b>2 sabotase</b>.':''}</div>`
      +(inT&&!done&&canWrite!==false?`<div class="rbig"><button class="btn ok" data-act="rplay" data-c="s">✅ Dukung proyek</button><button class="btn danger" data-act="rplay" data-c="f" ${side==='O'?'':'disabled'}>💣 Sabotase</button></div>${side!=='O'?'<div class="bd">Tim Integritas selalu mendukung proyek.</div>':'<div class="bd">Tidak ada yang tahu siapa mengirim kartu apa, hanya jumlah sabotasenya.</div>'}`
       :inT?'<div class="bd">Kartumu sudah masuk. Menunggu anggota lain…</div>':'<div class="bd">Menunggu tim proyek mengirim kartu secara rahasia…</div>');}
  else if(st.phase==='shoot'){const d=roles.indexOf('D');head='🎯 3 proyek berhasil, tapi Dalang punya satu tebakan';
    act=canShoot?`<div><b>Kamu Dalang.</b> Ketuk satu pemain yang kamu curigai sebagai <b>Auditor Internal</b>. Tebakan benar → Oknum menang. Rekan Oknum boleh ikut berdiskusi.</div><button class="btn danger" data-act="rshootok" ${ui.rtarget!=null?'':'disabled'}>🎯 Tuduh ${ui.rtarget!=null?esc(nm(st,ui.rtarget)):'…'}</button>`
      :`<div>Oknum kini terbuka. <b>${esc(nm(st,d))}</b> (Dalang) sedang menebak siapa Auditor Internal. ${myRole==='A'?'Tetap tenang! 😶':'Integritas boleh berusaha mengecoh.'}</div>`;}
  const lvHTML=lv?`<div class="rbd">🗳 Voting terakhir · proyek ${lv.mi+1}, usulan ${esc(nm(st,lv.leader))}: <b style="color:${lv.ok?'var(--ok)':'var(--bad)'}">${lv.ok?'DISETUJUI':'DITOLAK'}</b> · 👍 ${Object.keys(lv.votes).filter(k=>lv.votes[k]).map(k=>esc(nm(st,+k))).join(', ')||'—'} · 👎 ${Object.keys(lv.votes).filter(k=>!lv.votes[k]).map(k=>esc(nm(st,+k))).join(', ')||'—'}</div>`:'';
  const mh=(st.mhist||[]).map(h=>`<div class="rbd">${h.ok?'✅':'❌'} Proyek ${h.mi+1} · ${esc(MISSIONS[st.missions[h.mi].m][0])}: ${h.team.map(i=>esc(nm(st,i))).join(', ')} · <b>${h.fails} sabotase</b></div>`).join('');
  const logs=st.log.slice(-16).reverse().map(l=>`<div>${l.p>=0?`<b>${esc(nm(st,l.p))}</b> `:''}${esc(l.m)}</div>`).join('');
  const isHost=st.host===myId;
  $('#app').innerHTML=`<div class="rp-wrap">
    <section class="panel">
      <div class="turnbar"><div class="who"><span class="pill playing" style="margin:0 6px 0 0">🏛️ RAPAT</span>${head}${timerHTML(st)}</div>
        <div class="row" style="gap:6px">${mi>=0?'<button class="btn sm" data-act="myrole">🎭 Peranku</button>':'<span class="bd">👀 Menonton</span>'}<button class="btn sm" data-act="tutorial" data-w="rapat">📖</button></div></div>
      <div class="rmis-row">${track}</div>
      <div class="row" style="justify-content:space-between;margin-top:10px">${rej}<span class="bd">✅ ${st.res.filter(x=>x==='s').length} berhasil · ❌ ${st.res.filter(x=>x==='f').length} gagal</span></div>
    </section>
    <section class="panel ract">${act}</section>
    <section class="panel"><div class="rpl">${chips}</div><div style="margin-top:10px;display:grid;gap:4px">${showLV?'':lvHTML}${mh}</div>
      ${(st.vhist||[]).length?'<button class="btn sm" style="margin-top:8px" data-act="rvhist">📊 Riwayat voting</button>':''}
      ${isHost&&!ended?'<button class="btn sm" style="margin-top:8px;margin-left:6px" data-act="rforce" title="Untuk pemain yang terputus atau tidak merespons">⏩ Lanjutkan paksa</button>':''}</section>
    <details class="panel log" ${ui.logOpen?'open':''} ontoggle="ui.logOpen=this.open"><summary style="font-family:Fraunces,serif;font-weight:600;font-size:15px;cursor:pointer">Catatan rapat</summary>${logs}</details>
  </div>`;
  if(!ended&&mi>=0){ui.roleShown=ui.roleShown||{};if(!ui.roleShown[cur.gid]){ui.roleShown[cur.gid]=true;setTimeout(()=>{if(cur&&cur.st&&isHubGame(cur.st)&&cur.st.status==='playing'&&!modalOpen())openRoleModal(true);},400);}}
  maybeEndPopup(st);
}
function missionModal(j){
  const st=cur.st, m=st.missions[j], X=MISSIONS[m.m], h=(st.mhist||[]).find(x=>x.mi===j), r=st.res[j];
  openModal(`<h3>Proyek ${j+1}: ${esc(X[0])}</h3><div style="margin:6px 0">${mkChip(X[1],X[2])} <span class="bd">${esc((MK_INFO[X[1]]||{}).full||'')}</span></div>
    <p style="font-size:14.5px;line-height:1.55;margin:6px 0">${esc(X[3])}</p>
    <p class="bd" style="margin:0">👥 Tim ${m.size} orang · gagal bila ada ${m.need2?'<b>2</b>':'1'} sabotase${r?` · hasil: <b>${r==='s'?'✅ berhasil':'❌ gagal'}</b>`:''}</p>
    ${h?`<p class="bd" style="margin:6px 0 0">Tim: ${h.team.map(i=>esc(nm(st,i))).join(', ')} (usulan ${esc(nm(st,h.leader))}) · ${h.fails} sabotase</p>`:''}
    <div class="mbtns"><button class="btn pri" data-act="close">Tutup</button></div>`);
}
function voteHistModal(){
  const st=cur.st, V=st.vhist||[];
  openModal(`<h3>📊 Riwayat voting</h3><p class="bd" style="margin:0 0 8px">Pola voting adalah petunjuk terbaik untuk menebak Oknum.</p>
    <div style="overflow-x:auto"><table class="rec vh"><tr><th>Proyek</th><th>Pemimpin</th><th>Tim</th><th>Hasil</th>${st.players.map((p,i)=>`<th title="${esc(nm(st,i))}">${i+1}</th>`).join('')}</tr>
    ${V.map(v=>`<tr><td>${v.mi+1}</td><td>${esc(nm(st,v.leader))}</td><td style="text-align:left">${v.team.map(i=>esc(nm(st,i))).join(', ')}</td><td>${v.ok?'✅':'❌'}</td>${st.players.map((p,i)=>`<td>${v.votes[i]?'👍':'👎'}</td>`).join('')}</tr>`).join('')}</table></div>
    <p class="bd" style="margin:6px 0 0">Nomor kolom = nomor kursi: ${st.players.map((p,i)=>`${i+1}. ${esc(nm(st,i))}`).join(' · ')}</p>
    <div class="mbtns"><button class="btn pri" data-act="close">Tutup</button></div>`);
}
function openHubEnd(){
  const st=cur.st; if(!st||st.status!=='ended')return;
  if(st.game==='werewolf')return openWWEnd();
  if(st.game==='pemukim')return openPmEnd();
  if(st.game==='wwk')return openWKEnd();
  const mi=meIdx(st), w=hubWinners(st), rv=st.reveal||rapatRoles(st), I=st.winner==='I';
  const title=mi<0?(I?'Tim Integritas menang':'Oknum menang'):w[mi]?'Pihakmu menang! 🎉':'Pihakmu kalah';
  const list=st.players.map((p,i)=>({i,r:rv[i]})).sort((a,b)=>(w[b.i]-w[a.i])||(a.i-b.i)).map(x=>`<div class="rki ${w[x.i]?'win':''} ${x.i===mi?'me':''}"><span class="pos">${ROLE_UI[x.r].icon}</span><span class="nm">${esc(nm(st,x.i))}${x.i===mi?' <span class="mine" style="font-size:12px">(kamu)</span>':''}<div class="bd" style="font-weight:400">${ROLE[x.r].n}${st.shot===x.i?' · 🎯 dituduh Dalang':''}</div></span><span class="pt" style="font-size:15px">${w[x.i]?'🏆':''}</span></div>`).join('');
  openModal(`<div class="endm"><div class="big">${I?'🛡️':'🦹'}</div><h3>${title}</h3><p class="why"><b>${I?'Tim Integritas':'Oknum'}</b> menang: ${esc(st.winBy||'')}.</p>
    <div class="rkl">${list}</div>
    <p class="bd" style="margin:10px 0 0">Tercatat di 📜 Riwayat dan rekor 👤 Profil. Rapat Rahasia belum menambah poin peringkat.</p>
    <div class="mbtns"><button class="btn" data-act="close">Lihat meja</button>${st.vhist&&st.vhist.length?'<button class="btn" data-act="rvhist">📊 Riwayat voting</button>':''}<button class="btn pri" data-act="lobby">Kembali ke lobi</button></div></div>`);
}
async function hubMove(mv){
  if(ui.busy)return; const st=cur.st, mi=meIdx(st);
  if(mi<0||canWrite===false)return toast('Kamu sedang menonton meja ini');
  try{hubAct(clone(st),mi,mv);}catch(e){return toast(e.message);}
  ui.busy=true; closeModal();
  try{await commitOnline(s=>{const k=meIdx(s);if(k<0)fail('Kamu bukan pemain meja ini');hubAct(s,k,mv);});}
  catch(e){if(!e.noop)toast(e.message||'Gagal menyimpan, coba lagi');}
  finally{ui.busy=false;}
}
function hubNotify(prev,d){
  if(!prev||prev.status!=='playing'||!isHubGame(d))return;
  if(d.game==='pemukim'){const mi=meIdx(d);(d.log||[]).slice((prev.log||[]).length&&d.log.length>=prev.log.length?prev.log.length:d.log.length).forEach(l=>{if(l.priv&&l.priv[mi]&&l.p!==mi)toast('🦹 '+nm(d,l.p)+': '+l.priv[mi]);});if(d.phase==='discard'&&d.disc&&d.disc[mi]&&prev.phase!=='discard')toast('🦹 Angka 7! Kamu harus membuang kartu');return;}
  if(d.game==='wwk'){const mi=meIdx(d);if(prev.phase!==d.phase||prev.day!==d.day||prev.night!==d.night){const L=d.log[d.log.length-1];if(L)toast(L.m);if(mi>=0&&prev.alive&&prev.alive[mi]&&!d.alive[mi])rankPop('down','☠️','Kamu tewas','Kamu boleh menonton, tapi jangan bocorkan peran',4200);}return;}
  if(d.game==='werewolf'){if(prev.phase==='night'&&d.phase==='day'){rankPop('up','☀️','Pagi tiba!','Diskusikan siapa serigala, lalu kunci suaramu',4200);}return;}
  const mi=meIdx(d), msgs=[];
  const pm=(prev.mhist||[]).length, dm=(d.mhist||[]).length;
  if(dm>pm){const h=d.mhist[dm-1];rankPop(h.ok?'up':'down',h.ok?'✅':'❌',`Proyek ${h.mi+1} ${h.ok?'berhasil':'gagal'}`,`“${esc(MISSIONS[d.missions[h.mi].m][0])}” · ${h.fails} kartu sabotase`,4200);}
  else if((d.vhist||[]).length>(prev.vhist||[]).length){const v=d.lastVote;msgs.push(`🗳 Tim ${v.ok?'DISETUJUI':'DITOLAK'} (${Object.values(v.votes).filter(Boolean).length} setuju)`);}
  if(d.status==='playing'&&(prev.phase!==d.phase||prev.mi!==d.mi||prev.leader!==d.leader)){
    if(d.phase==='propose'&&d.leader===mi)msgs.push('👑 Kamu pemimpin rapat — pilih tim proyek');
    else if(d.phase==='vote'&&mi>=0)msgs.push('Saatnya voting: setuju atau tolak?');
    else if(d.phase==='mission'&&d.team.includes(mi))msgs.push('🛠 Kamu masuk tim proyek — kirim kartumu');
    else if(d.phase==='shoot')msgs.push('🎯 Oknum terbuka — Dalang menebak Auditor Internal');
  }
  if(msgs.length)toast(msgs.join(' · '));
}
async function onHubEnded(st){
  const rid='g_'+cur.gid; if(ui.saved[rid])return; ui.saved[rid]=true;
  const w=hubWinners(st), WW=st.game==='werewolf', rv=WW?(st.reveal?st.reveal.fin:[]):(st.reveal||[]);
  const players=st.players.map((p,i)=>({id:p.id,nick:p.nick||NAMES[p.id]||'',rank:w[i]?1:2,role:rv[i]||'',orig:WW&&st.reveal?st.reveal.deal[i]:'',dead:WW&&st.reveal?st.reveal.dead.includes(i):st.game==='wwk'?!st.alive[i]:false,pts:0,cards:0}));
  const ts=Date.now();
  const doc={variant:st.game,mode:'online',level:null,name:st.name||'',endedAt:ts,week:weekKey(ts),rounds:WW?1:st.game==='wwk'?st.day:(st.res||[]).length,
    ids:players.map(p=>p.id),players,award:{},winner:st.winner,winBy:st.winBy||'',log:st.log.slice(-40)};
  try{const ref=db.doc('results/'+rid);await lease(ref);const ex=await ref.get();
    if(!ex.exists){await ref.set(doc);for(const uid of doc.ids){try{await bumpStats(uid,doc,rid);}catch(e){}}}}catch(e){}
  if(cur.gid){const g=cur.gid;setTimeout(()=>{db.doc('games/'+g).delete().catch(()=>{});},20000);}
}
