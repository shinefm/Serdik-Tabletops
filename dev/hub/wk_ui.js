/* ================= HUB · WEREWOLF KLASIK (UI) ================= */
function wkChip(k){const R=WK_ROLES[k];return `<span class="wwr t-${R.t}" title="${esc(R.d)}">${R.i} ${R.n}</span>`;}
function wkCompHTML(st,isHost){
  const n=st.players.length, auto=!(st.roles&&st.roles.length), deck=auto?wkPreset(Math.max(6,Math.min(20,n))):st.roles, ok=deck.length===n;
  return `<div class="wwcomp"><div class="bd" style="margin-bottom:6px">🃏 Peran (${deck.length} kartu = jumlah pemain)${auto?' · <b>rekomendasi otomatis</b> sesuai jumlah pemain':' · <b>diatur tuan rumah</b>'}</div>
    <div class="wwchips">${WK_KEYS.flatMap(k=>deck.filter(x=>x===k)).map(wkChip).join('')}</div>
    ${!auto&&!ok?`<div class="bd" style="color:var(--bad);margin-top:6px">⚠️ Sekarang ${n} pemain, jadi butuh ${n} kartu. Atur ulang sebelum mulai.</div>`:''}
    ${n<6?`<div class="bd" style="margin-top:6px">Butuh minimal 6 pemain untuk mulai (sekarang ${n}).</div>`:''}
    ${isHost?`<div class="row" style="gap:6px;margin-top:8px"><button class="btn sm" data-act="wkroles">⚙️ Atur peran</button>${auto?'':'<button class="btn sm" data-act="wwauto">↺ Pakai rekomendasi</button>'}</div>`:''}</div>`;
}
function wkRolesModal(){
  const st=cur.st, n=st.players.length;
  if(!ui.wwDraft)ui.wwDraft=(st.roles&&st.roles.length?st.roles:wkPreset(Math.max(6,n))).slice();
  const D=ui.wwDraft, cnt=k=>D.filter(x=>x===k).length;
  const row=k=>{const R=WK_ROLES[k],c=cnt(k);return `<div class="wwrow"><span class="wwr t-${R.t}">${R.i} ${R.n}</span><span class="bd wwd">${esc(R.d)}</span>
      <span class="wwct"><button class="btn sm" data-act="wkdec" data-k="${k}" ${c?'':'disabled'}>−</button><b>${c}</b><button class="btn sm" data-act="wkinc" data-k="${k}" ${c<WK_MAX[k]?'':'disabled'}>+</button></span></div>`;};
  openModal(`<h3>⚙️ Atur peran · Werewolf Klasik</h3><p class="bd" style="margin:0 0 8px">Jumlah kartu harus sama dengan jumlah pemain (<b>${n}</b>). Terpilih: <b style="color:${D.length===n?'var(--ok)':'var(--bad)'}">${D.length}</b>. Serigala harus kurang dari separuh.</p>
    <div class="wwlist">${WK_KEYS.map(row).join('')}</div>
    <div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn" data-act="wkdraftauto">↺ Rekomendasi</button><button class="btn pri" data-act="wwsave" ${D.includes('W')?'':'disabled'}>Simpan</button></div>`);
}
function wkRules(){
  return `<h3>🐺 Werewolf Klasik (6–20 pemain)</h3>
  <p>Versi klasik dengan <b>banyak malam dan siang</b>, dan aplikasi bertindak sebagai moderator. Pemain yang tewas keluar dari permainan, perannya dibuka ke semua, dan ia tidak boleh ikut bicara lagi.</p>
  <ul><li><b>🌙 Malam.</b> Semua pemain membuka layar masing-masing. Serigala memilih korban bersama (suara terbanyak; malam pertama hanya berkenalan). Peramal memeriksa 1 orang, Tabib melindungi 1 orang. Pemain lain menekan "Tidur". Malam berakhir saat semua selesai.</li>
  <li><b>☀️ Siang.</b> Korban malam diumumkan, lalu warga berdiskusi dan voting <b>terbuka</b> untuk menghukum 1 orang, atau memilih <b>Lewati</b>. Yang suaranya terbanyak dihukum. Kalau seri, atau "Lewati" ikut seri di posisi teratas, tidak ada yang dihukum.</li>
  <li><b>🏹 Pemburu</b> yang tewas langsung menembak 1 orang.</li></ul>
  <p><b>Menang:</b> Desa menang kalau semua serigala tewas. Serigala (dan Antek) menang kalau jumlah serigala hidup sudah menyamai sisa pemain lain. Penyamak menang sendirian kalau ia dihukum warga.</p>
  <p><b>Peran:</b></p><div class="wwlist">${WK_KEYS.map(k=>`<div class="wwrow"><span class="wwr t-${WK_ROLES[k].t}">${WK_ROLES[k].i} ${WK_ROLES[k].n}</span><span class="bd wwd">${esc(WK_ROLES[k].d)}</span></div>`).join('')}</div>
  <p class="mute">Cocok untuk grup besar, di satu ruangan atau lewat call. Yang sudah tewas boleh menonton tapi jangan membocorkan peran!</p>`;
}
function wkMine(st,mi){ // informasi rahasia untuk pemain mi
  const R=wkRoles(st), r=R[mi], L=[], H=(()=>{const h=wwGet(st,'hk');return Array.isArray(h)?h:[];})(), who=i=>'<b>'+esc(nm(st,i))+'</b>';
  if(r==='W'){const o=R.map((x,i)=>x==='W'&&i!==mi?i:-1).filter(i=>i>=0);L.push('🐺 Kawanan serigala: '+(o.map(i=>who(i)+(st.alive[i]?'':' ☠️')).join(', ')||'kamu sendirian'));}
  if(r==='M'){const o=R.map((x,i)=>x==='W'?i:-1).filter(i=>i>=0);L.push('😈 Serigala: '+o.map(i=>who(i)+(st.alive[i]?'':' ☠️')).join(', '));}
  if(r==='S'){H.filter(h=>h.seer&&h.seer.p===mi).forEach(h=>L.push(`🔮 Malam ${h.night}: ${who(h.seer.t)} ${h.seer.wolf?'<b style="color:var(--bad)">SERIGALA</b>':'bukan serigala'}`));
    const a=wwGet(st,'ak')[mi];if(st.phase!=='night'||!a||a.t==null){}else L.push(`🔮 Malam ini: ${who(a.t)} ${R[a.t]==='W'?'<b style="color:var(--bad)">SERIGALA</b>':'bukan serigala'}`);}
  if(r==='T'&&st.lastProt!=null)L.push(`🩺 Malam terakhir kamu melindungi ${who(st.lastProt)} (malam ini tidak boleh orang yang sama).`);
  return L;
}
function renderWK(){
  const st=cur.st, mi=meIdx(st), n=st.players.length, ended=st.status!=='playing', ph=st.phase, R=wkRoles(st);
  refreshNames(st.players.map(p=>p.id));
  const key=ph+':'+st.night+':'+st.day; if(ui.wkKey!==key){ui.wkKey=key;ui.wkSel=null;}
  const me=mi>=0?R[mi]:null, alive=mi>=0&&st.alive[mi], dead=mi>=0&&!st.alive[mi];
  const seeAll=ended||dead, wolfMates=me==='W'||me==='M';
  const acts=ph==='night'&&me==='W'?wwGet(st,'ak'):{};
  const done=ph==='night'&&st.done.includes(mi);
  const needT=ph==='night'&&alive&&!done&&((me==='W'&&st.night>1)||me==='S'||me==='T');
  const canVote=ph==='day'&&alive&&canWrite!==false, canShoot=ph==='hunter'&&st.hunter&&st.hunter.p===mi;
  const tally={}; if(ph==='day')Object.values(st.votes).forEach(t=>tally[t]=(tally[t]||0)+1);
  const chips=st.players.map((p,i)=>{
    const al=st.alive[i], d=st.deaths.find(x=>x.p===i);
    let tag='';
    if(!al&&d)tag=`<span class="wwr t-${WK_ROLES[d.r].t}">${WK_ROLES[d.r].i} ${WK_ROLES[d.r].n}</span>`;
    else if(seeAll)tag=`<span class="wwr t-${WK_ROLES[R[i]].t}" style="opacity:.8">${WK_ROLES[R[i]].i} ${WK_ROLES[R[i]].n}</span>`;
    else if(i===mi)tag=`<span class="wwr t-${WK_ROLES[me].t}">${WK_ROLES[me].i} kamu</span>`;
    else if(wolfMates&&R[i]==='W')tag='<span class="wwr t-w">🐺 Serigala</span>';
    let sub='';
    if(!al)sub=`<span class="rbd">☠️ ${esc(d?d.cause:'tewas')}</span>`;
    else if(ph==='night')sub=`<span class="rbd">${st.done.includes(i)?'😴 tidur':'🌙 …'}</span>${me==='W'&&R[i]==='W'&&acts[i]&&acts[i].t!=null?`<span class="rbd" style="color:var(--bad)">🐺 incar ${esc(nm(st,acts[i].t))}</span>`:''}`;
    else if(ph==='day')sub=`<span class="rbd">${st.votes[i]!=null?(st.votes[i]<0?'🗳 Lewati':'🗳 → '+esc(nm(st,st.votes[i]))):'… berdiskusi'}</span>${tally[i]?`<span class="rbd" style="color:var(--gold)"><b>${tally[i]} suara</b></span>`:''}`;
    const can=al&&i!==mi&&((needT&&!(me==='W'&&R[i]==='W'))||canVote||canShoot)||(needT&&me==='T'&&i===mi&&al);
    const sel=ui.wkSel===i||(ph==='day'&&ui.wkSel==null&&st.votes[mi]===i);
    return `<div class="rpchip ${can?'pick':''} ${sel?'team':''} ${i===mi?'me':''} ${al?'':'dead'}" ${can?`data-act="wksel" data-i="${i}"`:''}>
      <div class="rh"><span class="dot ${ONLINE.has(p.id)?'on':''}"></span><span class="rno">${i+1}</span><b>${esc(nm(st,i))}</b>${i===mi?'<span class="mine" style="font-size:11px">(kamu)</span>':''}</div><div class="rbadges">${tag}</div>${sub}</div>`;}).join('');
  let head, act='';
  const info=mi>=0?wkMine(st,mi):[];
  const card=me?`<div class="wwme t-${WK_ROLES[me].t}"><div class="wi">${WK_ROLES[me].i}</div><div><div class="bd" style="letter-spacing:1.5px;font-weight:700">PERANMU · PIHAK ${WW_TEAM[WK_ROLES[me].t].toUpperCase()}${dead?' · ☠️ SUDAH TEWAS':''}</div><h3 style="font-size:20px;margin:2px 0">${WK_ROLES[me].n}</h3><div class="bd">${esc(WK_ROLES[me].d)}</div></div></div>${info.length?`<div class="wwinfo">${info.map(x=>`<div>${x}</div>`).join('')}</div>`:''}`:'';
  if(ended){head='🏁 '+esc(st.winBy);act=`<div><b>${esc(st.winBy)}</b>.</div><button class="btn pri" data-act="showend">Lihat hasil & semua peran</button>`;}
  else if(ph==='night'){head=`🌙 Malam ke-${st.night} · ${st.done.length}/${wkAliveIdx(st).length} selesai`;
    act=card+(dead?'<div class="bd">☠️ Kamu sudah tewas. Kamu bisa melihat semua peran, tapi jangan dibocorkan ya.</div>':mi<0?'<div class="bd">👀 Kamu menonton.</div>':done?`<div class="bd">😴 Kamu sudah selesai. Menunggu ${wkAliveIdx(st).length-st.done.length} pemain lagi…</div>`
      :needT?`<div>${me==='W'?'Ketuk <b>korban</b> pilihanmu. Kawananmu melihat pilihanmu, dan korban ditentukan suara terbanyak.':me==='S'?'Ketuk <b>1 pemain</b> untuk diperiksa.':'Ketuk <b>1 pemain</b> (boleh dirimu) untuk dilindungi malam ini.'}</div>
        <div class="row"><button class="btn pri" data-act="wknight" ${ui.wkSel!=null?'':'disabled'}>${me==='W'?'🐺 Mangsa':me==='S'?'🔮 Periksa':'🩺 Lindungi'} ${ui.wkSel!=null?esc(nm(st,ui.wkSel)):''}</button>${me!=='W'?'<button class="btn" data-act="wkskip">Lewati</button>':''}</div>`
      :`<div class="row"><button class="btn pri" data-act="wkskip">😴 ${me==='W'&&st.night===1?'Sudah berkenalan, tidur':'Tidur'}</button></div>`);}
  else if(ph==='day'){const al=wkAliveIdx(st).length;head=`☀️ Hari ke-${st.day} · ${Object.keys(st.votes).length}/${al} sudah memilih`;
    act=card+(canVote?`<div>Diskusikan, lalu ketuk orang yang mau dihukum. Voting terbuka, dan pilihanmu bisa diganti sampai semua memilih${st.timer?' atau waktu habis':''}.</div>
      <div class="row"><button class="btn danger" data-act="wkvote" ${ui.wkSel!=null&&ui.wkSel!==st.votes[mi]?'':'disabled'}>⚖️ Hukum ${ui.wkSel!=null?esc(nm(st,ui.wkSel)):''}</button><button class="btn" data-act="wkvskip" ${st.votes[mi]===-1?'disabled':''}>Lewati</button>${st.votes[mi]!=null?`<span class="bd">Pilihanmu: <b>${st.votes[mi]<0?'Lewati':esc(nm(st,st.votes[mi]))}</b></span>`:''}</div>`
      :dead?'<div class="bd">☠️ Kamu sudah tewas, jadi tidak ikut voting. Jangan bocorkan peran ya.</div>':'');}
  else if(ph==='hunter'){head=`🏹 ${esc(nm(st,st.hunter.p))} (Pemburu) menembak sebelum tewas`;
    act=canShoot?`<div><b>Kamu Pemburu dan baru saja tewas.</b> Ketuk 1 pemain untuk ditembak.</div><button class="btn danger" data-act="wkshoot" ${ui.wkSel!=null?'':'disabled'}>🏹 Tembak ${ui.wkSel!=null?esc(nm(st,ui.wkSel)):''}</button>`:`<div>Menunggu Pemburu memilih sasaran…</div>`;}
  const deaths=st.deaths.map(d=>`<div class="rbd">☠️ ${esc(nm(st,d.p))} — ${WK_ROLES[d.r].n}, ${esc(d.cause)} (${d.cause==='dihukum warga'?'hari '+d.day:'malam '+d.night})</div>`).join('');
  const logs=st.log.slice(-14).reverse().map(l=>`<div>${l.p>=0?`<b>${esc(nm(st,l.p))}</b> `:''}${esc(l.m)}</div>`).join('');
  const isHost=st.host===myId;
  $('#app').innerHTML=`<div class="rp-wrap ww ${ph}">
    <section class="panel"><div class="turnbar"><div class="who"><span class="pill playing" style="margin:0 6px 0 0">🐺 KLASIK</span>${head}${timerHTML(st)}</div>
      <div class="row" style="gap:6px"><button class="btn sm" data-act="tutorial" data-w="wwk">📖</button></div></div>
      <div class="bd" style="margin-bottom:6px">Peran di desa ini (${wkAliveIdx(st).length}/${n} masih hidup):</div><div class="wwchips">${(st.inPlay||[]).map(wkChip).join('')}</div></section>
    <section class="panel ract">${act}</section>
    <section class="panel"><div class="rpl">${chips}</div>
      ${isHost&&!ended?`<button class="btn sm" style="margin-top:10px" data-act="rforce">⏩ ${ph==='night'?'Akhiri malam sekarang':ph==='day'?'Akhiri diskusi & hitung suara':'Lewati Pemburu (tembak acak)'}</button>`:''}</section>
    ${deaths?`<section class="panel"><h3 style="font-size:16px;margin-bottom:6px">⚰️ Makam desa</h3>${deaths}</section>`:''}
    ${ended?`<section class="panel"><h3 style="font-size:16px;margin-bottom:6px">🌙 Kronologi malam</h3>${wkChron(st)}</section>`:''}
    <details class="panel log" ${ui.logOpen?'open':''} ontoggle="ui.logOpen=this.open"><summary style="font-family:Fraunces,serif;font-weight:600;font-size:15px;cursor:pointer">Catatan permainan</summary>${logs}</details>
  </div>`;
  maybeEndPopup(st);
}
function wkChron(st){
  const H=st.hist||[], who=i=>'<b>'+esc(nm(st,i))+'</b>';
  return H.map(h=>`<div class="rbd" style="font-size:13.5px">🌙 Malam ${h.night}: ${h.night===1?'serigala berkenalan':h.target!=null?'serigala mengincar '+who(h.target):'serigala tidak memilih'}${h.prot!=null?` · Tabib melindungi ${who(h.prot)}`:''}${h.seer?` · Peramal memeriksa ${who(h.seer.t)} (${h.seer.wolf?'serigala':'bukan'})`:''} → ${h.victim!=null?who(h.victim)+' tewas':h.night===1?'aman':'tidak ada korban'}</div>`).join('')||'<div class="bd">—</div>';
}
function openWKEnd(){
  const st=cur.st, mi=meIdx(st), w=hubWinners(st), R=st.reveal||wkRoles(st);
  const title=mi<0?esc(st.winBy):w[mi]?'Kamu menang! 🎉':'Kamu kalah';
  const list=st.players.map((p,i)=>i).sort((a,b)=>(w[b]-w[a])||(st.alive[b]-st.alive[a])||(a-b)).map(i=>{const d=st.deaths.find(x=>x.p===i);
    return `<div class="rki ${w[i]?'win':''} ${i===mi?'me':''}"><span class="pos">${WK_ROLES[R[i]].i}</span><span class="nm">${esc(nm(st,i))}${i===mi?' <span class="mine" style="font-size:12px">(kamu)</span>':''}<div class="bd" style="font-weight:400">${WK_ROLES[R[i]].n} · ${d?'☠️ '+esc(d.cause):'✅ selamat'}</div></span><span class="pt" style="font-size:15px">${w[i]?'🏆':''}</span></div>`;}).join('');
  openModal(`<div class="endm"><div class="big">${st.winner==='v'?'🏡':st.winner==='w'?'🐺':'🧥'}</div><h3>${title}</h3><p class="why">${esc(st.winBy)}.</p>
    <div class="rkl">${list}</div><p class="bd" style="margin:10px 0 0">Kronologi malam ada di bawah papan. Tercatat di 📜 Riwayat dan rekor 👤 Profil, tanpa poin peringkat.</p>
    <div class="mbtns"><button class="btn" data-act="close">Lihat kronologi</button><button class="btn pri" data-act="lobby">Kembali ke lobi</button></div></div>`);
}
