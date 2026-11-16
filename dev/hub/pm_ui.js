/* ================= HUB · PEMUKIM NUSANTARA (UI) ================= */
const PM_COL=['#e0434f','#3b7be0','#f39c33','#a35bd6'];
const PM_TCOL={L:'#2f7d4f',B:'#c0613a',W:'#8fc45a',G:'#e3bd3e',O:'#8b93a1',D:'#d8c49a'};
const PM_TEMO={L:'🌳',B:'🧱',W:'🐐',G:'🌾',O:'⛰️',D:'🏜️'};
function pmMe(st){return cur.local?cur.human:meIdx(st);}
function pmRules(){
  return `<h3>🏝️ Pemukim Nusantara (3–4 pemain)</h3>
  <p>Aturan dasar <b>Catan</b> dengan tema Nusantara. Bangun pemukiman, jalan, dan kota di pulau acak. Pemain pertama yang mencapai <b>10 poin</b> di gilirannya sendiri menang.</p>
  <p><b>Persiapan.</b> Tiap pemain menaruh 1 pemukiman + 1 jalan, lalu urutannya dibalik untuk pemukiman + jalan kedua. Pemukiman kedua langsung memberi hasil bumi dari petak di sekitarnya.</p>
  <p><b>Giliranmu:</b></p>
  <ul><li><b>🎲 Lempar dadu.</b> Setiap petak dengan angka itu menghasilkan 1 kartu untuk tiap pemukiman di sudutnya (2 kartu untuk kota). Angka 6 dan 8 paling sering keluar; titik di bawah angka menunjukkan peluangnya.</li>
  <li><b>🦹 Angka 7.</b> Tidak ada yang menghasilkan. Yang memegang lebih dari 7 kartu membuang setengahnya. Pelempar memindahkan perampok (petak itu berhenti menghasilkan) lalu mencuri 1 kartu dari pemain di petak itu.</li>
  <li><b>🔄 Dagang.</b> Dengan bank 4:1, lewat pelabuhan 3:1 atau 2:1 (kalau punya bangunan di pelabuhan), atau tawar-menawar dengan pemain lain.</li>
  <li><b>🔨 Bangun:</b> 🛤️ Jalan = Kayu + Bata · 🏠 Pemukiman (1 poin) = Kayu + Bata + Ternak + Padi · 🏙️ Kota (2 poin, ganti pemukiman) = 2 Padi + 3 Bijih · 🃏 Kartu pembangunan = Ternak + Padi + Bijih.</li></ul>
  <p>Pemukiman harus di ujung jalanmu dan <b>berjarak minimal 2 ruas</b> dari pemukiman siapa pun.</p>
  <p><b>Kartu pembangunan</b> (maks. 1 per giliran, tidak bisa dimainkan di giliran yang sama saat dibeli): ⚔️ Ksatria (pindahkan perampok, boleh sebelum lempar dadu) · 🛤️ Bangun Jalan (2 jalan gratis) · 🎁 Panen Raya (ambil 2 kartu dari bank) · 💰 Monopoli (ambil semua kartu satu jenis dari semua pemain) · 🏆 Poin Kemenangan (rahasia, +1 poin).</p>
  <p><b>Bonus:</b> 🛤️ Jalan Terpanjang (minimal 5 ruas bersambung) = +2 poin. ⚔️ Pasukan Terbesar (minimal 3 Ksatria) = +2 poin. Keduanya bisa direbut pemain lain.</p>
  <p class="mute">Hasil bumi: 🌳 Hutan → 🪵 Kayu · 🧱 Bukit → Bata · 🐐 Padang → Ternak · 🌾 Sawah → Padi · ⛰️ Gunung → ⛏️ Bijih · 🏜️ Tanah tandus tidak menghasilkan.</p>`;
}
function pmBoardSVG(st,me,mode){
  const s=48, G=PM_G, B=st.board, X=x=>(x*s).toFixed(1), parts=[];
  const myTurn=me>=0&&st.turn===me&&st.status==='playing';
  let vOk=[],eOk=[],hOk=[];
  if(myTurn){
    if(st.phase==='setup'){if(st.setup.need==='S')vOk=pmSettleSpots(st,me,true);else eOk=PM_G.verts[st.setup.v].e.filter(e=>st.edge[e]==null);}
    else if(st.phase==='robber')hOk=[...Array(19).keys()].filter(h=>h!==B.robber);
    else if(st.phase==='freeroad'||mode==='road')eOk=pmRoadSpots(st,me);
    else if(mode==='settle')vOk=pmSettleSpots(st,me);
    else if(mode==='city')vOk=pmCitySpots(st,me);
  }
  parts.push(`<defs><radialGradient id="pmsea" cx="50%" cy="50%" r="60%"><stop offset="0%" stop-color="#2a6f9e"/><stop offset="100%" stop-color="#173f63"/></radialGradient></defs>`);
  const R=4.95*s; parts.push(`<polygon points="${[0,1,2,3,4,5].map(k=>{const a=Math.PI/180*(60*k);return (R*Math.cos(a)).toFixed(1)+','+(R*Math.sin(a)).toFixed(1);}).join(' ')}" fill="url(#pmsea)" stroke="#0f2c47" stroke-width="3"/>`);
  B.ports.forEach(pt=>{const E=G.edges[pt.e],A=G.verts[E.a],C=G.verts[E.b],mx=(A.x+C.x)/2,my=(A.y+C.y)/2,l=Math.hypot(mx,my),px=mx+mx/l*0.62,py=my+my/l*0.62;
    parts.push(`<line x1="${X(A.x)}" y1="${X(A.y)}" x2="${X(px)}" y2="${X(py)}" stroke="#e9dcc0" stroke-width="3" stroke-dasharray="3 3"/><line x1="${X(C.x)}" y1="${X(C.y)}" x2="${X(px)}" y2="${X(py)}" stroke="#e9dcc0" stroke-width="3" stroke-dasharray="3 3"/>`);
    parts.push(`<g><circle cx="${X(px)}" cy="${X(py)}" r="17" fill="#f6ecd2" stroke="#7a5a2a" stroke-width="2"/><text x="${X(px)}" y="${(py*s-2).toFixed(1)}" text-anchor="middle" font-size="${pt.t==='any'?11:13}">${pt.t==='any'?'❓':PM_RI[pt.t]}</text><text x="${X(px)}" y="${(py*s+11).toFixed(1)}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#4a3412">${pt.t==='any'?'3:1':'2:1'}</text></g>`);});
  B.hex.forEach((h,i)=>{const pts=G.hv[i].map(v=>X(G.verts[v].x)+','+X(G.verts[v].y)).join(' '), [cx,cy]=G.center[i], hl=hOk.includes(i);
    parts.push(`<polygon points="${pts}" fill="${PM_TCOL[h.t]}" stroke="#f3e6c4" stroke-width="2.5" ${hl?`class="pmhl" data-act="pmh" data-h="${i}"`:''}/>`);
    parts.push(`<text x="${X(cx)}" y="${(cy*s-14).toFixed(1)}" text-anchor="middle" font-size="19" pointer-events="none">${PM_TEMO[h.t]}</text>`);
    if(h.n){const hot=h.n===6||h.n===8, pip=PM_PIPS[h.n];
      parts.push(`<g pointer-events="none" opacity="${i===B.robber?0.45:1}"><circle cx="${X(cx)}" cy="${(cy*s+10).toFixed(1)}" r="14" fill="#f8f0da" stroke="#6b5a3a" stroke-width="1.5"/><text x="${X(cx)}" y="${(cy*s+14).toFixed(1)}" text-anchor="middle" font-size="13" font-weight="800" fill="${hot?'#c0262f':'#2a2216'}">${h.n}</text>
        ${[...Array(pip)].map((_,k)=>`<circle cx="${(cx*s+(k-(pip-1)/2)*3.6).toFixed(1)}" cy="${(cy*s+19.5).toFixed(1)}" r="1.2" fill="${hot?'#c0262f':'#2a2216'}"/>`).join('')}</g>`);}
    if(i===B.robber)parts.push(`<text x="${(cx*s+(h.n?20:0)).toFixed(1)}" y="${(cy*s+(h.n?17:12)).toFixed(1)}" text-anchor="middle" font-size="${h.n?20:26}" pointer-events="none">🦹</text>`);
  });
  st.edge.forEach((p,e)=>{if(p==null)return;const E=G.edges[e],A=G.verts[E.a],C=G.verts[E.b];
    parts.push(`<line x1="${X(A.x)}" y1="${X(A.y)}" x2="${X(C.x)}" y2="${X(C.y)}" stroke="#1b1b1b" stroke-width="9" stroke-linecap="round"/><line x1="${X(A.x)}" y1="${X(A.y)}" x2="${X(C.x)}" y2="${X(C.y)}" stroke="${PM_COL[p]}" stroke-width="6" stroke-linecap="round"/>`);});
  eOk.forEach(e=>{const E=G.edges[e],A=G.verts[E.a],C=G.verts[E.b],c=`x1="${X(A.x)}" y1="${X(A.y)}" x2="${X(C.x)}" y2="${X(C.y)}"`;parts.push(`<line class="pmspot" ${c} stroke="#1b1b1b" stroke-width="11" stroke-linecap="round" opacity=".55"/><line class="pmspot" ${c} stroke="#ffd84d" stroke-width="7" stroke-linecap="round"/><line class="pmhit" data-act="pme" data-e="${e}" ${c} stroke="transparent" stroke-width="22"/>`);});
  st.vtx.forEach((b,v)=>{if(!b)return;const V=G.verts[v],x=V.x*s,y=V.y*s,c=PM_COL[b.p];
    parts.push(b.c?`<path d="M${x-11},${y+8} v-11 l6,-6 l6,6 v-4 h10 v15 z" fill="${c}" stroke="#1b1b1b" stroke-width="2"/>`:`<path d="M${x-8},${y+7} v-8 l8,-7 l8,7 v8 z" fill="${c}" stroke="#1b1b1b" stroke-width="2"/>`);});
  vOk.forEach(v=>{const V=G.verts[v];parts.push(`<circle class="pmspot" data-act="pmv" data-v="${v}" cx="${X(V.x)}" cy="${X(V.y)}" r="10" fill="#fff" stroke="#1b1b1b" stroke-width="2"/><circle class="pmhit" data-act="pmv" data-v="${v}" cx="${X(V.x)}" cy="${X(V.y)}" r="19" fill="transparent"/>`);});
  return `<svg class="pmboard" viewBox="${-5.05*s} ${-4.6*s} ${10.1*s} ${9.2*s}" xmlns="http://www.w3.org/2000/svg">${parts.join('')}</svg>`;
}
function pmDice(d){if(!d)return '';const f=['','⚀','⚁','⚂','⚃','⚄','⚅'];return `<span class="pmdice" title="Dadu: ${d[0]+d[1]}">${f[d[0]]}${f[d[1]]}<b>${d[0]+d[1]}</b></span>`;}
function pmCostHTML(c){return PM_RES.filter(r=>c[r]).map(r=>`${c[r]>1?c[r]:''}${PM_RI[r]}`).join('');}
function pmPhaseText(st,me){
  const t=st.turn, who=t===me?'Kamu':esc(nm(st,t)), mine=t===me;
  if(st.status!=='playing')return `🏁 ${esc(nm(st,st.winner))} menang dengan ${pmVP(st,st.winner,true)} poin`;
  if(st.phase==='setup')return `🏗️ Persiapan · ${who} ${mine?'menaruh':'menaruh'} ${st.setup.need==='S'?(st.setup.i>=st.players.length?'pemukiman kedua':'pemukiman pertama'):'jalan'}${mine?(st.setup.need==='S'?' — ketuk titik putih':' — ketuk ruas kuning'):''}`;
  if(st.phase==='roll')return `🎲 ${who} ${mine?'— lempar dadu':'akan melempar dadu'}`;
  if(st.phase==='discard'){const d=st.disc||{};return `🦹 Angka 7! Menunggu ${Object.keys(d).map(i=>+i===me?'kamu':esc(nm(st,+i))).join(', ')} membuang kartu`;}
  if(st.phase==='robber')return `🦹 ${who} ${mine?'— ketuk petak untuk memindahkan perampok':'memindahkan perampok'}`;
  if(st.phase==='steal')return `🦹 ${who} memilih korban pencurian`;
  if(st.phase==='freeroad')return `🛤️ ${who} membangun ${st.free} jalan gratis`;
  return `🔨 Giliran ${who}${mine?': bangun, dagang, atau akhiri giliran':''}`;
}
function renderPemukim(){
  const st=cur.st, me=pmMe(st), n=st.players.length, P=me>=0?st.players[me]:null, ended=st.status!=='playing', myTurn=!ended&&me>=0&&st.turn===me;
  if(!cur.local)refreshNames(st.players.filter(p=>!p.bot).map(p=>p.id));
  if(!myTurn||st.phase!=='main')ui.pmMode=null;
  const mode=ui.pmMode;
  const pc=P?pmPieces(st,me):null;
  const can=(w)=>{if(!myTurn||st.phase!=='main')return false;const c=PM_COST[w];if(!pmHas(P.res,c))return false;
    if(w==='road')return pc.r<15&&pmRoadSpots(st,me).length>0; if(w==='settle')return pc.s<5&&pmSettleSpots(st,me).length>0; if(w==='city')return pc.c<4&&pmCitySpots(st,me).length>0; return st.devDeck.length>0;};
  let actions='';
  if(myTurn){
    if(st.phase==='roll'){actions=`<button class="btn pri big" data-act="pmroll">🎲 Lempar dadu</button>${P.dev.includes('K')&&!st.devPlayed?'<button class="btn" data-act="pmdev" data-c="K">⚔️ Main Ksatria dulu</button>':''}`;}
    else if(st.phase==='main'){
      const b=(w,ic,lb)=>`<button class="btn ${mode===w?'on':''}" data-act="${w==='dev'?'pmbuydev':'pmmode'}" data-w="${w}" ${can(w)?'':'disabled'} title="${lb}">${ic} ${lb}<span class="pmcost">${pmCostHTML(PM_COST[w])}</span></button>`;
      actions=`<div class="pmbtns">${b('road','🛤️','Jalan')}${b('settle','🏠','Pemukiman')}${b('city','🏙️','Kota')}${b('dev','🃏','Kartu')}</div>
        <div class="row" style="gap:6px"><button class="btn" data-act="pmtrade">🔄 Dagang</button><button class="btn pri" data-act="pmend">✅ Akhiri giliran</button></div>
        ${mode?`<div class="bd">Ketuk ${mode==='road'?'ruas kuning':'titik putih'} di papan untuk membangun ${mode==='road'?'jalan':mode==='settle'?'pemukiman':'kota'}. <a href="#" data-act="pmmode" data-w="">Batal</a></div>`:''}`;}
    else if(st.phase==='freeroad')actions=`<div>Ketuk ruas kuning untuk jalan gratis (sisa ${st.free}).</div><button class="btn sm" data-act="pmskipfree">Lewati</button>`;
    else if(st.phase==='steal')actions=`<div>Pilih korban:</div><div class="row">${st.vic.map(j=>`<button class="btn" data-act="pmsteal" data-v="${j}"><span class="pmdot" style="background:${PM_COL[j]}"></span>${esc(nm(st,j))} (${pmTotal(st.players[j].res)} kartu)</button>`).join('')}</div>`;
  }
  if(!ended&&st.phase==='discard'&&me>=0&&st.disc&&st.disc[me]&&!modalOpen())setTimeout(()=>{if(!modalOpen())pmDiscardModal();},50);
  const hand=P?`<div class="pmhand">${PM_RES.map(r=>`<div class="pmres r-${r}"><span>${PM_RI[r]}</span><b>${P.res[r]}</b><small>${PM_RN[r]}</small></div>`).join('')}</div>`:'';
  const devs=P?(()=>{const all=P.dev.map(c=>({c,nw:false})).concat(P.devNew.map(c=>({c,nw:true})));if(!all.length)return '<div class="bd">Belum punya kartu pembangunan.</div>';
    return `<div class="pmdevs">${all.map(x=>{const playable=myTurn&&!x.nw&&x.c!=='V'&&!st.devPlayed&&(st.phase==='main'||(st.phase==='roll'&&x.c==='K'));
      return `<button class="pmdev ${playable?'ok':''}" ${playable?`data-act="pmdev" data-c="${x.c}"`:'disabled'} title="${x.nw?'Baru dibeli — bisa dimainkan giliran berikutnya':x.c==='V'?'Poin rahasia, otomatis dihitung':''}">${PM_DEVI[x.c]} ${PM_DEVN[x.c]}${x.nw?' <small>baru</small>':''}</button>`;}).join('')}</div>`;})():'';
  const players=st.players.map((p,i)=>{const vp=pmVP(st,i,i===me||ended), dc=p.dev.length+p.devNew.length;
    return `<div class="pmpl ${i===st.turn&&!ended?'turn':''} ${i===me?'me':''}"><span class="pmdot" style="background:${PM_COL[i]}"></span><div class="pmpn"><b>${p.bot?'🤖':''}${esc(nm(st,i))}${i===me?' <span class="mine" style="font-size:11px">(kamu)</span>':''}</b>
      <div class="bd">🃏 ${pmTotal(p.res)} kartu · 📜 ${dc} pembangunan · ⚔️ ${p.knights} · 🛤️ ${st.lens[i]}</div>
      <div>${st.longest===i?'<span class="rtag ld">🛤️ Jalan Terpanjang</span> ':''}${st.largest===i?'<span class="rtag ld">⚔️ Pasukan Terbesar</span>':''}</div></div><div class="pmvp">${vp}<small>poin</small></div></div>`;}).join('');
  const off=st.offer?pmOfferHTML(st,me):'';
  const logs=st.log.slice(-18).reverse().map(l=>`<div>${l.p>=0?`<span class="pmdot sm" style="background:${PM_COL[l.p]}"></span><b>${esc(nm(st,l.p))}</b> `:''}${esc(l.m)}${l.priv&&l.priv[me]?` <i class="mine">(${esc(l.priv[me])})</i>`:''}</div>`).join('');
  const lastL=[...st.log].reverse().find(l=>l.p>=0);
  $('#app').innerHTML=`<div class="pmwrap">
    <section class="panel pmbp"><div class="turnbar"><div class="who">${pmPhaseText(st,me)}${timerHTML(st)}</div><div class="row" style="gap:6px">${pmDice(st.dice)}<button class="btn sm" data-act="tutorial" data-w="pemukim">📖</button></div></div>
      ${pmBoardSVG(st,me,mode)}
      ${lastL?`<div class="bd pmlast"><span class="pmdot sm" style="background:${PM_COL[lastL.p]}"></span><b>${esc(nm(st,lastL.p))}</b> ${esc(lastL.m)}${lastL.priv&&lastL.priv[me]?` <i class="mine">(${esc(lastL.priv[me])})</i>`:''}</div>`:''}</section>
    <aside class="pmside">
      ${P?`<section class="panel"><div class="row" style="justify-content:space-between;align-items:center"><h3 style="font-size:16px"><span class="pmdot" style="background:${PM_COL[me]}"></span>Kartumu</h3><span class="bd">${pmVP(st,me,true)} poin · 🏠 ${5-pc.s} 🏙️ ${4-pc.c} 🛤️ ${15-pc.r} tersisa</span></div>${hand}${devs}${actions?`<div class="pmact">${actions}</div>`:''}</section>`:'<section class="panel"><span class="bd">👀 Kamu menonton meja ini.</span></section>'}
      ${off}
      <section class="panel"><div class="pmpls">${players}</div>${ended?'<button class="btn pri sm" style="margin-top:8px" data-act="showend">Lihat hasil</button>':''}</section>
      <details class="panel log" ${ui.logOpen??(window.innerWidth>760)?'open':''} ontoggle="ui.logOpen=this.open"><summary style="font-family:Fraunces,serif;font-weight:600;font-size:15px;cursor:pointer;margin-bottom:4px">Catatan permainan</summary>${logs}</details>
    </aside></div>`;
  maybeEndPopup(st); pmMaybeBot(); pmOnlineBot();
}
function pmOfferHTML(st,me){
  const o=st.offer, mine=o.from===me;
  const rows=st.players.map((p,j)=>{if(j===o.from)return '';const r=o.resp[j];
    return `<div class="row" style="gap:6px;align-items:center"><span class="pmdot" style="background:${PM_COL[j]}"></span>${p.bot?'🤖':''}${esc(nm(st,j))}: ${r==='yes'?'<b style="color:var(--ok)">✔ mau</b>':r==='no'?'<span class="bd">✘ menolak</span>':'<span class="bd">… menimbang</span>'}
      ${mine&&r==='yes'?`<button class="btn ok sm" data-act="pmaccept" data-p="${j}">Deal!</button>`:''}</div>`;}).join('');
  const ask=!mine&&me>=0&&o.resp[me]==null;
  return `<section class="panel pmoffer"><div><b>🔄 Tawaran ${mine?'kamu':esc(nm(st,o.from))}</b>: memberi <b>${pmResTxt(o.give)}</b>, minta <b>${pmResTxt(o.get)}</b></div>
    ${ask?`<div class="row" style="margin:6px 0"><button class="btn ok sm" data-act="pmresp" data-y="1" ${pmHas(st.players[me].res,o.get)?'':'disabled'}>✔ Mau</button><button class="btn sm" data-act="pmresp" data-y="0">✘ Tolak</button></div>`:''}
    <div style="display:grid;gap:4px;margin-top:6px">${rows}</div>${mine?'<button class="btn sm" style="margin-top:6px" data-act="pmcancel">Batalkan tawaran</button>':''}</section>`;
}
function pmDiscardModal(){
  const st=cur.st, me=pmMe(st); if(!st.disc||!st.disc[me])return;
  const need=st.disc[me], P=st.players[me]; ui.pmDisc=ui.pmDisc&&ui.pmDisc.k===st.v+':'+need?ui.pmDisc:{k:st.v+':'+need,g:{L:0,B:0,W:0,G:0,O:0}};
  const g=ui.pmDisc.g, tot=pmTotal(g);
  openModal(`<h3>🦹 Buang ${need} kartu</h3><p class="bd" style="margin:0 0 10px">Angka 7 keluar dan kamu memegang ${pmTotal(P.res)} kartu. Pilih ${need} kartu untuk dikembalikan ke bank.</p>
    <div class="pmstep">${PM_RES.map(r=>`<div class="pmsrow"><span>${PM_RI[r]} ${PM_RN[r]} <span class="bd">(punya ${P.res[r]})</span></span><span class="wwct"><button class="btn sm" data-act="pmdd" data-r="${r}" data-d="-1" ${g[r]?'':'disabled'}>−</button><b>${g[r]}</b><button class="btn sm" data-act="pmdd" data-r="${r}" data-d="1" ${g[r]<P.res[r]&&tot<need?'':'disabled'}>+</button></span></div>`).join('')}</div>
    <div class="mbtns"><button class="btn pri" data-act="pmdiscok" ${tot===need?'':'disabled'}>Buang ${tot}/${need}</button></div>`);
}
function pmTradeModal(tab){
  const st=cur.st, me=pmMe(st), P=st.players[me]; tab=tab||ui.pmTab||'bank'; ui.pmTab=tab;
  ui.pmT=ui.pmT||{give:null,get:null,og:{},ot:{}};
  const T=ui.pmT, tabs=`<div class="tabs"><button class="btn sm ${tab==='bank'?'on':''}" data-act="pmtrade" data-t="bank">🏦 Bank & pelabuhan</button><button class="btn sm ${tab==='pl'?'on':''}" data-act="pmtrade" data-t="pl">🤝 Ke pemain</button></div>`;
  let body;
  if(tab==='bank'){
    body=`<p class="bd" style="margin:0 0 6px">1. Pilih yang kamu berikan (rasio tergantung pelabuhanmu):</p><div class="pmpick">${PM_RES.map(r=>{const k=pmRate(st,me,r);return `<button class="btn sm ${T.give===r?'on':''}" data-act="pmtg" data-r="${r}" ${P.res[r]>=k?'':'disabled'}>${PM_RI[r]} ${k}:1<small> (punya ${P.res[r]})</small></button>`;}).join('')}</div>
      <p class="bd" style="margin:10px 0 6px">2. Pilih yang kamu dapat:</p><div class="pmpick">${PM_RES.map(r=>`<button class="btn sm ${T.get===r?'on':''}" data-act="pmtt" data-r="${r}" ${r!==T.give&&st.bank[r]>0?'':'disabled'}>${PM_RI[r]} ${PM_RN[r]}</button>`).join('')}</div>
      <div class="mbtns"><button class="btn" data-act="close">Tutup</button><button class="btn pri" data-act="pmbank" ${T.give&&T.get&&T.give!==T.get&&P.res[T.give]>=pmRate(st,me,T.give)?'':'disabled'}>Tukar ${T.give?pmRate(st,me,T.give)+' '+PM_RN[T.give]:''} → 1 ${T.get?PM_RN[T.get]:''}</button></div>`;
  } else {
    const st2=(k,obj,max)=>PM_RES.map(r=>`<div class="pmsrow"><span>${PM_RI[r]} ${PM_RN[r]}${max?` <span class="bd">(punya ${P.res[r]})</span>`:''}</span><span class="wwct"><button class="btn sm" data-act="pmo" data-k="${k}" data-r="${r}" data-d="-1" ${obj[r]?'':'disabled'}>−</button><b>${obj[r]||0}</b><button class="btn sm" data-act="pmo" data-k="${k}" data-r="${r}" data-d="1" ${(!max||(obj[r]||0)<P.res[r])?'':'disabled'}>+</button></span></div>`).join('');
    body=`<div class="pmtwo"><div><p class="bd" style="margin:0 0 4px"><b>Kamu beri</b></p><div class="pmstep">${st2('og',T.og,true)}</div></div><div><p class="bd" style="margin:0 0 4px"><b>Kamu minta</b></p><div class="pmstep">${st2('ot',T.ot,false)}</div></div></div>
      <p class="bd" style="margin:8px 0 0">Tawaran dikirim ke semua pemain. Pilih siapa yang diajak deal dari yang menjawab "mau".${st.players.some(p=>p.bot)?' Bot menerima kalau tawaranmu membantu mereka dan kamu belum hampir menang.':''}</p>
      <div class="mbtns"><button class="btn" data-act="close">Tutup</button><button class="btn pri" data-act="pmoffer" ${pmTotal(T.og)&&pmTotal(T.ot)&&!PM_RES.some(r=>T.og[r]&&T.ot[r])?'':'disabled'}>Kirim tawaran</button></div>`;
  }
  openModal(`<h3>🔄 Dagang</h3>${tabs}${body}`);
}
function pmDevModal(c){
  const st=cur.st;
  if(c==='Y'){ui.pmY=ui.pmY||[];openModal(`<h3>🎁 Panen Raya</h3><p class="bd" style="margin:0 0 8px">Ambil 2 kartu apa saja dari bank (boleh sama). Terpilih: ${ui.pmY.map(r=>PM_RI[r]).join(' ')||'—'}</p>
    <div class="pmpick">${PM_RES.map(r=>`<button class="btn sm" data-act="pmy" data-r="${r}" ${st.bank[r]>ui.pmY.filter(x=>x===r).length&&ui.pmY.length<2?'':'disabled'}>${PM_RI[r]} ${PM_RN[r]}</button>`).join('')}</div>
    <div class="mbtns"><button class="btn" data-act="pmyclr">Ulang</button><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="pmyok" ${ui.pmY.length===2?'':'disabled'}>Ambil</button></div>`);return;}
  if(c==='M'){openModal(`<h3>💰 Monopoli</h3><p class="bd" style="margin:0 0 8px">Sebut satu jenis hasil bumi. Semua pemain lain wajib menyerahkan seluruh kartu jenis itu kepadamu.</p>
    <div class="pmpick">${PM_RES.map(r=>`<button class="btn" data-act="pmmono" data-r="${r}">${PM_RI[r]} ${PM_RN[r]}</button>`).join('')}</div><div class="mbtns"><button class="btn" data-act="close">Batal</button></div>`);return;}
  pmMove({type:'dev',card:c});
}
async function pmMove(mv){
  const st=cur.st, me=pmMe(st);
  try{pmAct(clone(st),me,mv);}catch(e){return toast(e.message);}
  if(cur.local){const s=clone(st);pmAct(s,me,mv);cur.st=s;ui.pmMode=null;closeModal();render();if(s.status==='ended')onGameEnded(s);return;}
  if(ui.busy)return; ui.busy=true; closeModal();
  try{await commitOnline(s=>{const k=meIdx(s);if(k<0)fail('Kamu bukan pemain meja ini');pmAct(s,k,mv);});ui.pmMode=null;}
  catch(e){if(!e.noop)toast(e.message||'Gagal menyimpan, coba lagi');}
  finally{ui.busy=false;}
}
function pmBotNext(st){
  if(st.status!=='playing')return null;
  if(st.phase==='discard'){const j=Object.keys(st.disc||{}).map(Number).find(j=>st.players[j].bot);return j!=null?{j,mv:pmBotDiscard(st,j)}:null;}
  if(st.offer){const j=st.players.findIndex((p,j)=>p.bot&&j!==st.offer.from&&st.offer.resp[j]==null);if(j>=0)return {j,mv:pmBotRespond(st,j,st.players[j].level||'normal')};}
  const t=st.turn;if(st.players[t].bot){if(st.offer&&st.offer.from!==t)return null;return {j:t,mv:pmBotMove(st,t,st.players[t].level||'normal')};}
  return null;
}
function pmApplyBot(s,j,mv){
  try{pmAct(s,j,mv);}catch(e){
    if(!(e instanceof GameErr))throw e;
    const fb=s.phase==='robber'?pmBotRobber(s,j,'easy'):s.phase==='discard'?pmBotDiscard(s,j):s.phase==='roll'?{type:'roll'}:s.phase==='freeroad'?{type:'skipfree'}:s.phase==='steal'?{type:'steal',v:s.vic[0]}:s.offer&&s.offer.from!==j?{type:'respond',yes:false}:{type:'end'};
    pmAct(s,j,fb);}
}
function pmMaybeBot(){
  if(!cur||!cur.local||cur.botTimer||cur.st.game!=='pemukim')return;
  const st=cur.st, nx=pmBotNext(st); if(!nx)return;
  const fast=st.phase==='setup'||nx.mv.type==='respond'||nx.mv.type==='discard';
  cur.botTimer=setTimeout(()=>{const c0=cur;if(!c0||!c0.local)return;c0.botTimer=null;if(c0.st!==st)return render();
    const s=clone(st), x=pmBotNext(s); if(!x)return render(); pmApplyBot(s,x.j,x.mv); c0.st=s;
    const L=s.log[s.log.length-1]; if(L&&L.priv&&L.priv[c0.human])toast('🦹 '+esc(nm(s,L.p))+': '+L.priv[c0.human]);
    else if(x.mv.type==='roll'&&s.dice&&s.dice[0]+s.dice[1]===7)toast('🎲 '+nm(s,x.j)+' melempar 7!');
    if(s.status==='ended')onGameEnded(s); render();},fast?380:st.phase==='roll'?900:750);
}
function pmOnlineBot(){
  if(!cur||cur.local||!cur.st||cur.st.game!=='pemukim'||canWrite===false||!myId)return;
  const st=cur.st; if(st.status!=='playing')return; const nx=pmBotNext(st); if(!nx)return;
  const key=cur.gid+':'+st.v; if(ui.obKey===key)return;
  const humans=st.players.filter(q=>!q.bot).map(q=>q.id), order=[st.host,...humans.filter(x=>x!==st.host)];
  const runner=order.find(id=>id===myId||ONLINE.has(id)), stalled=st.turnAt&&Date.now()-st.turnAt>9000;
  if(runner!==myId&&!(stalled&&humans.includes(myId))){if(!ui.obRetry)ui.obRetry=setTimeout(()=>{ui.obRetry=null;pmOnlineBot();},4000);return;}
  ui.obKey=key; const v=st.v;
  setTimeout(()=>{if(!cur||cur.local||!cur.st||cur.st.v!==v)return;
    commitOnline(s=>{if(s.status!=='playing'||s.v!==v)throw NOOP;const x=pmBotNext(s);if(!x)throw NOOP;pmApplyBot(s,x.j,x.mv);}).catch(()=>{ui.obKey=null;});
  },nx.mv.type==='respond'||st.phase==='setup'?450:850);
}
function pmTimeoutMove(st,j){
  if(st.phase==='discard')return pmBotDiscard(st,j);
  if(st.phase==='setup'||st.phase==='robber'||st.phase==='steal')return pmBotMove(st,j,'easy');
  if(st.phase==='roll')return {type:'roll'}; if(st.phase==='freeroad')return {type:'skipfree'};
  if(st.offer&&st.offer.from===j)return {type:'cancel'}; return {type:'end'};
}
function pmTimeoutRun(s){ // jalankan langkah minimal sampai giliran berganti
  const t0=s.turn, r0=s.round; let k=0;
  while(s.status==='playing'&&k++<40){const pend=pmPending(s);if(s.turn!==t0||s.round!==r0)break;const j=s.phase==='discard'?pend[0]:s.turn;pmApplyBot(s,j,pmTimeoutMove(s,j));if(s.phase==='roll'&&s.turn!==t0)break;}
}
function pmLocalSetup(){
  const last=ui.lastPm||{me:ui.nick||'Kamu',bots:randomBots(3),level:'normal',order:'random',timer:0};
  openModal(`<h3>🏝️ Pemukim Nusantara · lawan bot</h3><p class="mute" style="font-size:14px;margin:0 0 10px">Main 3–4 pemain bersama bot. Bot jalan otomatis dan bisa diajak dagang.</p>
    <div class="row" style="align-items:flex-end">
      <label class="field">Nama kamu<input id="pmMe" maxlength="20" value="${esc(last.me)}"></label>
      <label class="field" style="min-width:0">Jumlah bot<select id="pmN" style="min-width:90px">${[2,3].map(n=>`<option ${n===last.bots.length?'selected':''}>${n}</option>`).join('')}</select></label>
      <label class="field" style="min-width:0">Level<select id="pmLv" style="min-width:110px"><option value="easy" ${last.level==='easy'?'selected':''}>Santai</option><option value="normal" ${last.level==='normal'?'selected':''}>Normal</option><option value="hard" ${last.level==='hard'?'selected':''}>Sulit</option></select></label>
      <label class="field" style="min-width:0">Urutan giliranmu<select id="pmOrd" style="min-width:120px">${ordOptions(4,last.order)}</select></label>
      <label class="field" style="min-width:0">⏱ Waktu per giliran<select id="pmTmr" style="min-width:120px">${timerOptions(last.timer||0)}</select></label>
    </div>
    <div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="pmlocalgo">Mulai</button></div>`);
}
function pmLocalStart(){
  const me=($('#pmMe').value.trim())||'Kamu', nb=+$('#pmN').value, level=$('#pmLv').value, ord=$('#pmOrd').value, tmr=+($('#pmTmr').value||0);
  const bots=randomBots(nb); ui.lastPm={me,bots,level,order:ord,timer:tmr};
  const total=nb+1, hpos=ord==='random'?Math.floor(Math.random()*total):Math.min(+ord,total-1);
  const players=bots.map((b,i)=>({id:'B'+i,nick:b,bot:true,level})); players.splice(hpos,0,{id:'H',nick:me});
  const s={name:'Pemukim lawan bot',game:'pemukim',mode:'pemukim',status:'lobby',players,v:1}; pmStart(s); s.timer=tmr; s.turnAt=Date.now();
  s.log.push({p:-1,m:`Urutan giliran${ord==='random'?' (diacak)':''}: kamu ${ORD_NAMES[hpos].toLowerCase()}.`});
  if(cur&&cur.unsub)cur.unsub(); if(cur&&cur.botTimer)clearTimeout(cur.botTimer); ui.guideFrom=null;
  cur={local:true,st:s,human:hpos,level,lid:'b'+Date.now().toString(36)+Math.random().toString(36).slice(2,6)}; ui.rec=[]; view='table'; ui.pmMode=null; closeModal(); render();
}
async function pmOnEnded(st){
  const rid=cur.local?cur.lid:'g_'+cur.gid; if(!rid||ui.saved[rid])return; ui.saved[rid]=true;
  const vp=st.players.map((p,i)=>pmVP(st,i,true)), order=st.players.map((p,i)=>i).sort((a,b)=>(a===st.winner?-1:b===st.winner?1:vp[b]-vp[a]));
  const rankOf={};order.forEach((i,k)=>rankOf[i]=k+1);
  const players=st.players.map((p,i)=>({id:cur.local?(i===cur.human?myId:null):(p.bot?null:p.id),nick:p.nick||NAMES[p.id]||'',bot:!!p.bot,pts:vp[i],cards:0,rank:rankOf[i]}));
  const ts=Date.now();
  const doc={variant:'pemukim',mode:cur.local?'bot':'online',level:cur.local?cur.level:null,name:st.name||'',endedAt:ts,week:weekKey(ts),rounds:st.round,ids:players.filter(p=>p.id).map(p=>p.id),players,award:{},log:st.log.slice(-40).map(l=>({p:l.p,m:l.m}))};
  try{const ref=db.doc('results/'+rid);await lease(ref);const ex=await ref.get();if(!ex.exists){await ref.set(doc);for(const uid of doc.ids){try{await bumpStats(uid,doc,rid);}catch(e){}}}}catch(e){}
  if(!cur.local&&cur.gid){const g=cur.gid;setTimeout(()=>{db.doc('games/'+g).delete().catch(()=>{});},20000);}
}
function openPmEnd(){
  const st=cur.st, me=pmMe(st), vp=st.players.map((p,i)=>pmVP(st,i,true));
  const order=st.players.map((p,i)=>i).sort((a,b)=>(a===st.winner?-1:b===st.winner?1:vp[b]-vp[a]));
  const win=st.winner===me;
  const list=order.map((i,k)=>{const p=st.players[i],pc=pmPieces(st,i),vd=p.dev.concat(p.devNew).filter(c=>c==='V').length;
    return `<div class="rki ${k===0?'win':''} ${i===me?'me':''}"><span class="pos">${['🥇','🥈','🥉','4'][k]}</span><span class="nm"><span class="pmdot" style="background:${PM_COL[i]}"></span>${p.bot?'🤖':''}${esc(nm(st,i))}${i===me?' <span class="mine" style="font-size:12px">(kamu)</span>':''}<div class="bd" style="font-weight:400">🏠 ${pc.s} · 🏙️ ${pc.c}${st.longest===i?' · 🛤️ Jalan Terpanjang':''}${st.largest===i?' · ⚔️ Pasukan Terbesar':''}${vd?' · 🏆 '+vd+' kartu poin':''}</div></span><span class="pt">${vp[i]}</span></div>`;}).join('');
  openModal(`<div class="endm"><div class="big">${win?'🏆':'🏝️'}</div><h3>${me<0?esc(nm(st,st.winner))+' menang':win?'Kamu menang! 🎉':esc(nm(st,st.winner))+' menang'}</h3><p class="why">Mencapai ${vp[st.winner]} poin di ronde ${st.round}.</p>
    <div class="rkl">${list}</div><p class="bd" style="margin:10px 0 0">Tercatat di 📜 Riwayat dan rekor 👤 Profil${cur.local?'':''}. Pemukim belum menambah poin peringkat.</p>
    <div class="mbtns"><button class="btn" data-act="close">Lihat papan</button>${cur.local?'<button class="btn" data-act="pmagain">🔁 Main lagi</button>':''}<button class="btn pri" data-act="lobby">Kembali ke lobi</button></div></div>`);
}
