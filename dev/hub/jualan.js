/* ================= JUALAN YUK (mesin aturan) =================
   Satuan uang: ribuan rupiah (2000 = Rp2.000.000). */
const JY={START:2000,CAP:1200,STEP:50,ROUNDS:5,HIRE:[50,100,150],UP:50,CR:50,
  PROD:{H:150,M:100,L:50},FEE:{E:150,N:100,C:50},SOLD2:50,TARGET:5000,
  Q:['H','M','L'],P:['E','N','C'],QN:{H:'Premium',M:'Standar',L:'Ekonomi'},PN:{E:'Mahal',N:'Normal',C:'Murah'},
  ABL:{H:{E:[3],N:[3],C:[2,3]},M:{E:[3],N:[2,3],C:[1,2,3]},L:{E:[2,3],N:[1,2,3],C:[1,2,3]}},
  FAIL:{H:{E:[1,2],N:[1],C:[]},M:{E:[1,2,3],N:[1],C:[1]},L:{E:[1,2,3,4],N:[1,2,3],C:[1,2]}},
  REV:{H:{E:800,N:650,C:500},M:{E:700,N:550,C:400},L:{E:500,N:450,C:300}},
  DIVS:['fin','hr','op','mk','sl'],DN:{fin:'Keuangan',hr:'SDM',op:'Produksi',mk:'Pemasaran',sl:'Penjualan'},
  TEAMS:[{n:'Tim Merah',c:'#e0524f'},{n:'Tim Biru',c:'#3d8fe0'},{n:'Tim Hijau',c:'#35b26f'},{n:'Tim Ungu',c:'#9a6be0'}]};
function jyRp(k){k=Math.round(k||0);const neg=k<0;k=Math.abs(k);const s=k>=1000?(k/1000).toFixed(k%1000?(k%100?2:1):0).replace('.',',')+' jt':k+' rb';return (neg?'−':'')+'Rp'+s;}
function jyRpFull(k){return 'Rp'+(Math.round(k||0)*1000).toLocaleString('id-ID');}
function jyElig(T,q,p){return JY.ABL[q][p].reduce((a,l)=>a+T.emp[l-1],0);}
function jyChance(q,p,k){const f=JY.FAIL[q][p].length;return (5-f+k)/(5+k);}
function jyMaxDemand(n){return 5;}
function jyNewDemand(n){const mx=jyMaxDemand(n),D={};for(const q of JY.Q){D[q]={};for(const p of JY.P)D[q][p]=Math.floor(Math.random()*(mx+1));}return D;}
const JY_KEYS={h0:'hr',h1:'hr',h2:'hr',u12:'hr',u23:'hr',H:'op',M:'op',L:'op',cr:'mk',sl:'sl'};
function jyNewDraft(){return {h0:0,h1:0,h2:0,u12:0,u23:0,H:0,M:0,L:0,cr:0,sl:0};}
function jyDraftCost(d){const hr=d.h0*50+d.h1*100+d.h2*150+(d.u12+d.u23)*50, op=d.H*150+d.M*100+d.L*50, mk=d.cr*50, sl=d.sl;return {hr,op,mk,sl,tot:hr+op+mk+sl};}
function jyTeamOf(st,pi){const p=st.players[pi];return p&&p.team!=null?p.team:-1;}
function jyHolder(st,t,div){const T=st.teams[t];if(!T)return [];if(T.bot)return [];
  if(st.split)return T.roles[div]!=null?[T.roles[div]]:[];return T.members.slice();}
function jyCan(st,pi,t,div){return jyTeamOf(st,pi)===t&&jyHolder(st,t,div).includes(pi);}
/* ---------- mulai ---------- */
function jyStart(st){
  const n=Math.max(2,Math.min(4,st.nteams||2));
  const cnt=Array(n).fill(0); st.players.forEach(p=>{if(!p.bot&&p.team!=null&&p.team>=0&&p.team<n)cnt[p.team]++;});
  st.players.forEach(p=>{if(p.bot)return;if(p.team==null||p.team<0||p.team>=n){const t=cnt.indexOf(Math.min(...cnt));p.team=t;cnt[t]++;}});
  st.split=!!st.split; st.round=1; st.rounds=JY.ROUNDS; st.status='playing'; st.log=[];
  st.teams=[];
  for(let t=0;t<n;t++){
    const members=st.players.map((p,i)=>i).filter(i=>st.players[i].team===t&&!st.players[i].bot);
    const T={name:JY.TEAMS[t].n,col:JY.TEAMS[t].c,cash:JY.START,bud:{sl:0},draft:jyNewDraft(),emp:[0,0,0],inv:{H:0,M:0,L:0},cr:0,
      members,bot:members.length===0,level:st.botLevel||'normal',roles:{},step:'plan',hist:[JY.START],rev:0,revR:0,sold:0};
    if(st.split&&members.length){JY.DIVS.forEach((d,k)=>{T.roles[d]=members[k%members.length];});}
    st.teams.push(T);
  }
  st.demand=jyNewDemand(n); st.phase='plan'; st.order=null; st.si=0; st.draw=null; st.turnAt=Date.now();
  st.log.push({p:-1,m:`Ronde 1 dimulai · ${n} tim · mode ${st.split?'bagi peran':'sendiri'}. Demand ronde ini sudah keluar.`});
}
/* ---------- tahap ---------- */
function jyAllReady(st){return st.teams.every(T=>T.step==='ready');}
function jyEnterSell(st){
  const idx=st.teams.map((T,i)=>i), tie={};idx.forEach(i=>tie[i]=Math.random());
  idx.sort((a,b)=>st.teams[b].cr-st.teams[a].cr||tie[a]-tie[b]);
  st.order=idx; st.si=0; st.phase='sell'; st.turnAt=Date.now(); st.draw=null;
  const tied=idx.some((i,k)=>k&&st.teams[idx[k-1]].cr===st.teams[i].cr);
  st.log.push({p:-1,m:`Semua tim siap. Urutan jualan (CR tertinggi duluan${tied?', CR sama diundi':''}): ${idx.map(i=>st.teams[i].name+' ('+st.teams[i].cr+')').join(' → ')}.`});
  jySkipStuck(st);
}
function jyCanSell(st,t){const T=st.teams[t];
  for(const q of JY.Q)for(const p of JY.P){if(st.demand[q][p]>0&&T.inv[q]>0&&jyElig(T,q,p)>0&&T.bud.sl>=JY.FEE[p])return true;}return false;}
function jySkipStuck(st){
  while(st.phase==='sell'&&st.si<st.order.length&&!jyCanSell(st,st.order[st.si])){
    const t=st.order[st.si];st.log.push({p:-1,t,m:`${st.teams[t].name} tidak bisa jualan lagi (stok, demand, karyawan, atau anggaran penjualan habis).`});st.si++;}
  if(st.phase==='sell'&&st.si>=st.order.length)jyEndRound(st);
}
function jyEndRound(st){
  st.teams.forEach(T=>{T.hist.push(T.cash);});
  const sum=st.teams.map(T=>`${T.name} ${jyRp(T.cash)}`).join(' · ');
  st.log.push({p:-1,m:`Ronde ${st.round} selesai. Kas: ${sum}.`});
  st.recap={round:st.round,rev:st.teams.map(T=>T.revR),cash:st.teams.map(T=>T.cash)};
  if(st.round>=st.rounds){
    st.status='ended'; st.phase='end';
    const best=Math.max(...st.teams.map(T=>T.cash));
    st.teams.forEach(T=>{T.stars=(T.cash>=JY.TARGET?1:0)+(T.cash===best?1:0);});
    st.winner=st.teams.map((T,i)=>i).filter(i=>st.teams[i].cash===best);
    st.log.push({p:-1,m:`Permainan selesai! Juara: ${st.winner.map(i=>st.teams[i].name).join(' & ')} dengan kas ${jyRp(best)}.`});
    return;
  }
  st.round++; st.demand=jyNewDemand(st.teams.length); st.phase='plan'; st.order=null; st.si=0; st.draw=null; st.turnAt=Date.now();
  st.teams.forEach(T=>{T.step='plan';T.draft=jyNewDraft();T.revR=0;});
  st.log.push({p:-1,m:`Ronde ${st.round} dimulai. Demand baru sudah keluar.`});
}
function jyMul(x){return Number.isInteger(x)&&x>=0&&x%JY.STEP===0;}
/* ---------- aksi ---------- */
function jyAct(st,pi,mv){
  if(st.status!=='playing')fail('Permainan belum/ sudah selesai');
  const t=mv.team!=null&&pi===-9?mv.team:jyTeamOf(st,pi);   // pi=-9: bot/autopilot
  const T=st.teams[t]; if(!T)fail('Kamu bukan anggota tim mana pun');
  const can=div=>pi===-9||jyCan(st,pi,t,div);
  const who=pi>=0?pi:-1;
  switch(mv.type){
    case 'draft':{
      if(st.phase!=='plan'||T.step!=='plan')fail('Rencana ronde ini sudah dikirim');
      const d=mv.d||{};
      for(const k in d){const dv=JY_KEYS[k];if(!dv)continue;if(!can(dv))fail('Bagian '+JY.DN[dv]+' bukan peganganmu');
        let v=Math.max(0,d[k]|0);if(k==='sl')v=Math.floor(v/JY.STEP)*JY.STEP;T.draft[k]=v;}
      return;}
    case 'ready':{
      if(st.phase!=='plan'||T.step!=='plan')fail('Rencana ronde ini sudah dikirim');
      if(!can('fin'))fail('Hanya pemegang Keuangan yang bisa mengirim rencana');
      const d=T.draft, C=jyDraftCost(d);
      if(C.tot>JY.CAP)fail('Belanja maksimal Rp1.200.000 per ronde (sekarang '+jyRp(C.tot)+')');
      if(C.tot>T.cash)fail('Kas tidak cukup');
      if(d.u12>T.emp[0])fail('Karyawan level 1 tidak cukup untuk dilatih');
      if(d.u23>T.emp[1])fail('Karyawan level 2 tidak cukup untuk dilatih');
      T.cash-=C.tot; T.emp[0]+=d.h0-d.u12; T.emp[1]+=d.h1+d.u12-d.u23; T.emp[2]+=d.h2+d.u23;
      T.inv.H+=d.H; T.inv.M+=d.M; T.inv.L+=d.L; T.cr+=d.cr; T.bud.sl+=d.sl;
      st.log.push({p:who,t,m:`${T.name} belanja ${jyRp(C.tot)}: rekrut ${d.h0}/${d.h1}/${d.h2} (L1/L2/L3)${d.u12+d.u23?', latih '+(d.u12+d.u23):''} · produksi ${d.H} premium, ${d.M} standar, ${d.L} ekonomi · CR +${d.cr} · dana jualan +${jyRp(d.sl)}.`,priv:1});
      T.draft=jyNewDraft(); T.step='ready';
      if(jyAllReady(st))jyEnterSell(st);
      return;}
    case 'sell':{
      if(st.phase!=='sell'||st.order[st.si]!==t)fail('Belum giliran timmu jualan');
      if(!can('sl'))fail('Hanya pemegang divisi Penjualan');
      const q=mv.q,p=mv.p,k=mv.k|0; if(!JY.QN[q]||!JY.PN[p])fail('Pilih kotak demand');
      if(![0,2,4].includes(k))fail('Token pasti dibeli per 2 (maks. 4)');
      if(st.demand[q][p]<=0)fail('Demand kotak ini sudah habis');
      if(T.inv[q]<=0)fail('Stok '+JY.QN[q].toLowerCase()+' kosong');
      const el=jyElig(T,q,p); if(el<=0)fail('Belum ada karyawan yang mampu menjual '+JY.QN[q].toLowerCase()+' '+JY.PN[p].toLowerCase());
      const cost=JY.FEE[p]+(k/2)*JY.SOLD2; if(cost>T.bud.sl)fail('Dana jualan tidak cukup');
      T.bud.sl-=cost;
      const pouch=[1,2,3,4,5].concat(Array(k).fill('S')), drawn=pouch[Math.floor(Math.random()*pouch.length)];
      const ok=drawn==='S'||!JY.FAIL[q][p].includes(drawn);
      let units=0,rev=0;
      if(ok){units=Math.min(st.demand[q][p],T.inv[q],el);rev=units*JY.REV[q][p];st.demand[q][p]-=units;T.inv[q]-=units;T.cash+=rev;T.rev+=rev;T.revR+=rev;T.sold+=units;}
      st.draw={t,q,p,k,pouch,drawn,ok,units,rev,cost,at:Date.now(),n:(st.draw&&st.draw.n||0)+1};
      st.log.push({p:who,t,m:`${T.name} mengincar ${JY.QN[q]} · ${JY.PN[p]}${k?` (+${k} token pasti)`:''}: ambil ${drawn==='S'?'token PASTI':'angka '+drawn} → ${ok?`laku ${units} · +${jyRp(rev)}`:'gagal'}.`});
      st.turnAt=Date.now();
      if(!jyCanSell(st,t)){st.si++;jySkipStuck(st);}
      return;}
    case 'stop':{
      if(st.phase!=='sell'||st.order[st.si]!==t)fail('Belum giliran timmu');
      if(!can('sl'))fail('Hanya pemegang divisi Penjualan');
      st.log.push({p:who,t,m:`${T.name} berhenti jualan ronde ini.`}); st.si++; st.turnAt=Date.now(); jySkipStuck(st); return;}
  }
  fail('Aksi tidak dikenal');
}
/* siapa yang sedang ditunggu: [{t,div,who:[pi..]}] */
function jyWaiting(st){
  const W=[]; if(st.status!=='playing')return W;
  if(st.phase==='plan')st.teams.forEach((T,t)=>{if(T.step==='plan')W.push({t,div:'plan',who:T.members.slice()});});
  else if(st.phase==='sell'){const t=st.order[st.si];if(t!=null)W.push({t,div:'sl',who:jyHolder(st,t,'sl')});}
  return W;
}
function jyPending(st){const s=new Set();jyWaiting(st).forEach(w=>w.who.forEach(i=>s.add(i)));return [...s];}
/* ---------- bot ---------- */
function jyBotPlan(st,t){
  const T=st.teams[t], lv=T.level||'normal', r=st.round, R=st.rounds, D=st.demand, d=jyNewDraft(), last=r===R;
  let b=Math.floor(Math.min(JY.CAP,T.cash)/JY.STEP)*JY.STEP;
  const pay=c=>{if(c>b)return false;b-=c;return true;};
  if(lv==='easy'){
    if(pay(150))d.sl=150; const lvl=Math.floor(Math.random()*3); if(!last&&pay(JY.HIRE[lvl]))d['h'+lvl]++; if(T.emp[0]+T.emp[1]+T.emp[2]+d.h0+d.h1+d.h2===0&&pay(150))d.h2++;
    if(Math.random()<.5&&pay(50))d.cr++;
    let g=0;while(b>=50&&g++<8){const q=JY.Q[Math.floor(Math.random()*3)];if(pay(JY.PROD[q]))d[q]++;}
    return d;}
  const slWant=Math.max(0,300-T.bud.sl); if(pay(slWant))d.sl=slWant; else if(pay(150))d.sl=150;
  const need=last?(T.emp[2]?0:1):Math.max(0,(r===1?2:3)-T.emp[2]);
  for(let i=0;i<need;i++)if(b>=300&&pay(150))d.h2++;
  const crN=last?0:r<=2?2:1; for(let i=0;i<crN;i++)if(b>=350)pay(50)&&d.cr++;
  const nT=st.teams.length, dH=D.H.E+D.H.N+D.H.C, dM=D.M.E+D.M.N+D.M.C, l3=T.emp[2]+d.h2;
  let wantH=Math.max(0,Math.min(l3*3,Math.ceil(dH/nT)+1)-T.inv.H), wantM=Math.max(0,Math.min(2,Math.ceil(dM/nT/2))-T.inv.M);
  while(wantH-->0&&pay(150))d.H++;
  while(wantM-->0&&l3>0&&pay(100))d.M++;
  if(T.inv.L===0&&b>=50&&dH<3&&pay(50))d.L++;
  return d;
}
function jyBotSell(st,t){
  const T=st.teams[t], lv=T.level||'normal'; let best=null;
  for(const q of JY.Q)for(const p of JY.P){
    const el=jyElig(T,q,p), d=st.demand[q][p]; if(d<=0||T.inv[q]<=0||el<=0)continue;
    const units=Math.min(d,T.inv[q],el);
    for(const k of [0,2,4]){const cost=JY.FEE[p]+k/2*JY.SOLD2;if(cost>T.bud.sl)continue;
      const ev=jyChance(q,p,k)*units*JY.REV[q][p]-cost+(lv==='easy'?Math.random()*300:0);
      if(!best||ev>best.ev)best={ev,q,p,k};}
  }
  if(!best||best.ev<=0)return {type:'stop'};
  return {type:'sell',q:best.q,p:best.p,k:best.k};
}
/* langkah bot berikutnya (untuk tim bot / pemegang yang AFK): {t,div,mv} */
function jyBotNext(st,all){
  for(const w of jyWaiting(st)){const T=st.teams[w.t];
    if(!(T.bot||all))continue;
    return {t:w.t,div:w.div,mv:w.div==='sl'?jyBotSell(st,w.t):{type:'plan',d:jyBotPlan(st,w.t)}};}
  return null;
}
function jyApplyBot(s,x){
  if(x.mv.type==='plan'){
    try{jyAct(s,-9,{type:'draft',d:x.mv.d,team:x.t});jyAct(s,-9,{type:'ready',team:x.t});}
    catch(e){if(!(e instanceof GameErr))throw e;s.teams[x.t].draft=jyNewDraft();jyAct(s,-9,{type:'ready',team:x.t});}
    return;}
  try{jyAct(s,-9,{...x.mv,team:x.t});}catch(e){if(!(e instanceof GameErr))throw e;jyAct(s,-9,{type:'stop',team:x.t});}
}
