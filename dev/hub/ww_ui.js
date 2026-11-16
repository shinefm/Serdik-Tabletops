/* ================= HUB · WEREWOLF SATU MALAM ================= */
function wwRoleChip(k,cls){const R=WW_ROLES[k];return `<span class="wwr t-${R.t} ${cls||''}" title="${esc(R.d)}">${R.i} ${R.n}</span>`;}
function wwDeckChips(deck){return deck.map(k=>wwRoleChip(k)).join('');}
function wwCompHTML(st,isHost){
  const n=st.players.length, auto=!(st.roles&&st.roles.length), deck=auto?wwPreset(Math.max(3,Math.min(10,n))):st.roles;
  const ok=deck.length===n+3;
  return `<div class="wwcomp"><div class="bd" style="margin-bottom:6px">🃏 Peran yang dimainkan (${deck.length} kartu = pemain + 3 kartu tengah)${auto?' · <b>rekomendasi otomatis</b> sesuai jumlah pemain':' · <b>diatur tuan rumah</b>'}</div>
    <div class="wwchips">${wwDeckChips(WW_KEYS.flatMap(k=>deck.filter(x=>x===k)))}</div>
    ${!auto&&!ok?`<div class="bd" style="color:var(--bad);margin-top:6px">⚠️ Sekarang ${n} pemain, jadi butuh ${n+3} kartu. Atur ulang sebelum mulai.</div>`:''}
    ${n<3?`<div class="bd" style="margin-top:6px">Butuh minimal 3 pemain untuk mulai (sekarang ${n}).</div>`:''}
    ${isHost?`<div class="row" style="gap:6px;margin-top:8px"><button class="btn sm" data-act="wwroles">⚙️ Atur peran</button>${auto?'':'<button class="btn sm" data-act="wwauto">↺ Pakai rekomendasi</button>'}</div>`:''}</div>`;
}
function wwRolesModal(){
  const st=cur.st, n=st.players.length;
  if(!ui.wwDraft)ui.wwDraft=(st.roles&&st.roles.length?st.roles:wwPreset(Math.max(3,n))).slice();
  const D=ui.wwDraft, cnt=k=>D.filter(x=>x===k).length, need=n+3;
  const row=k=>{const R=WW_ROLES[k],c=cnt(k),step=k==='K'?2:1;
    return `<div class="wwrow"><span class="wwr t-${R.t}">${R.i} ${R.n}</span><span class="bd wwd">${esc(R.d)}</span>
      <span class="wwct"><button class="btn sm" data-act="wwdec" data-k="${k}" ${c?'':'disabled'}>−</button><b>${c}</b><button class="btn sm" data-act="wwinc" data-k="${k}" ${c+step<=WW_MAX[k]?'':'disabled'}>+</button></span></div>`;};
  openModal(`<h3>⚙️ Atur peran</h3><p class="bd" style="margin:0 0 8px">Jumlah kartu harus <b>pemain + 3</b>. Sekarang ${n} pemain → butuh <b>${need}</b> kartu. Terpilih: <b style="color:${D.length===need?'var(--ok)':'var(--bad)'}">${D.length}</b>.</p>
    <div class="wwlist">${WW_KEYS.map(row).join('')}</div>
    <div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn" data-act="wwdraftauto">↺ Rekomendasi</button><button class="btn pri" data-act="wwsave" ${D.includes('W')?'':'disabled'}>Simpan</button></div>`);
}
function wwRules(){
  return `<h3>🐺 Werewolf Satu Malam (3–10 pemain)</h3>
  <p>Versi bahasa Indonesia dari <b>One Night Ultimate Werewolf</b>. Tiap pemain dapat 1 kartu peran rahasia, dan <b>3 kartu sisanya ada di tengah</b>. Permainannya hanya <b>satu malam</b> dan <b>satu kali voting</b>, jadi tidak ada yang tersingkir lebih awal.</p>
  <ul><li><b>🌙 Malam.</b> Semua pemain melihat perannya lalu menjalankan kemampuan malamnya di layar masing-masing. Aplikasi menjalankan efeknya sesuai urutan resmi: Serigala → Antek → Tukang Batu → Peramal → Pencuri → Pembuat Onar → Pemabuk → Insomnia.</li>
  <li><b>☀️ Pagi.</b> Diskusikan siapa serigala. Kamu boleh jujur, menggertak, atau berbohong. Ingat: kartumu mungkin sudah ditukar orang lain tanpa kamu tahu.</li>
  <li><b>🗳 Voting.</b> Semua memilih 1 pemain lain, dan suara dibuka bersamaan. Pemain dengan suara terbanyak tewas (kalau seri, semua yang seri tewas). Kalau tiap pemain hanya dapat 1 suara, tidak ada yang tewas.</li>
  <li><b>Pihakmu ditentukan kartu terakhirmu</b>, bukan kartu awal.</li></ul>
  <p><b>Siapa menang?</b></p>
  <ul><li><b>Desa</b> menang kalau minimal 1 Manusia Serigala tewas. Kalau tidak ada serigala di antara pemain (semuanya di tengah), Desa menang kalau tidak ada yang tewas.</li>
  <li><b>Serigala</b> (termasuk Antek) menang kalau ada serigala di antara pemain dan tidak ada serigala yang tewas.</li>
  <li><b>Penyamak</b> menang kalau dia sendiri tewas, dan serigala otomatis gagal menang.</li></ul>
  <p><b>Peran:</b></p><div class="wwlist">${WW_KEYS.map(k=>`<div class="wwrow"><span class="wwr t-${WW_ROLES[k].t}">${WW_ROLES[k].i} ${WW_ROLES[k].n}</span><span class="bd wwd">${esc(WW_ROLES[k].d)}</span></div>`).join('')}</div>
  <p class="mute">Main sambil ngobrol, di satu ruangan atau lewat telepon/WA call. Jangan perlihatkan layarmu ke orang lain!</p>`;
}
function wwInfo(st,mi){
  const n=st.players.length, d=wwDeal(st), r=d[mi], a=wwGet(st,'ak')[mi], L=[], who=i=>'<b>'+esc(nm(st,i))+'</b>', role=k=>'<b>'+WW_ROLES[k].i+' '+WW_ROLES[k].n+'</b>', cen=c=>'kartu tengah '+(c+1);
  if(r==='W'){const o=d.map((x,i)=>i<n&&i!==mi&&x==='W'?i:-1).filter(i=>i>=0);
    if(o.length)L.push('🐺 Sesama serigala: '+o.map(who).join(', '));
    else if(a&&a.c!=null)L.push(`🐺 Kamu serigala sendirian. Kamu mengintip ${cen(a.c)}: ${role(d[n+a.c])}`);
    else L.push('🐺 Kamu serigala sendirian'+(a?' (tidak mengintip)':' — boleh mengintip 1 kartu tengah'));}
  if(r==='M'){const o=d.map((x,i)=>i<n&&x==='W'?i:-1).filter(i=>i>=0);L.push(o.length?'😈 Serigala: '+o.map(who).join(', '):'😈 Tidak ada serigala di antara pemain, semuanya di tengah');}
  if(r==='K'){const o=d.map((x,i)=>i<n&&i!==mi&&x==='K'?i:-1).filter(i=>i>=0);L.push(o.length?'🧱 Tukang Batu lainnya: '+o.map(who).join(', '):'🧱 Tukang Batu yang lain ada di tengah');}
  if(a&&!a.skip){
    if(r==='S'){if(a.p!=null)L.push(`🔮 Kartu ${who(a.p)}: ${role(d[a.p])}`);else L.push(`🔮 ${a.c.map(c=>cen(c)+': '+role(d[n+c])).join(' · ')}`);}
    if(r==='R')L.push(`🦝 Kamu menukar kartu dengan ${who(a.p)}. Kartu barumu: ${role(d[a.p])}`);
    if(r==='T')L.push(`🃏 Kamu menukar kartu ${who(a.ps[0])} dan ${who(a.ps[1])}`);
    if(r==='D')L.push(`🍺 Kamu menukar kartumu dengan ${cen(a.c)} (isinya tidak kamu ketahui)`);
  } else if(a&&a.skip&&['S','R','T'].includes(r))L.push('Kamu memilih tidak memakai kemampuan malam.');
  if(r==='I'){const f=wwFinal(st);L.push(f?`🌙 Kartumu di akhir malam: ${role(f[mi])}`:'🌙 Kamu akan melihat kartumu lagi di akhir malam.');}
  return L;
}
function wwNeeds(st,mi){
  const n=st.players.length, d=wwDeal(st), r=d[mi];
  if(r==='W')return d.some((x,i)=>i<n&&i!==mi&&x==='W')?null:{c:1,opt:true,txt:'Kamu serigala sendirian. Boleh mengintip <b>1 kartu tengah</b>.'};
  if(r==='S')return {p:1,c:2,opt:true,txt:'Ketuk <b>1 pemain</b> untuk melihat kartunya, atau <b>2 kartu tengah</b>.'};
  if(r==='R')return {p:1,opt:true,txt:'Ketuk <b>1 pemain</b> untuk menukar kartu dengannya, lalu kamu melihat kartu barumu.'};
  if(r==='T')return {p:2,opt:true,txt:'Ketuk <b>2 pemain lain</b> untuk menukar kartu mereka.'};
  if(r==='D')return {c:1,txt:'Ketuk <b>1 kartu tengah</b> untuk ditukar dengan kartumu. Kamu tidak melihat isinya.'};
  return null;
}
function renderWerewolf(){
  const st=cur.st, mi=meIdx(st), n=st.players.length, ended=st.status!=='playing', ph=st.phase;
  refreshNames(st.players.map(p=>p.id));
  const key=st.phase+':'+cur.gid; if(ui.wwKey!==key){ui.wwKey=key;ui.wsel={p:[],c:[]};ui.wvote=null;}
  const deal=mi>=0?wwDeal(st):null, myR=mi>=0?deal[mi]:null, done=mi>=0&&st.done.includes(mi), need=mi>=0&&ph==='night'&&!done&&canWrite!==false?wwNeeds(st,mi):null;
  const myVote=mi>=0&&ph==='day'?wwGet(st,'vk')[mi]:null;
  const R=st.reveal, pend=rapatPending(st);
  const canPickP=need&&need.p, canPickC=need&&need.c, canVote=!ended&&ph==='day'&&mi>=0&&canWrite!==false;
  const chips=st.players.map((p,i)=>{
    let tag='', sub='';
    if(ended&&R){const o=R.deal[i],f=R.fin[i];tag=`<span class="wwr t-${WW_ROLES[f].t}">${WW_ROLES[f].i} ${WW_ROLES[f].n}</span>${o!==f?`<span class="rbd">awalnya ${WW_ROLES[o].n}</span>`:''}`;
      sub=`<span class="rbd">${R.dead.includes(i)?'☠️ tewas · ':''}${R.cnt[i]} suara · pilih ${R.votes[i]!=null?esc(nm(st,R.votes[i])):'—'}</span>`;}
    else if(ph==='night')sub=`<span class="rbd">${st.done.includes(i)?'😴 sudah selesai':'🌙 sedang bertindak…'}</span>`;
    else if(ph==='day')sub=`<span class="rbd">${st.voted.includes(i)?'✔ sudah memilih':'… berdiskusi'}</span>`;
    const sel=(ph==='night'&&ui.wsel.p.includes(i))||(ph==='day'&&(ui.wvote===i||(ui.wvote==null&&myVote===i)));
    const act=i!==mi&&(canPickP?`data-act="wpick" data-i="${i}"`:canVote?`data-act="wvote" data-i="${i}"`:'');
    return `<div class="rpchip ${act?'pick':''} ${sel?'team':''} ${i===mi?'me':''} ${pend.includes(i)?'pend':''} ${ended&&R&&R.dead.includes(i)?'dead':''}" ${act}>
      <div class="rh"><span class="dot ${ONLINE.has(p.id)?'on':''}"></span><span class="rno">${i+1}</span><b>${esc(nm(st,i))}</b>${i===mi?'<span class="mine" style="font-size:11px">(kamu)</span>':''}</div>
      <div class="rbadges">${tag}</div>${sub}</div>`;}).join('');
  const center=[0,1,2].map(c=>{const sel=ui.wsel.c.includes(c), open=ended&&R;
    return `<div class="wwcard ${canPickC?'pick':''} ${sel?'sel':''} ${open?'open t-'+WW_ROLES[R.fin[n+c]].t:''}" ${canPickC?`data-act="wcen" data-c="${c}"`:''}>${open?`<span class="wi">${WW_ROLES[R.fin[n+c]].i}</span><span>${WW_ROLES[R.fin[n+c]].n}</span>${R.deal[n+c]!==R.fin[n+c]?`<span class="rbd">awalnya ${WW_ROLES[R.deal[n+c]].n}</span>`:''}`:`<span class="wi">🂠</span><span>Tengah ${c+1}</span>`}</div>`;}).join('');
  let head, act='';
  if(ended){head=`🏁 ${esc(st.winBy||'')}`;act=`<div><b>${esc(st.winBy||'')}</b>.</div><button class="btn pri" data-act="showend">Lihat hasil &amp; semua kartu</button>`;}
  else if(ph==='night'){head=`🌙 Malam · ${st.done.length}/${n} pemain selesai`;
    if(mi<0)act='<div>Malam sedang berlangsung. Kamu menonton meja ini.</div>';
    else{const info=wwInfo(st,mi);
      act=`<div class="wwme t-${WW_ROLES[myR].t}"><div class="wi">${WW_ROLES[myR].i}</div><div><div class="bd" style="letter-spacing:1.5px;font-weight:700">KARTU AWALMU · PIHAK ${WW_TEAM[WW_ROLES[myR].t].toUpperCase()}</div><h3 style="font-size:22px;margin:2px 0">${WW_ROLES[myR].n}</h3><div class="bd">${esc(WW_ROLES[myR].d)}</div></div></div>`
        +(info.length?`<div class="wwinfo">${info.map(x=>`<div>${x}</div>`).join('')}</div>`:'');
      if(done)act+=`<div class="bd">😴 Kamu sudah selesai. Menunggu ${n-st.done.length} pemain lagi… Pagi tiba saat semua selesai.</div>`;
      else if(need){const cnt=ui.wsel.p.length+ui.wsel.c.length, ok=myR==='S'?(ui.wsel.p.length===1&&!ui.wsel.c.length)||(ui.wsel.c.length===2&&!ui.wsel.p.length):myR==='T'?ui.wsel.p.length===2:cnt===1;
        act+=`<div>${need.txt}</div><div class="row"><button class="btn pri" data-act="wnight" ${ok?'':'disabled'}>${{W:'👁 Intip',S:'👁 Lihat',R:'🦝 Curi kartu',T:'🔀 Tukar',D:'🍺 Tukar'}[myR]}</button>${need.opt?'<button class="btn" data-act="wskip">Lewati</button>':''}${cnt?'<button class="btn" data-act="wclr">Batal pilih</button>':''}</div>`;}
      else act+=`<div class="row"><button class="btn pri" data-act="wnight">${myR==='I'?'😴 Tidur dulu':'✔ Sudah, lanjut tidur'}</button></div>`;}}
  else{head=`☀️ Pagi · diskusi & voting · ${st.voted.length}/${n} sudah memilih`;
    if(mi<0)act='<div>Desa sedang berdiskusi. Kamu menonton meja ini.</div>';
    else{const info=wwInfo(st,mi);
      act=`<div class="wwinfo"><div class="bd" style="font-weight:700;margin-bottom:2px">📝 Catatan malammu · kartu awal: ${WW_ROLES[myR].i} ${WW_ROLES[myR].n}</div>${info.map(x=>`<div>${x}</div>`).join('')||'<div class="bd">Tidak ada informasi malam.</div>'}<div class="bd" style="margin-top:4px">Ingat: kartumu mungkin sudah ditukar orang lain.</div></div>`
        +`<div>Ketuk pemain yang kamu curigai sebagai serigala, lalu kunci suaramu. Suara dibuka bersamaan setelah semua memilih${st.timer?' atau waktu diskusi habis':''}.</div>`
        +`<div class="row"><button class="btn danger" data-act="wvoteok" ${ui.wvote!=null&&ui.wvote!==myVote?'':'disabled'}>🗳 ${ui.wvote!=null?'Pilih '+esc(nm(st,ui.wvote)):'Pilih pemain dulu'}</button>${myVote!=null?`<span class="bd">Suaramu sekarang: <b>${esc(nm(st,myVote))}</b> (masih bisa diganti)</span>`:''}</div>`;}}
  const chron=ended&&R?wwChronicle(st):'';
  const logs=st.log.slice(-12).reverse().map(l=>`<div>${l.p>=0?`<b>${esc(nm(st,l.p))}</b> `:''}${esc(l.m)}</div>`).join('');
  const isHost=st.host===myId;
  $('#app').innerHTML=`<div class="rp-wrap ww ${ph}">
    <section class="panel">
      <div class="turnbar"><div class="who"><span class="pill playing" style="margin:0 6px 0 0">🐺 WEREWOLF</span>${head}${timerHTML(st)}</div>
        <div class="row" style="gap:6px">${mi<0?'<span class="bd">👀 Menonton</span>':''}<button class="btn sm" data-act="tutorial" data-w="werewolf">📖</button></div></div>
      <div class="bd" style="margin-bottom:6px">Peran yang dimainkan:</div><div class="wwchips">${wwDeckChips(st.inPlay||[])}</div>
    </section>
    <section class="panel ract">${act}</section>
    <section class="panel"><div class="rpl">${chips}</div>
      <div class="bd" style="margin:12px 0 6px">Kartu tengah</div><div class="wwcen">${center}</div>
      ${isHost&&!ended?`<button class="btn sm" style="margin-top:10px" data-act="rforce">⏩ ${ph==='night'?'Akhiri malam sekarang':'Akhiri diskusi & hitung suara'}</button>`:''}</section>
    ${chron?`<section class="panel"><h3 style="font-size:16px;margin-bottom:6px">🌙 Kronologi malam</h3>${chron}</section>`:''}
    <details class="panel log" ${ui.logOpen?'open':''} ontoggle="ui.logOpen=this.open"><summary style="font-family:Fraunces,serif;font-weight:600;font-size:15px;cursor:pointer">Catatan permainan</summary>${logs}</details>
  </div>`;
  maybeEndPopup(st);
}
function wwChronicle(st){
  const R=st.reveal, n=st.players.length, d=R.deal, A=R.acts, who=i=>'<b>'+esc(nm(st,i))+'</b>', role=k=>WW_ROLES[k].n, cen=c=>'kartu tengah '+(c+1), out=[];
  const by=k=>d.map((x,i)=>i<n&&x===k?i:-1).filter(i=>i>=0);
  const w=by('W'); if(w.length)out.push(`🐺 Serigala: ${w.map(who).join(', ')}${w.length===1&&A[w[0]]&&A[w[0]].c!=null?` (mengintip ${cen(A[w[0]].c)}: ${role(d[n+A[w[0]].c])})`:''}`); else if(st.inPlay.includes('W'))out.push('🐺 Semua serigala ada di tengah.');
  by('M').forEach(i=>out.push(`😈 Antek: ${who(i)}`));
  const k=by('K'); if(k.length)out.push(`🧱 Tukang Batu: ${k.map(who).join(', ')}`);
  by('S').forEach(i=>{const a=A[i]||{};out.push(`🔮 Peramal ${who(i)} ${a.p!=null?'melihat kartu '+who(a.p)+' ('+role(d[a.p])+')':a.c?'melihat '+a.c.map(c=>cen(c)+' ('+role(d[n+c])+')').join(' & '):'tidak memakai kemampuannya'}`);});
  by('R').forEach(i=>{const a=A[i]||{};out.push(`🦝 Pencuri ${who(i)} ${a.p!=null?'menukar kartu dengan '+who(a.p)+' dan menjadi '+role(d[a.p]):'tidak mencuri'}`);});
  by('T').forEach(i=>{const a=A[i]||{};out.push(`🃏 Pembuat Onar ${who(i)} ${a.ps?'menukar kartu '+who(a.ps[0])+' dan '+who(a.ps[1]):'tidak membuat onar'}`);});
  by('D').forEach(i=>{const a=A[i]||{};out.push(`🍺 Pemabuk ${who(i)} menukar kartunya dengan ${cen(a.c)} (${role(d[n+a.c])})`);});
  by('I').forEach(i=>out.push(`🌙 Insomnia ${who(i)} bangun dan melihat kartunya: ${role(R.fin[i])}`));
  return out.map(x=>`<div class="rbd" style="font-size:13.5px">${x}</div>`).join('');
}
function openWWEnd(){
  const st=cur.st, R=st.reveal; if(!R)return;
  const mi=meIdx(st), w=hubWinners(st);
  const title=mi<0?'Permainan selesai':w[mi]?'Kamu menang! 🎉':'Kamu kalah';
  const list=st.players.map((p,i)=>i).sort((a,b)=>(w[b]-w[a])||(a-b)).map(i=>{const f=R.fin[i],o=R.deal[i];
    return `<div class="rki ${w[i]?'win':''} ${i===mi?'me':''}"><span class="pos">${WW_ROLES[f].i}</span><span class="nm">${esc(nm(st,i))}${i===mi?' <span class="mine" style="font-size:12px">(kamu)</span>':''}<div class="bd" style="font-weight:400">${WW_ROLES[f].n}${o!==f?' · awalnya '+WW_ROLES[o].n:''} · ${R.cnt[i]} suara${R.dead.includes(i)?' · ☠️ tewas':''}</div></span><span class="pt" style="font-size:15px">${w[i]?'🏆':''}</span></div>`;}).join('');
  openModal(`<div class="endm"><div class="big">${R.vw?'🏡':R.ww?'🐺':R.tanner?'🧥':'🏁'}</div><h3>${title}</h3><p class="why">${esc(st.winBy||'')}.</p>
    <div class="rkl">${list}</div>
    <p class="bd" style="margin:10px 0 0">Kronologi malam ada di bawah papan. Tercatat di 📜 Riwayat dan rekor 👤 Profil, tanpa poin peringkat.</p>
    <div class="mbtns"><button class="btn" data-act="close">Lihat kronologi</button><button class="btn pri" data-act="lobby">Kembali ke lobi</button></div></div>`);
}
