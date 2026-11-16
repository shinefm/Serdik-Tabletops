/* ================= HUB: mesin aturan Sandi Syndicate & Rapat Rahasia ================= */
const GAMES={
  permata:{icon:'💎',name:'Saudagar Permata',min:2,max:4},
  duel:{icon:'⚔️',name:'Saudagar Duel',min:2,max:2},
  sandi:{icon:'🕵️',name:'Sandi Syndicate',min:4,max:8},
  rapat:{icon:'🏛️',name:'Rapat Rahasia Direksi',min:5,max:10},
  werewolf:{icon:'🐺',name:'Werewolf Satu Malam',min:3,max:10},
  pemukim:{icon:'🏝️',name:'Pemukim Nusantara',min:3,max:4},
  wwk:{icon:'🐺',name:'Werewolf Klasik',min:6,max:20}
};
function gameOf(st){return st&&st.game?st.game:(st&&st.mode==='duel'?'duel':'permata');}
function isHubGame(st){const g=st&&st.game;return g==='sandi'||g==='rapat'||g==='werewolf'||g==='pemukim'||g==='wwk';}
function rndSeed(){return Math.random().toString(36).slice(2,10);}
function obf(str,seed){let h=2166136261;for(const ch of String(seed))h=Math.imul(h^ch.charCodeAt(0),16777619)>>>0;let o='';
  for(let i=0;i<str.length;i++){h=Math.imul(h^(i+7),2654435761)>>>0;o+=((str.charCodeAt(i)^(h&255))).toString(16).padStart(2,'0');}return o;}
function deobf(hex,seed){let h=2166136261;for(const ch of String(seed))h=Math.imul(h^ch.charCodeAt(0),16777619)>>>0;let o='';
  for(let i=0;i<hex.length/2;i++){h=Math.imul(h^(i+7),2654435761)>>>0;o+=String.fromCharCode(parseInt(hex.substr(i*2,2),16)^(h&255));}return o;}

/* ---------- SANDI SYNDICATE ---------- */
const TEAMNAME={r:'Merah',b:'Biru'}, CARDNAME={r:'Merah',b:'Biru',n:'Netral',x:'AUDIT'};
function sandiOther(t){return t==='r'?'b':'r';}
function sandiMembers(st,t){return st.players.map((p,i)=>i).filter(i=>st.players[i].team===t);}
function sandiNormalize(st){
  st.players.forEach(p=>{if(p.team!=='r'&&p.team!=='b'){const r=st.players.filter(q=>q.team==='r').length,b=st.players.filter(q=>q.team==='b').length;p.team=r<=b?'r':'b';}});
  ['r','b'].forEach(t=>{const m=sandiMembers(st,t);let k=m.filter(i=>st.players[i].ketua);
    if(!k.length&&m.length)st.players[m[0]].ketua=true;
    k.slice(1).forEach(i=>st.players[i].ketua=false);});
}
function sandiLobbyOk(st){sandiNormalize(st);return sandiMembers(st,'r').length>=2&&sandiMembers(st,'b').length>=2;}
function sandiStart(st){
  if(st.players.length<4)fail('Butuh minimal 4 pemain');
  if(!sandiLobbyOk(st))fail('Tiap tim butuh minimal 2 orang');
  const pool=shuffle(packTerms(st.pack||'mix'));
  const seen=new Set(),words=[];
  for(const x of pool){const k=x.w.toLowerCase();if(seen.has(k))continue;seen.add(k);words.push({mk:x.mk,i:x.i});if(words.length===25)break;}
  const starter=Math.random()<0.5?'r':'b';
  const key=shuffle([...Array(9).fill(starter),...Array(8).fill(sandiOther(starter)),...Array(7).fill('n'),'x']);
  st.seed=rndSeed(); st.words=words; st.kk=obf(key.join(''),st.seed);
  st.rev=Array(25).fill(null); st.starter=starter; st.turnTeam=starter; st.phase='clue'; st.clue=null; st.left=0;
  st.status='playing'; st.round=1; st.turnAt=Date.now(); st.clues=[];
  st.log=[{p:-1,m:`Permainan dimulai. Tim ${TEAMNAME[starter]} jalan duluan (9 kartu), Tim ${TEAMNAME[sandiOther(starter)]} 8 kartu.`}];
}
function sandiKey(st){return deobf(st.kk,st.seed).split('');}
function sandiLeft(st,t){const k=sandiKey(st);let n=0;k.forEach((c,i)=>{if(c===t&&!st.rev[i])n++;});return n;}
function sandiSwitch(st){st.turnTeam=sandiOther(st.turnTeam);st.phase='clue';st.clue=null;st.left=0;if(st.turnTeam===st.starter)st.round++;st.turnAt=Date.now();}
function sandiEnd(st,winner,why){st.status='ended';st.winner=winner;st.winBy=why;st.endedAt=Date.now();st.turnAt=null;}
function sandiAct(st,pi,mv){
  if(st.status!=='playing')fail('Permainan sudah selesai');
  if(mv.type==='timeout'){
    st.log.push({p:-1,m:`⏱ Tim ${TEAMNAME[st.turnTeam]} kehabisan waktu ${st.phase==='clue'?'memberi petunjuk':'menebak'} — giliran pindah.`});
    sandiSwitch(st);return;}
  const p=st.players[pi]; if(!p)fail('Kamu bukan pemain meja ini');
  if(p.team!==st.turnTeam)fail('Belum giliran timmu');
  const team=p.team;
  if(mv.type==='clue'){
    if(st.phase!=='clue')fail('Petunjuk sudah diberikan');
    if(!p.ketua)fail('Hanya ketua tim yang memberi petunjuk');
    const w=String(mv.word||'').trim(), n=mv.num|0;
    if(!w)fail('Tulis satu kata petunjuk');
    if(/\s/.test(w))fail('Petunjuk harus satu kata (tanpa spasi)');
    if(w.length>24)fail('Petunjuk terlalu panjang');
    if(n<1||n>9)fail('Angka petunjuk 1–9');
    const lw=w.toLowerCase();
    st.words.forEach((ref,i)=>{if(st.rev[i])return;const bw=termOf(ref).w.toLowerCase();
      if(bw===lw||bw.split(/[\s/-]+/).some(part=>part.length>=3&&part===lw))fail('Petunjuk tidak boleh sama dengan kata di papan');});
    st.clue={w,n,t:team,by:pi}; st.left=n+1; st.phase='guess'; st.turnAt=Date.now();
    st.clues.push({t:team,w,n,r:st.round});
    st.log.push({p:pi,m:`memberi petunjuk “${w}” · ${n}`});
    return;
  }
  if(mv.type==='guess'){
    if(st.phase!=='guess')fail('Tunggu petunjuk dari ketua');
    if(p.ketua)fail('Ketua tidak ikut menebak');
    const i=mv.i|0; if(i<0||i>24)fail('Kartu tidak dikenal'); if(st.rev[i])fail('Kartu sudah dibuka');
    const c=sandiKey(st)[i]; st.rev[i]={c,t:team,by:pi};
    st.log.push({p:pi,m:`membuka “${termOf(st.words[i]).w}” — ${c==='x'?'💥 KARTU AUDIT':c==='n'?'netral':'kartu '+TEAMNAME[c]}`});
    if(c==='x'){sandiEnd(st,sandiOther(team),`Tim ${TEAMNAME[team]} membuka Kartu Audit`);return;}
    if(sandiLeft(st,'r')===0){sandiEnd(st,'r','semua kartu Merah terbuka');return;}
    if(sandiLeft(st,'b')===0){sandiEnd(st,'b','semua kartu Biru terbuka');return;}
    if(c===team){st.left--;if(st.left<=0)sandiSwitch(st);}
    else sandiSwitch(st);
    return;
  }
  if(mv.type==='endturn'){
    if(st.phase!=='guess')fail('Belum ada petunjuk');
    if(p.ketua)fail('Hanya penebak yang mengakhiri giliran');
    if(st.left>=st.clue.n+1)fail('Tebak minimal satu kartu dulu');
    st.log.push({p:pi,m:'mengakhiri giliran tim'});
    sandiSwitch(st);return;
  }
  fail('Aksi tidak dikenal');
}

/* ---------- RAPAT RAHASIA DIREKSI ---------- */
const RAPAT_SIZES={5:[2,3,2,3,3],6:[2,3,4,3,4],7:[2,3,3,4,4],8:[3,4,4,5,5],9:[3,4,4,5,5],10:[3,4,4,5,5]};
const RAPAT_OKNUM={5:2,6:2,7:3,8:3,9:3,10:4};
const ROLE={I:{n:'Tim Integritas',s:'I'},A:{n:'Auditor Internal',s:'I'},O:{n:'Oknum',s:'O'},D:{n:'Dalang',s:'O'}};
function rapatStart(st){
  const n=st.players.length; if(n<5)fail('Butuh minimal 5 pemain'); if(n>10)fail('Maksimal 10 pemain');
  const k=RAPAT_OKNUM[n], sp=st.special!==false;
  const roles=[...Array(k).fill('O'),...Array(n-k).fill('I')];
  if(sp){roles[0]='D';roles[k]='A';}
  shuffle(roles);
  st.seed=rndSeed(); st.rk=obf(roles.join(''),st.seed);
  st.missions=shuffle(MISSIONS.map((m,i)=>i)).slice(0,5).map((mi,j)=>({m:mi,size:RAPAT_SIZES[n][j],need2:n>=7&&j===3}));
  st.mi=0; st.res=[]; st.leader=Math.floor(Math.random()*n); st.phase='propose'; st.team=[]; st.votes={}; st.rejects=0;
  st.played=[]; st.fc=0; st.lastVote=null; st.lastMission=null; st.status='playing'; st.round=1; st.turnAt=Date.now();
  st.log=[{p:-1,m:`Rapat dimulai: ${n-k} Integritas vs ${k} Oknum. ${st.players[st.leader].nick||'Pemimpin'} memimpin rapat pertama.`}];
}
function rapatRoles(st){return deobf(st.rk,st.seed).split('');}
function rapatSide(r){return ROLE[r].s;}
function rapatEnd(st,w,why){st.status='ended';st.winner=w;st.winBy=why;st.endedAt=Date.now();st.reveal=rapatRoles(st);st.phase='ended';st.turnAt=null;}
function rapatAct(st,pi,mv){
  if(st.status!=='playing')fail('Permainan sudah selesai');
  const n=st.players.length, roles=rapatRoles(st);
  if(!st.players[pi])fail('Kamu bukan pemain meja ini');
  const mis=st.missions[st.mi];
  if(mv.type==='propose'){
    if(st.phase!=='propose')fail('Bukan saatnya mengusulkan tim');
    if(pi!==st.leader)fail('Hanya pemimpin rapat yang mengusulkan tim');
    const t=[...new Set((mv.team||[]).map(x=>x|0))].filter(x=>x>=0&&x<n);
    if(t.length!==mis.size)fail(`Tim proyek ini harus ${mis.size} orang`);
    st.team=t.sort((a,b)=>a-b); st.votes={}; st.phase='vote'; st.turnAt=Date.now();
    st.log.push({p:pi,m:`mengusulkan tim: ${st.team.map(i=>st.players[i].nick||'?').join(', ')}`});
    return;
  }
  if(mv.type==='vote'){
    if(st.phase!=='vote')fail('Bukan saatnya voting');
    if(st.votes[pi]!=null)fail('Kamu sudah memilih');
    st.votes[pi]=!!mv.yes;
    if(Object.keys(st.votes).length<n)return;
    const yes=Object.values(st.votes).filter(Boolean).length, ok=yes>n/2;
    st.lastVote={team:st.team.slice(),votes:{...st.votes},ok,leader:st.leader,mi:st.mi};
    (st.vhist=st.vhist||[]).push(st.lastVote); if(st.vhist.length>30)st.vhist.shift();
    st.log.push({p:-1,m:`Voting ${ok?'DISETUJUI':'DITOLAK'} (${yes} setuju, ${n-yes} tolak).`});
    if(ok){st.phase='mission';st.played=[];st.fc=0;}
    else{st.rejects++;
      if(st.rejects>=5){rapatEnd(st,'O','5 usulan tim berturut-turut ditolak — rapat buntu');return;}
      st.leader=(st.leader+1)%n;st.phase='propose';st.team=[];}
    st.votes={}; st.turnAt=Date.now(); return;
  }
  if(mv.type==='play'){
    if(st.phase!=='mission')fail('Bukan saatnya menjalankan proyek');
    if(!st.team.includes(pi))fail('Kamu tidak ada di tim proyek ini');
    if(st.played.includes(pi))fail('Kartumu sudah masuk');
    const f=mv.card==='f';
    if(f&&rapatSide(roles[pi])!=='O')fail('Tim Integritas selalu mendukung proyek');
    st.played.push(pi); if(f)st.fc++;
    if(st.played.length<st.team.length)return;
    const need=mis.need2?2:1, ok=st.fc<need;
    st.res.push(ok?'s':'f');
    st.lastMission={mi:st.mi,fails:st.fc,size:st.team.length,ok,need};
    (st.mhist=st.mhist||[]).push({mi:st.mi,team:st.team.slice(),fails:st.fc,ok,leader:st.leader});
    st.log.push({p:-1,m:`Proyek “${MISSIONS[mis.m][0]}” ${ok?'BERHASIL ✅':'GAGAL ❌'} (${st.fc} kartu sabotase).`});
    st.played=[]; st.fc=0; st.team=[];
    const s=st.res.filter(x=>x==='s').length, fl=st.res.filter(x=>x==='f').length;
    if(fl>=3){rapatEnd(st,'O','3 proyek gagal');return;}
    if(s>=3){ if(roles.includes('D')){st.phase='shoot';st.turnAt=Date.now();st.log.push({p:-1,m:'3 proyek berhasil! Dalang punya satu kesempatan menebak Auditor Internal.'});return;}
      rapatEnd(st,'I','3 proyek berhasil');return;}
    st.mi++; st.round++; st.rejects=0; st.leader=(st.leader+1)%n; st.phase='propose'; st.turnAt=Date.now(); return;
  }
  if(mv.type==='timeout'){
    const pf=mv.forced?'⏩ Dilanjutkan paksa oleh tuan rumah':'⏱ Waktu habis';
    if(st.phase==='propose'){const t=[];for(let k=0;t.length<mis.size;k++)t.push((st.leader+k)%n);
      st.log.push({p:-1,m:pf+' — tim diusulkan otomatis.'});return rapatAct(st,st.leader,{type:'propose',team:t});}
    if(st.phase==='vote'){const miss=st.players.map((p,i)=>i).filter(i=>st.votes[i]==null);
      st.log.push({p:-1,m:`${pf} — ${miss.length} suara yang belum masuk dihitung Setuju.`});
      for(const i of miss){if(st.phase!=='vote')break;rapatAct(st,i,{type:'vote',yes:true});}return;}
    if(st.phase==='mission'){const miss=st.team.filter(i=>!st.played.includes(i));
      st.log.push({p:-1,m:pf+' — kartu yang belum masuk dihitung Dukung.'});
      for(const i of miss){if(st.phase!=='mission')break;rapatAct(st,i,{type:'play',card:'s'});}return;}
    if(st.phase==='shoot'){const d=roles.indexOf('D');const opts=st.players.map((p,i)=>i).filter(i=>i!==d);
      st.log.push({p:-1,m:pf+' — Dalang menebak secara acak.'});return rapatAct(st,d,{type:'shoot',target:opts[Math.floor(Math.random()*opts.length)]});}
    fail('Tidak ada yang ditunggu');
  }
  if(mv.type==='shoot'){
    if(st.phase!=='shoot')fail('Bukan saatnya menebak');
    if(roles[pi]!=='D')fail('Hanya Dalang yang menebak');
    const t=mv.target|0; if(!st.players[t]||t===pi)fail('Pilih pemain lain');
    st.shot=t; st.log.push({p:pi,m:`menebak ${st.players[t].nick||'?'} sebagai Auditor Internal`});
    if(roles[t]==='A')rapatEnd(st,'O','Dalang berhasil menebak Auditor Internal');
    else rapatEnd(st,'I','3 proyek berhasil dan Auditor tetap tersembunyi');
    return;
  }
  fail('Aksi tidak dikenal');
}
function hubWinners(st){
  if(st.game==='sandi')return st.players.map((p,i)=>p.team===st.winner);
  if(st.game==='rapat'){const r=st.reveal||rapatRoles(st);return st.players.map((p,i)=>rapatSide(r[i])===st.winner);}
  if(st.game==='pemukim')return st.players.map((p,i)=>i===st.winner);
  if(st.game==='wwk'){const R=st.reveal||wkRoles(st);return st.players.map((p,i)=>st.winner==='n'?R[i]==='N':WK_ROLES[R[i]].t===st.winner);}
  if(st.game==='werewolf'){const R=st.reveal;if(!R)return st.players.map(()=>false);return st.players.map((p,i)=>{const t=WW_ROLES[R.fin[i]].t;return t==='v'?R.vw:t==='w'?R.ww:R.dead.includes(i);});}
  return st.players.map(()=>false);
}
function hubAct(st,pi,mv){return st.game==='sandi'?sandiAct(st,pi,mv):st.game==='werewolf'?wwAct(st,pi,mv):st.game==='pemukim'?pmAct(st,pi,mv):st.game==='wwk'?wkAct(st,pi,mv):rapatAct(st,pi,mv);}
function hubStart(st){return st.game==='sandi'?sandiStart(st):st.game==='werewolf'?wwStart(st):st.game==='pemukim'?pmStart(st):st.game==='wwk'?wkStart(st):rapatStart(st);}

/* ---------- WEREWOLF SATU MALAM (One Night Ultimate Werewolf) ---------- */
const WW_ROLES={
  W:{n:'Manusia Serigala',i:'🐺',t:'w',d:'Malam: kenali sesama serigala. Kalau sendirian, boleh mengintip 1 kartu tengah.'},
  M:{n:'Antek Serigala',i:'😈',t:'w',d:'Malam: lihat siapa serigala (mereka tidak tahu kamu). Menang bersama serigala, walau kamu sendiri tewas.'},
  K:{n:'Tukang Batu',i:'🧱',t:'v',d:'Malam: kenali Tukang Batu yang lain. Selalu ada sepasang.'},
  S:{n:'Peramal',i:'🔮',t:'v',d:'Malam: lihat kartu 1 pemain lain, atau 2 kartu tengah.'},
  R:{n:'Pencuri',i:'🦝',t:'v',d:'Malam: tukar kartumu dengan 1 pemain lain, lalu lihat kartu barumu. Pihakmu ikut kartu baru itu.'},
  T:{n:'Pembuat Onar',i:'🃏',t:'v',d:'Malam: tukar kartu 2 pemain lain tanpa melihatnya.'},
  D:{n:'Pemabuk',i:'🍺',t:'v',d:'Malam: tukar kartumu dengan 1 kartu tengah tanpa melihatnya.'},
  I:{n:'Insomnia',i:'🌙',t:'v',d:'Akhir malam: lihat lagi kartumu sendiri, apakah sudah ditukar orang.'},
  H:{n:'Pemburu',i:'🏹',t:'v',d:'Kalau kamu tewas, orang yang kamu pilih saat voting ikut tewas.'},
  N:{n:'Penyamak',i:'🧥',t:'n',d:'Kamu benci pekerjaanmu. Kamu menang hanya kalau KAMU yang tewas.'},
  V:{n:'Warga Desa',i:'🧑‍🌾',t:'v',d:'Tidak punya kemampuan malam. Bantu desa menemukan serigala.'}
};
const WW_KEYS=['W','M','K','S','R','T','D','I','H','N','V'];
const WW_MAX={W:2,M:1,K:2,S:1,R:1,T:1,D:1,I:1,H:1,N:1,V:3};
const WW_TEAM={v:'Desa',w:'Serigala',n:'Sendiri'};
const WW_PRESET=['W','W','S','R','T','V','I','D','M','H','N','V','V'];
function wwPreset(n){return WW_PRESET.slice(0,n+3);}
function wwDeckOf(st){return st.roles&&st.roles.length?st.roles.slice():wwPreset(st.players.length);}
function wwCheckDeck(deck,n){
  if(deck.length!==n+3)fail(`Peran berisi ${deck.length} kartu, padahal butuh ${n+3} (${n} pemain + 3 kartu tengah). Atur ulang peran atau pakai rekomendasi.`);
  if(!deck.includes('W'))fail('Minimal harus ada 1 Manusia Serigala');
  if(deck.filter(x=>x==='K').length===1)fail('Tukang Batu harus sepasang (0 atau 2)');
  WW_KEYS.forEach(k=>{if(deck.filter(x=>x===k).length>WW_MAX[k])fail('Terlalu banyak '+WW_ROLES[k].n);});
}
function wwDeal(st){return deobf(st.dk,st.seed).split('');}
function wwFinal(st){return st.fk?deobf(st.fk,st.seed).split(''):null;}
function wwGet(st,k){try{return JSON.parse(deobf(st[k],st.seed+k))||{};}catch(e){return {};}}
function wwPut(st,k,o){st[k]=obf(JSON.stringify(o),st.seed+k);}
function wwStart(st){
  const n=st.players.length; if(n<3)fail('Butuh minimal 3 pemain'); if(n>10)fail('Maksimal 10 pemain');
  const deck=wwDeckOf(st); wwCheckDeck(deck,n);
  st.inPlay=WW_KEYS.flatMap(k=>deck.filter(x=>x===k));
  shuffle(deck); st.seed=rndSeed(); st.dk=obf(deck.join(''),st.seed); st.fk=null;
  wwPut(st,'ak',{}); wwPut(st,'vk',{}); st.done=[]; st.voted=[];
  st.phase='night'; st.status='playing'; st.round=1; st.turnAt=Date.now();
  st.log=[{p:-1,m:`🌙 Malam tiba. ${n} pemain, 3 kartu di tengah. Peran yang dimainkan: ${st.inPlay.map(k=>WW_ROLES[k].n).join(', ')}.`}];
}
function wwNightOk(st,pi,mv,deal){
  const n=st.players.length, r=deal[pi], other=x=>Number.isInteger(x)&&x>=0&&x<n&&x!==pi, cen=x=>Number.isInteger(x)&&x>=0&&x<3;
  if(mv.skip)return r==='D'?fail('Pemabuk wajib menukar kartu dengan kartu tengah'):{skip:true};
  if(r==='W'){const lone=!deal.some((x,i)=>i<n&&i!==pi&&x==='W');if(!lone||mv.c==null)return {};if(!cen(mv.c))fail('Pilih 1 kartu tengah');return {c:mv.c};}
  if(r==='S'){if(mv.p!=null){if(!other(mv.p))fail('Pilih pemain lain');return {p:mv.p};}
    const c=mv.c||[];if(c.length!==2||!c.every(cen)||c[0]===c[1])fail('Pilih 1 pemain lain atau 2 kartu tengah');return {c:[c[0],c[1]]};}
  if(r==='R'){if(!other(mv.p))fail('Pilih 1 pemain lain');return {p:mv.p};}
  if(r==='T'){const p=mv.ps||[];if(p.length!==2||!p.every(other)||p[0]===p[1])fail('Pilih 2 pemain lain');return {ps:[p[0],p[1]]};}
  if(r==='D'){if(!cen(mv.c))fail('Pilih 1 kartu tengah');return {c:mv.c};}
  return {};
}
function wwResolveNight(st){
  const n=st.players.length, deal=wwDeal(st), cards=deal.slice(), acts=wwGet(st,'ak');
  const sw=(a,b)=>{const t=cards[a];cards[a]=cards[b];cards[b]=t;};
  deal.forEach((r,i)=>{if(i<n&&r==='R'&&acts[i]&&acts[i].p!=null)sw(i,acts[i].p);});
  deal.forEach((r,i)=>{if(i<n&&r==='T'&&acts[i]&&acts[i].ps)sw(acts[i].ps[0],acts[i].ps[1]);});
  deal.forEach((r,i)=>{if(i<n&&r==='D'&&acts[i]&&acts[i].c!=null)sw(i,n+acts[i].c);});
  st.fk=obf(cards.join(''),st.seed); st.phase='day'; st.turnAt=Date.now();
  st.log.push({p:-1,m:'☀️ Pagi tiba. Diskusikan siapa serigala, lalu voting.'});
}
function wwResolveDay(st){
  const n=st.players.length, fin=wwFinal(st), votes=wwGet(st,'vk'), cnt=Array(n).fill(0);
  Object.keys(votes).forEach(k=>{const t=votes[k];if(t!=null&&t>=0&&t<n)cnt[t]++;});
  const mx=Math.max(...cnt); let dead=mx>=2?cnt.map((c,i)=>c===mx?i:-1).filter(i=>i>=0):[];
  dead.slice().forEach(d=>{if(fin[d]==='H'){const t=votes[d];if(t!=null&&!dead.includes(t))dead.push(t);}});
  const P=fin.slice(0,n), wolves=P.map((r,i)=>r==='W'?i:-1).filter(i=>i>=0);
  const tanner=dead.some(d=>P[d]==='N'), wolfDead=dead.some(d=>P[d]==='W');
  let vw,ww,why;
  const nm_=i=>st.players[i].nick||'Pemain '+(i+1);
  if(wolves.length){vw=wolfDead; ww=!wolfDead&&!tanner;
    why=wolfDead?`${dead.filter(d=>P[d]==='W').map(nm_).join(' & ')} (Manusia Serigala) tewas`:tanner?'Penyamak tewas, jadi serigala tidak bisa menang':dead.length?'tidak ada serigala yang tewas':'tidak ada yang tewas, serigala lolos';}
  else{vw=dead.length===0; ww=!tanner&&dead.some(d=>P[d]!=='M')&&P.includes('M');
    why=vw?'tidak ada serigala di antara pemain dan tidak ada yang tewas':'tidak ada serigala di antara pemain, tapi ada warga yang tewas';}
  st.reveal={deal:wwDeal(st),fin,acts:wwGet(st,'ak'),votes,cnt,dead,vw,ww,tanner};
  const winners=[vw?'Desa':null,ww?'Serigala':null,tanner?'Penyamak':null].filter(Boolean);
  st.winner=winners.join('+')||'-'; st.winBy=(winners.length?winners.join(' & ')+' menang: ':'Tidak ada yang menang: ')+why;
  st.status='ended'; st.phase='ended'; st.endedAt=Date.now(); st.turnAt=null;
  st.log.push({p:-1,m:`🗳 Voting selesai. ${dead.length?'Tewas: '+dead.map(d=>nm_(d)+' ('+WW_ROLES[P[d]].n+')').join(', '):'Tidak ada yang tewas'}. ${st.winBy}.`});
}
function wwAct(st,pi,mv){
  if(st.status!=='playing')fail('Permainan sudah selesai');
  const n=st.players.length;
  if(mv.type==='timeout'){
    if(st.phase==='night'){const deal=wwDeal(st),acts=wwGet(st,'ak');
      for(let i=0;i<n;i++)if(!st.done.includes(i)){acts[i]=deal[i]==='D'?{c:Math.floor(Math.random()*3)}:{skip:true};st.done.push(i);}
      wwPut(st,'ak',acts); st.log.push({p:-1,m:(mv.forced?'⏩ Malam diakhiri tuan rumah':'⏱ Malam berakhir')+' — yang belum bertindak dilewati.'}); wwResolveNight(st); return;}
    if(st.phase==='day'){st.log.push({p:-1,m:(mv.forced?'⏩ Diskusi diakhiri tuan rumah':'⏱ Waktu diskusi habis')+` — ${n-st.voted.length} pemain belum memilih.`});wwResolveDay(st);return;}
    fail('Tidak ada yang ditunggu');
  }
  if(!st.players[pi])fail('Kamu bukan pemain meja ini');
  if(mv.type==='night'){
    if(st.phase!=='night')fail('Malam sudah berakhir'); if(st.done.includes(pi))fail('Kamu sudah bertindak malam ini');
    const deal=wwDeal(st), a=wwNightOk(st,pi,mv,deal), acts=wwGet(st,'ak'); acts[pi]=a; wwPut(st,'ak',acts); st.done.push(pi);
    if(st.done.length>=n)wwResolveNight(st); return;
  }
  if(mv.type==='vote'){
    if(st.phase!=='day')fail('Belum saatnya voting'); const t=mv.target;
    if(!Number.isInteger(t)||t<0||t>=n||t===pi)fail('Pilih 1 pemain lain');
    const v=wwGet(st,'vk'); v[pi]=t; wwPut(st,'vk',v); if(!st.voted.includes(pi))st.voted.push(pi);
    if(st.voted.length>=n)wwResolveDay(st); return;
  }
  fail('Aksi tidak dikenal');
}

/* ---------- WEREWOLF KLASIK (banyak malam, 6–20 pemain, aplikasi = moderator) ---------- */
const WK_ROLES={
  W:{n:'Manusia Serigala',i:'🐺',t:'w',d:'Tiap malam (mulai malam ke-2) bersama serigala lain memilih 1 korban. Siang hari berpura-pura jadi warga.'},
  M:{n:'Antek Serigala',i:'😈',t:'w',d:'Tahu siapa serigala, tapi serigala tidak tahu kamu. Di mata Peramal kamu terlihat warga. Menang bersama serigala.'},
  S:{n:'Peramal',i:'🔮',t:'v',d:'Tiap malam memeriksa 1 pemain: serigala atau bukan.'},
  T:{n:'Tabib',i:'🩺',t:'v',d:'Tiap malam melindungi 1 pemain (boleh diri sendiri) dari serigala, tapi tidak boleh orang yang sama 2 malam berturut-turut.'},
  H:{n:'Pemburu',i:'🏹',t:'v',d:'Saat tewas (dimangsa atau dihukum), kamu langsung menembak 1 pemain lain.'},
  N:{n:'Penyamak',i:'🧥',t:'n',d:'Kamu menang sendirian kalau warga menghukummu di siang hari.'},
  V:{n:'Warga Desa',i:'🧑‍🌾',t:'v',d:'Tidak punya kemampuan malam. Temukan dan hukum para serigala.'}
};
const WK_KEYS=['W','M','S','T','H','N','V'];
const WK_MAX={W:6,M:1,S:1,T:1,H:1,N:1,V:20};
function wkPreset(n){const w=n<=8?2:n<=12?3:n<=16?4:5,d=Array(w).fill('W');d.push('S','T');if(n>=8)d.push('H');if(n>=10)d.push('M');if(n>=12)d.push('N');while(d.length<n)d.push('V');return d.slice(0,n);}
function wkDeckOf(st){return st.roles&&st.roles.length?st.roles.slice():wkPreset(st.players.length);}
function wkCheckDeck(d,n){
  if(d.length!==n)fail(`Peran berisi ${d.length} kartu, padahal ada ${n} pemain. Atur ulang peran atau pakai rekomendasi.`);
  const w=d.filter(x=>x==='W').length; if(!w)fail('Minimal harus ada 1 Manusia Serigala'); if(w*2>=n)fail('Serigala terlalu banyak, harus kurang dari separuh pemain');
  WK_KEYS.forEach(k=>{if(d.filter(x=>x===k).length>WK_MAX[k])fail('Terlalu banyak '+WK_ROLES[k].n);});
}
function wkRoles(st){return deobf(st.rk,st.seed).split('');}
function wkNm(st,i){return st.players[i].nick||'Pemain '+(i+1);}
function wkStart(st){
  const n=st.players.length; if(n<6)fail('Butuh minimal 6 pemain'); if(n>20)fail('Maksimal 20 pemain');
  const d=wkDeckOf(st); wkCheckDeck(d,n); st.inPlay=WK_KEYS.flatMap(k=>d.filter(x=>x===k)); shuffle(d);
  st.seed=rndSeed(); st.rk=obf(d.join(''),st.seed); wwPut(st,'ak',{}); wwPut(st,'hk',[]);
  st.alive=Array(n).fill(true); st.deaths=[]; st.night=1; st.day=0; st.done=[]; st.votes={}; st.hunter=null; st.lastProt=null;
  st.phase='night'; st.status='playing'; st.turnAt=Date.now();
  st.log=[{p:-1,m:`🌙 Malam pertama. ${n} warga desa, ${d.filter(x=>x==='W').length} di antaranya serigala. Malam ini serigala hanya saling berkenalan.`}];
}
function wkAliveIdx(st){return st.alive.map((a,i)=>a?i:-1).filter(i=>i>=0);}
function wkKill(st,p,cause){
  const r=wkRoles(st)[p]; st.alive[p]=false; st.deaths.push({p,r,cause,day:st.day,night:st.night});
  return r;
}
function wkWin(st){
  const R=wkRoles(st), al=wkAliveIdx(st), w=al.filter(i=>R[i]==='W').length, o=al.length-w;
  if(!w){wkEnd(st,'v','Semua serigala sudah tewas');return true;}
  if(w>=o){wkEnd(st,'w',`Jumlah serigala (${w}) sudah menyamai warga yang tersisa (${o})`);return true;}
  return false;
}
function wkEnd(st,win,why){
  st.status='ended'; st.phase='ended'; st.winner=win; st.endedAt=Date.now(); st.turnAt=null;
  st.reveal=wkRoles(st); st.hist=wwGet(st,'hk');
  st.winBy=({v:'Desa menang',w:'Serigala menang',n:'Penyamak menang'})[win]+': '+why;
  st.log.push({p:-1,m:'🏁 '+st.winBy+'.'});
}
function wkAfterDeath(st,p,r,then){
  if(r==='H'){st.hunter={p,then};st.phase='hunter';st.turnAt=Date.now();return;}
  wkContinue(st,then);
}
function wkContinue(st,then){
  if(wkWin(st))return;
  if(then==='day'){st.phase='day';st.day++;st.votes={};st.turnAt=Date.now();}
  else{st.phase='night';st.night++;st.done=[];wwPut(st,'ak',{});st.turnAt=Date.now();st.log.push({p:-1,m:`🌙 Malam ke-${st.night} tiba. Semua menutup mata…`});}
}
function wkResolveNight(st){
  const R=wkRoles(st), acts=wwGet(st,'ak'), al=wkAliveIdx(st), rec={night:st.night,wv:{},seer:null,prot:null,target:null,victim:null};
  al.forEach(i=>{const a=acts[i]||{};if(R[i]==='W'&&a.t!=null)rec.wv[i]=a.t;if(R[i]==='S'&&a.t!=null)rec.seer={p:i,t:a.t,wolf:R[a.t]==='W'};if(R[i]==='T'&&a.t!=null)rec.prot=a.t;});
  st.lastProt=rec.prot;
  if(st.night>1){const cnt={};Object.values(rec.wv).forEach(t=>cnt[t]=(cnt[t]||0)+1);const mx=Math.max(0,...Object.values(cnt));
    const top=Object.keys(cnt).filter(k=>cnt[k]===mx).map(Number);if(top.length)rec.target=top[Math.floor(Math.random()*top.length)];}
  let H=wwGet(st,'hk'); if(!Array.isArray(H))H=[]; let dead=null, r=null;
  if(rec.target!=null&&rec.target!==rec.prot&&st.alive[rec.target]){dead=rec.target;rec.victim=dead;r=wkKill(st,dead,'dimangsa serigala');}
  H.push(rec); wwPut(st,'hk',H);
  st.log.push({p:-1,m:st.night===1?'☀️ Pagi pertama. Semua masih hidup.':dead!=null?`☀️ Pagi. ${wkNm(st,dead)} ditemukan tewas dimangsa serigala. Ia ternyata ${WK_ROLES[r].n}.`:'☀️ Pagi. Tidak ada korban malam ini!'});
  if(dead!=null)wkAfterDeath(st,dead,r,'day'); else wkContinue(st,'day');
}
function wkResolveDay(st){
  const al=wkAliveIdx(st), cnt={}; al.forEach(i=>{const t=st.votes[i];if(t!=null)cnt[t]=(cnt[t]||0)+1;});
  const mx=Math.max(0,...Object.values(cnt)), top=Object.keys(cnt).filter(k=>cnt[k]===mx).map(Number);
  st.lastVote={day:st.day,votes:{...st.votes}};
  if(top.length!==1||top[0]<0||mx===0){st.log.push({p:-1,m:`⚖️ Hari ke-${st.day}: ${top.length>1?'suara seri':'tidak ada mayoritas untuk menghukum'}, tidak ada yang dihukum.`});wkContinue(st,'night');return;}
  const p=top[0], r=wkRoles(st)[p];
  wkKill(st,p,'dihukum warga');
  st.log.push({p:-1,m:`⚖️ Hari ke-${st.day}: warga menghukum ${wkNm(st,p)} (${mx} suara). Ia ternyata ${WK_ROLES[r].n}.`});
  if(r==='N'){wkEnd(st,'n',`${wkNm(st,p)} berhasil membuat dirinya dihukum`);return;}
  wkAfterDeath(st,p,r,'night');
}
function wkAct(st,pi,mv){
  if(st.status!=='playing')fail('Permainan sudah selesai');
  const n=st.players.length, R=wkRoles(st), live=i=>Number.isInteger(i)&&i>=0&&i<n&&st.alive[i];
  if(mv.type==='timeout'){
    const pf=mv.forced?'⏩ Dilanjutkan tuan rumah':'⏱ Waktu habis';
    if(st.phase==='night'){const acts=wwGet(st,'ak');wkAliveIdx(st).forEach(i=>{if(!st.done.includes(i)){acts[i]={};st.done.push(i);}});wwPut(st,'ak',acts);st.log.push({p:-1,m:pf+' — yang belum bertindak dilewati.'});wkResolveNight(st);return;}
    if(st.phase==='day'){st.log.push({p:-1,m:pf+' — suara dihitung.'});wkResolveDay(st);return;}
    if(st.phase==='hunter'){const opts=wkAliveIdx(st);const t=opts[Math.floor(Math.random()*opts.length)];st.log.push({p:-1,m:pf+' — Pemburu menembak acak.'});return wkAct(st,st.hunter.p,{type:'shoot',t});}
    fail('Tidak ada yang ditunggu');
  }
  if(!st.players[pi])fail('Kamu bukan pemain meja ini');
  if(mv.type==='shoot'){
    if(st.phase!=='hunter'||st.hunter.p!==pi)fail('Bukan giliran Pemburu');
    if(!live(mv.t))fail('Pilih pemain yang masih hidup');
    const then=st.hunter.then; st.hunter=null; const r=wkKill(st,mv.t,'ditembak Pemburu');
    st.log.push({p:pi,m:`🏹 menembak ${wkNm(st,mv.t)} sebelum tewas. Ia ternyata ${WK_ROLES[r].n}.`});
    wkContinue(st,then); return;
  }
  if(!st.alive[pi])fail('Kamu sudah tewas. Tetap diam ya 🤐');
  if(mv.type==='night'){
    if(st.phase!=='night')fail('Bukan malam hari'); if(st.done.includes(pi))fail('Kamu sudah bertindak malam ini');
    const r=R[pi], a={};
    if(r==='W'&&st.night>1&&!mv.skip){if(!live(mv.t)||R[mv.t]==='W')fail('Pilih korban yang bukan serigala');a.t=mv.t;}
    if(r==='S'&&!mv.skip){if(!live(mv.t)||mv.t===pi)fail('Pilih 1 pemain lain');a.t=mv.t;}
    if(r==='T'&&!mv.skip){if(!live(mv.t))fail('Pilih pemain yang masih hidup');if(mv.t===st.lastProt)fail('Tidak boleh melindungi orang yang sama 2 malam berturut-turut');a.t=mv.t;}
    const acts=wwGet(st,'ak'); acts[pi]=a; wwPut(st,'ak',acts); st.done.push(pi);
    if(wkAliveIdx(st).every(i=>st.done.includes(i)))wkResolveNight(st); return;
  }
  if(mv.type==='vote'){
    if(st.phase!=='day')fail('Voting hanya siang hari');
    if(mv.t!==-1&&(!live(mv.t)||mv.t===pi))fail('Pilih pemain lain yang masih hidup');
    st.votes[pi]=mv.t; if(wkAliveIdx(st).every(i=>st.votes[i]!=null))wkResolveDay(st); return;
  }
  fail('Aksi tidak dikenal');
}
