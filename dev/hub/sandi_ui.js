/* ================= SANDI SYNDICATE: tampilan ================= */
function sdKetua(st,t){return st.players.findIndex(p=>p.team===t&&p.ketua);}
function sdTeamNames(st,t){return st.players.map((p,i)=>i).filter(i=>st.players[i].team===t);}
function sdMkColor(mk){return (MK_INFO[mk]||{}).c||'#8a7fc0';}
function sdPackLabel(v){const p=PACKS.find(x=>x[0]===v);return p?p[1]:'Campuran 6 MK';}

/* ---------- ruang tunggu ---------- */
function renderWaitingSD(){
  const st=cur.st, mi=meIdx(st), isHost=st.host===myId, G=GAMES.sandi, n=st.players.length, canAct=canWrite!==false&&myId;
  refreshNames(st.players.map(p=>p.id));
  const col=t=>{
    const m=sdTeamNames(st,t), hasK=m.some(i=>st.players[i].ketua);
    const rows=m.map(i=>{const p=st.players[i];
      const canK=canAct&&!p.ketua&&(isHost||i===mi);
      return `<div class="seat"><span class="dot ${ONLINE.has(p.id)?'on':''}"></span><b>${esc(nm(st,i))}</b>${p.ketua?'<span class="sdk">🎖️ Ketua</span>':''}${p.id===st.host?'<span class="crown">· tuan rumah</span>':''}${i===mi?'<span class="mute">(kamu)</span>':''}${canK?`<button class="btn sm" style="margin-left:auto" data-act="sdketua" data-i="${i}">🎖️ ${i===mi?'Aku ketua':'Jadikan ketua'}</button>`:''}</div>`;}).join('')
      ||'<div class="seat emptyseat">Belum ada anggota</div>';
    const note=m.length&&!hasK?'<div class="bd" style="margin-top:4px">Ketua dipilih otomatis saat mulai kalau belum ada.</div>':'';
    const move=mi>=0&&st.players[mi].team!==t&&canAct?`<button class="btn sm" style="margin-top:8px" data-act="sdteam" data-t="${t}">Pindah ke Tim ${TEAMNAME[t]}</button>`:'';
    return `<div class="sdcol sd-${t}"><h3>${t==='r'?'🔴':'🔵'} Tim ${TEAMNAME[t]} <span class="bd">${m.length} orang</span></h3>${rows}${note}${move}</div>`;};
  const r=sdTeamNames(st,'r').length, b=sdTeamNames(st,'b').length, ok=r>=2&&b>=2;
  const comp=ok?`Siap mulai: Tim Merah ${r} orang, Tim Biru ${b} orang. Tim yang jalan duluan diacak saat mulai.`
    :`Tiap tim butuh minimal 2 orang: 1 ketua dan 1 penebak (sekarang Merah ${r}, Biru ${b}).`;
  $('#app').innerHTML=`<section class="panel" style="max-width:680px;margin:0 auto">
    <h2 style="font-size:24px">${G.icon} ${esc(st.name||'Meja')}</h2>
    <p class="mute" style="font-size:14px;margin:6px 0 0">${G.name} · ${G.min}–${G.max} pemain, 2 tim. Kirim link meja ini ke syndicate, teman langsung masuk ke meja.</p>
    ${shareBox(st)}
    <div class="sdcols">${col('r')}${col('b')}</div>
    <p class="bd" style="margin:10px 0 12px">${comp}</p>
    <div class="row">
      ${mi<0&&n<G.max&&canAct?'<button class="btn pri" data-act="join">Duduk di meja ini</button>':''}
      ${mi>=0&&!isHost?'<button class="btn" data-act="leave">Tinggalkan kursi</button>':''}
      ${isHost?`<button class="btn pri" data-act="start" ${ok?'':'disabled'}>Mulai permainan</button>`:''}
      <button class="btn" data-act="tutorial" data-w="sandi">📖 Cara main</button>
      ${(isHost||isOwnerFlag)?'<button class="btn danger sm" data-act="delete">Hapus meja</button>':''}
    </div>
    <div class="row" style="margin-top:12px;align-items:center;gap:8px"><span class="bd">📚 Kata di papan:</span>
      ${isHost?`<select id="sdPack" class="ordsel">${PACKS.map(([v,l])=>`<option value="${v}" ${(st.pack||'mix')===v?'selected':''}>${l}</option>`).join('')}</select>`:`<b>${esc(sdPackLabel(st.pack||'mix'))}</b>`}</div>
    <div class="row" style="margin-top:10px;align-items:center;gap:8px"><span class="bd">⏱ Waktu per tahap:</span>
      ${isHost?`<select id="tmrSel" class="ordsel">${timerOptions(st.timer||0)}</select>`:`<b>${timerLabel(st.timer||0)}</b>`}</div>
    <p class="hint" style="text-align:left">Ketua melihat kunci warna kartu dan memberi petunjuk satu kata. Anggota lain menebak istilah materi MK yang dimaksud.${st.timer?' Kalau waktu habis, giliran pindah ke tim lawan.':''}</p>
    ${mi<0&&!isHost?'<p class="hint" style="text-align:left">Kamu bisa ikut sebelum tuan rumah memulai permainan.</p>':''}
  </section>`;
}

/* ---------- papan permainan ---------- */
function renderSandi(){
  const st=cur.st, mi=meIdx(st), me=mi>=0?st.players[mi]:null, ended=st.status!=='playing';
  refreshNames(st.players.map(p=>p.id));
  const key=sandiKey(st), T=st.turnTeam, isK=!!(me&&me.ketua);
  const spy=ended||(isK&&ui.sdKey!==false);
  const myTurn=!ended&&me&&me.team===T&&canWrite!==false&&!st.paused;
  const canClue=myTurn&&isK&&st.phase==='clue', canGuess=myTurn&&!isK&&st.phase==='guess';
  const sk=st.round+':'+T+':'+st.phase+':'+st.rev.filter(Boolean).length; if(ui.sdSK!==sk){ui.sdSK=sk;ui.sdSel=null;}
  const oneMk=new Set(st.words.map(x=>x.mk)).size===1;
  const cards=st.words.map((ref,i)=>{const w=termOf(ref), r=st.rev[i];
    const cls=r?`rev c-${r.c}`:spy?`spy c-${key[i]}`:'';
    const sel=canGuess&&ui.sdSel===i?'sel':'', pick=canGuess&&!r?'pick':'';
    const by=r&&r.by!=null&&st.players[r.by]?`<span class="sdby">${r.c==='x'?'💥 ':''}${esc(nm(st,r.by))}</span>`:'';
    const lg=Math.max(...w.w.split(/\s+/).map(x=>x.length))>=10?'long':'';
    return `<button class="sdcard ${cls} ${sel} ${pick} ${lg}" data-act="sdcard" data-i="${i}">${oneMk?'':`<span class="sdmk" style="--mk:${sdMkColor(ref.mk)}">${ref.mk}</span>`}<span class="sdw">${esc(w.w)}</span>${spy&&!r&&key[i]==='x'?'<span class="sdx">💥</span>':''}${by}</button>`;}).join('');
  const left=t=>sandiLeft(st,t), Tn=t=>'Tim '+TEAMNAME[t];
  const kName=t=>{const k=sdKetua(st,t);return k>=0?esc(nm(st,k)):'ketua';};
  let head, act='';
  if(ended){head=`🏁 <b>${Tn(st.winner)}</b> menang`;
    act=`<div>${esc(st.winBy||'')}.</div><div class="bd">Semua warna kartu kini terbuka di papan. Ketuk kartu untuk membaca arti istilahnya.</div><button class="btn pri" data-act="showend">Lihat hasil</button>`;}
  else if(st.phase==='clue'){head=`🎖️ <b>${Tn(T)}</b> · ketua ${kName(T)} menyiapkan petunjuk`;
    if(canClue){const wv=esc(ui.sdW||''), nv=ui.sdN||1;
      act=`<div><b>Giliranmu memberi petunjuk.</b> Kartu timmu yang belum terbuka: <b>${left(T)}</b> (bergaris ${T==='r'?'merah':'biru'}). Hindari kartu 💥 Audit.</div>
        <div class="sdclue-in"><input id="sdW" maxlength="24" placeholder="Satu kata petunjuk" value="${wv}" autocomplete="off" oninput="ui.sdW=this.value" onfocus="ui.sdFoc=1" onblur="ui.sdFoc=0">
        <select id="sdN" class="ordsel" onchange="ui.sdN=+this.value">${[1,2,3,4,5,6,7,8,9].map(k=>`<option value="${k}" ${k===nv?'selected':''}>${k}</option>`).join('')}</select>
        <button class="btn pri" data-act="sdclue">Kirim petunjuk</button></div>
        <div class="bd">Satu kata tanpa spasi, tidak boleh sama dengan kata di papan. Angka = berapa kartu timmu yang terkait petunjuk itu.</div>`;}
    else if(isK&&me.team===T)act='<div>Menyiapkan petunjuk…</div>';
    else if(me&&me.team===T)act=`<div>Tunggu ketua timmu (<b>${kName(T)}</b>) memberi petunjuk.</div>`;
    else act=`<div>${Tn(T)} sedang menyiapkan petunjuk. Timmu berikutnya.</div>`;}
  else{const c=st.clue, used=c.n+1-st.left;
    head=`🔍 <b>${Tn(T)}</b> menebak`;
    const big=`<div class="sdbig sd-${T}">“${esc(c.w)}” <span>${c.n}</span></div>`;
    if(canGuess){
      const s=ui.sdSel;
      act=big+`<div>Sisa tebakan: <b>${st.left}</b> (maks. angka + 1). Salah tebak langsung mengakhiri giliran.</div>`
        +(s!=null?`<div class="sdconfirm"><span>Buka <b>“${esc(termOf(st.words[s]).w)}”</b>?</span><button class="btn pri" data-act="sdguess">✅ Buka kartu</button><button class="btn sm" data-act="sdinfo" data-i="${s}">ℹ️ Arti</button><button class="btn sm" data-act="sdcancel">Batal</button></div>`
          :'<div class="bd">Ketuk kartu yang menurutmu terkait petunjuk, lalu tekan Buka kartu. Diskusikan dulu dengan tim!</div>')
        +`<div class="row"><button class="btn" data-act="sdend" ${used>0?'':'disabled'}>✋ Akhiri giliran tim</button></div>`;}
    else if(isK&&me.team===T)act=big+`<div>Timmu sedang menebak (${used} kartu dibuka). Ketua dilarang memberi isyarat 🤐</div>`;
    else if(me&&me.team===T)act=big+'<div>Timmu sedang menebak.</div>';
    else act=big+`<div>${Tn(T)} sedang menebak.</div>`;}
  const teamBox=t=>{const m=sdTeamNames(st,t);
    return `<div class="sdteam sd-${t} ${!ended&&T===t?'on':''}"><div class="sdth"><b>${t==='r'?'🔴':'🔵'} ${Tn(t)}</b><span class="sdleft">${left(t)}<small> kartu lagi</small></span></div>
      <div class="sdmem">${m.map(i=>`<span class="${i===mi?'me':''}"><span class="dot ${ONLINE.has(st.players[i].id)?'on':''}"></span>${st.players[i].ketua?'🎖️':''}${esc(nm(st,i))}</span>`).join('')}</div>
      <div class="sdcl">${(st.clues||[]).filter(c=>c.t===t).map(c=>`<span>“${esc(c.w)}” ${c.n}</span>`).join('')||'<span class="mute">Belum ada petunjuk</span>'}</div></div>`;};
  const logs=st.log.slice(-14).reverse().map(l=>`<div>${l.p>=0?`<b>${esc(nm(st,l.p))}</b> `:''}${esc(l.m)}</div>`).join('');
  $('#app').innerHTML=`<div class="sd-wrap">
    <section class="panel">
      <div class="turnbar"><div class="who"><span class="pill playing" style="margin:0 6px 0 0">🕵️ SANDI</span>${head}${timerHTML(st)}</div>
        <div class="row" style="gap:6px">${isK&&!ended?`<button class="btn sm" data-act="sdkey">${spy?'🙈 Sembunyikan kunci':'👁 Lihat kunci'}</button>`:mi<0?'<span class="bd">👀 Menonton</span>':''}<button class="btn sm" data-act="tutorial" data-w="sandi">📖</button></div></div>
      <div class="sdteams">${teamBox('r')}${teamBox('b')}</div>
    </section>
    <section class="panel ract sdact">${act}</section>
    <section class="panel"><div class="sdboard">${cards}</div>
      <div class="sdlegend bd">${spy&&!ended?'Kamu ketua: kartu bergaris menunjukkan kunci (🔴 Merah, 🔵 Biru, ⬜ netral, 💥 Audit). Hanya ketua yang melihatnya.':'Ketuk kartu yang sudah terbuka untuk membaca arti istilahnya.'}</div></section>
    <details class="panel log" ${ui.logOpen?'open':''} ontoggle="ui.logOpen=this.open"><summary style="font-family:Fraunces,serif;font-weight:600;font-size:15px;cursor:pointer">Catatan permainan</summary>${logs}</details>
  </div>`;
  if(ui.sdFoc){const x=$('#sdW');if(x){x.focus();const L=x.value.length;try{x.setSelectionRange(L,L);}catch(e){}}}
  if(!ended&&mi>=0){ui.sdRoleShown=ui.sdRoleShown||{};if(!ui.sdRoleShown[cur.gid]){ui.sdRoleShown[cur.gid]=true;setTimeout(()=>{if(cur&&cur.st&&cur.st.game==='sandi'&&cur.st.status==='playing'&&!modalOpen())sdRoleModal();},400);}}
  maybeEndPopup(st);
}
function sdRoleModal(){
  const st=cur.st, mi=meIdx(st); if(mi<0)return; const p=st.players[mi], t=p.team;
  openModal(`<div class="endm"><div class="big">${t==='r'?'🔴':'🔵'}</div><h3>Kamu di Tim ${TEAMNAME[t]}${p.ketua?' · 🎖️ Ketua':''}</h3>
    <p style="font-size:14.5px;line-height:1.55">${p.ketua?'Kamu melihat kunci warna semua kartu. Beri petunjuk <b>satu kata + angka</b> supaya timmu menebak kartu warnamu. Jangan sampai mereka membuka 💥 Kartu Audit.':'Tunggu petunjuk dari ketua timmu, lalu diskusikan dan ketuk kartu yang menurutmu terkait. Salah tebak mengakhiri giliran, dan 💥 Kartu Audit membuat timmu langsung kalah.'}</p>
    <p class="bd">${TEAMNAME[st.starter]===TEAMNAME[t]?'Timmu jalan duluan dan harus membuka 9 kartu.':'Tim lawan jalan duluan. Timmu harus membuka 8 kartu.'}</p>
    <div class="mbtns"><button class="btn pri" data-act="close">Siap!</button></div></div>`);
}
function sdInfo(i){
  const st=cur.st, ref=st.words[i], w=termOf(ref), r=st.rev[i], mi=meIdx(st), me=mi>=0?st.players[mi]:null;
  const showC=r||st.status!=='playing'||(me&&me.ketua&&ui.sdKey!==false);
  const c=r?r.c:showC?sandiKey(st)[i]:null;
  const cn=c?`<span class="sdpill c-${c}">${c==='x'?'💥 Kartu Audit':c==='n'?'Netral':'Kartu '+TEAMNAME[c]}</span>`:'';
  openModal(`<h3>${esc(w.w)}</h3><div style="margin:6px 0">${mkChip(ref.mk,w.wk)} <span class="bd">${esc((MK_INFO[ref.mk]||{}).full||'')}</span> ${cn}</div>
    <p style="font-size:15px;line-height:1.55;margin:8px 0">${esc(w.d||'')}</p>
    ${r&&st.players[r.by]?`<p class="bd">Dibuka oleh ${esc(nm(st,r.by))} (Tim ${TEAMNAME[r.t]}).</p>`:''}
    <div class="mbtns"><button class="btn pri" data-act="close">Tutup</button></div>`);
}
function sdClick(i){
  const st=cur.st, mi=meIdx(st), me=mi>=0?st.players[mi]:null;
  const canGuess=st.status==='playing'&&me&&!me.ketua&&me.team===st.turnTeam&&st.phase==='guess'&&canWrite!==false&&!st.paused;
  if(canGuess&&!st.rev[i]){if(ui.sdSel===i){sdGuess();return;}ui.sdSel=i;render();return;}
  sdInfo(i);
}
function sdGuess(){const i=ui.sdSel;if(i==null)return;ui.sdSel=null;hubMove({type:'guess',i});}
function sdSendClue(){
  const w=(($('#sdW')||{}).value||'').trim(), n=+(($('#sdN')||{}).value||1);
  if(!w)return toast('Tulis satu kata petunjuk');
  ui.sdFoc=0; hubMove({type:'clue',word:w,num:n}).then(()=>{const s=cur&&cur.st;if(s&&s.phase==='guess'&&s.clue&&s.clue.w===w){ui.sdW='';ui.sdN=1;}});
}

/* ---------- akhir permainan ---------- */
function openSDEnd(){
  const st=cur.st, mi=meIdx(st), me=mi>=0?st.players[mi]:null, W=st.winner;
  const title=!me?`Tim ${TEAMNAME[W]} menang`:me.team===W?'Timmu menang! 🎉':'Timmu kalah';
  const list=t=>sdTeamNames(st,t).map(i=>`<div class="rki ${t===W?'win':''} ${i===mi?'me':''}"><span class="pos">${t==='r'?'🔴':'🔵'}</span><span class="nm">${esc(nm(st,i))}${i===mi?' <span class="mine" style="font-size:12px">(kamu)</span>':''}<div class="bd" style="font-weight:400">${st.players[i].ketua?'🎖️ Ketua':'Penebak'} · Tim ${TEAMNAME[t]}</div></span></div>`).join('');
  const clues=(st.clues||[]).map(c=>`<span class="sdpill c-${c.t}">“${esc(c.w)}” ${c.n}</span>`).join(' ');
  openModal(`<div class="endm"><div class="big">${W==='r'?'🔴':'🔵'}</div><h3>${title}</h3><p class="why"><b>Tim ${TEAMNAME[W]}</b> menang: ${esc(st.winBy||'')}.</p>
    <div class="rkl">${list(W)}${list(sandiOther(W))}</div>
    ${clues?`<p class="bd" style="margin:10px 0 4px">Petunjuk yang dipakai:</p><div class="sdclues">${clues}</div>`:''}
    <p class="bd" style="margin:10px 0 0">Tercatat di 📜 Riwayat dan rekor 👤 Profil. Sandi Syndicate belum menambah poin peringkat.</p>
    <div class="mbtns"><button class="btn" data-act="close">Lihat papan</button><button class="btn pri" data-act="lobby">Kembali ke lobi</button></div></div>`);
}

/* ---------- aturan ---------- */
function sandiRules(){
  return `<h3>🕵️ Sandi Syndicate (4–8 pemain, 2 tim)</h3>
  <p>Dua tim, <b>Merah</b> dan <b>Biru</b>, berlomba menemukan kartu timnya di papan berisi <b>25 istilah materi MK</b>. Tiap tim punya satu <b>🎖️ Ketua</b>; anggota lain adalah <b>penebak</b>.</p>
  <ul>
    <li><b>Kunci rahasia.</b> Tim yang jalan duluan punya 9 kartu, tim lawan 8 kartu. Ada 7 kartu netral dan 1 <b>💥 Kartu Audit</b>. Hanya ketua yang melihat warna kartu.</li>
    <li><b>Petunjuk.</b> Di gilirannya, ketua memberi <b>satu kata + angka</b>. Contoh: “Modal · 2” artinya ada 2 kartu timnya yang terkait kata “Modal”. Kata petunjuk tidak boleh sama dengan kata di papan, dan ketua dilarang memberi isyarat lain.</li>
    <li><b>Menebak.</b> Penebak berdiskusi lalu membuka kartu satu per satu, paling banyak <b>angka + 1</b> kartu. Kalau yang terbuka kartu timnya, boleh lanjut menebak. Kalau kartu netral atau milik lawan, giliran langsung pindah. Penebak boleh berhenti kapan saja setelah membuka minimal satu kartu.</li>
    <li><b>💥 Kartu Audit.</b> Tim yang membukanya langsung <b>kalah</b>.</li>
    <li><b>Menang.</b> Tim pertama yang membuka semua kartunya menang. Kartu yang dibuka tim lawan untuk timmu tetap dihitung.</li>
    <li><b>Timer.</b> Kalau tuan rumah memasang waktu per tahap dan waktu habis, giliran pindah ke tim lawan.</li>
  </ul>
  <p><b>Sambil belajar:</b> ketuk kartu yang sudah terbuka untuk membaca arti istilahnya, lengkap dengan MK dan minggu materinya. Tuan rumah bisa memilih kata dari satu MK saja atau campuran 6 MK.</p>`;
}
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target&&e.target.id==='sdW'){e.preventDefault();sdSendClue();}});
