/* ================= SAUDAGAR PERMATA · EKSPANSI KOTA ================= */
/* Pahlawan diganti 3 kartu Kota. Kota direbut kalau poin & kartu bonus memenuhi syarat.
   Merebut kota pertama memicu ronde terakhir; yang punya kota dengan poin terbanyak menang. */
const KOTA={
  jkt:{name:'Jakarta',pts:16,need:{}},
  sby:{name:'Surabaya',pts:14,need:{},same:4},
  plg:{name:'Palembang',pts:13,need:{},same:5},
  smg:{name:'Semarang',pts:13,need:{},each:1},
  bdg:{name:'Bandung',pts:12,need:{g:3,u:3}},
  mdn:{name:'Medan',pts:12,need:{r:4,k:2}},
  mks:{name:'Makassar',pts:12,need:{u:4,w:2}},
  bpn:{name:'Balikpapan',pts:12,need:{k:4,g:2}},
  yog:{name:'Yogyakarta',pts:11,need:{w:3,g:3,r:2}},
  dps:{name:'Denpasar',pts:11,need:{k:3,r:3,u:2}}
};
function kotaReq(id,p){
  const K=KOTA[id], b=bonusOf(p), pts=ptsOf(p), items=[];
  items.push({t:'pts',n:K.pts,ok:pts>=K.pts,have:pts});
  for(const c in K.need)items.push({t:'c',c,n:K.need[c],ok:b[c]>=K.need[c],have:b[c]});
  if(K.same){const mx=Math.max(...COLORS.map(c=>b[c]));items.push({t:'same',n:K.same,ok:mx>=K.same,have:mx});}
  if(K.each){const k=COLORS.filter(c=>b[c]>=K.each).length;items.push({t:'each',n:5,ok:k>=5,have:k});}
  return items;
}
function kotaOk(id,p){return kotaReq(id,p).every(x=>x.ok);}
function kotaOwner(st,id){return (st.kotaBy||{})[id];}
function kotaStart(st){st.patrons=[];st.cities=shuffle(Object.keys(KOTA)).slice(0,3);st.kotaBy={};}
function kotaCheck(st,pi,p){
  if(p.kota)return;
  const ok=st.cities.filter(id=>kotaOwner(st,id)==null&&kotaOk(id,p)).sort((a,b)=>KOTA[b].pts-KOTA[a].pts);
  if(!ok.length)return;
  const id=ok[0]; p.kota=id; st.kotaBy[id]=pi;
  st.log.push({p:pi,m:'🏙️ merebut Kota '+KOTA[id].name+'!'});
  if(!st.endTriggered){st.endTriggered=true;st.log.push({p:-1,m:'Kota pertama sudah direbut: ini ronde terakhir!'});}
}
function kotaRanking(st){
  const r=st.players.map((p,i)=>({i,pts:ptsOf(p),n:p.cards.length,k:p.kota?1:0})).sort((a,b)=>b.k-a.k||b.pts-a.pts||a.n-b.n);
  if(st.status==='ended'&&r[0]&&r[0].k){const w=st.players[r[0].i];st.winBy='merebut Kota '+KOTA[w.kota].name;}
  return r;
}
/* bantuan bot: seberapa kartu warna ini mendekatkan ke kota yang masih kosong */
function kotaHelp(st,p,b,card){
  if(p.kota)return 0;
  const pts=ptsOf(p);
  return st.cities.reduce((s,id)=>{if(kotaOwner(st,id)!=null)return s;const K=KOTA[id], near=pts>=K.pts-5?1.4:1;let v=0;
    if((K.need[card.b]||0)>b[card.b])v+=1;
    if(K.same){const mx=Math.max(...COLORS.map(c=>b[c]));if(b[card.b]===mx&&mx<K.same)v+=0.8;}
    if(K.each&&b[card.b]<K.each)v+=1;
    return s+v*near;},0);
}
/* ---------- tampilan ---------- */
function kotaTile(st,id,p){
  const K=KOTA[id], own=kotaOwner(st,id), req=p?kotaReq(id,p):null;
  const mark=i=>req?(req[i].ok?' ok':' no'):'';
  let k=0;
  const items=[`<span class="kreq kpts${mark(k++)}" title="Minimal ${K.pts} poin">⭐${K.pts}</span>`];
  for(const c in K.need)items.push(`<span class="hsq c-${c}${mark(k++)}" title="${K.need[c]} kartu ${CNAME[c]}">${K.need[c]}</span>`);
  if(K.same)items.push(`<span class="kreq ksame${mark(k++)}" title="${K.same} kartu dari satu warna apa pun">${K.same}× 1 warna</span>`);
  if(K.each)items.push(`<span class="kreq ksame${mark(k++)}" title="Minimal 1 kartu dari tiap warna">1 tiap warna</span>`);
  const ready=req&&own==null&&!p.kota&&req.every(x=>x.ok);
  return `<div class="kota ${own!=null?'taken':''} ${ready?'ready':''}" data-act="kotainfo" data-id="${id}">
    <div class="kn">🏙️ ${esc(K.name)}</div><div class="kr">${items.join('')}</div>
    <div class="ks">${own!=null?`🏁 ${esc(nm(st,own))}`:ready?'✅ Siap direbut':''}</div></div>`;
}
function kotaPanel(st){
  const seat=actor(st), p=seat>=0?st.players[seat]:null;
  return `<div class="kotas">${st.cities.map(id=>kotaTile(st,id,p)).join('')}</div>`;
}
function patronsOrKota(st){
  if(st.mode==='kota')return kotaPanel(st);
  return `<div class="patrons">${st.patrons.map(patronHTML).join('')||'<span class="mute">Semua pahlawan sudah memberi dukungan.</span>'}</div>`;
}
function kotaInfo(id){
  const st=cur.st, K=KOTA[id], seat=actor(st), p=seat>=0?st.players[seat]:null, own=kotaOwner(st,id);
  const lbl=x=>x.t==='pts'?`⭐ Minimal ${x.n} poin`:x.t==='c'?`${x.n} kartu ${wn(x.c)}`:x.t==='same'?`${x.n} kartu dari satu warna apa pun`:'Minimal 1 kartu dari tiap warna (5 warna)';
  const rows=(p?kotaReq(id,p):kotaReq(id,{cards:[],pat:[]})).map(x=>`<div class="krow">${p?(x.ok?'✅':'⬜'):'•'} ${lbl(x)}${p?` <span class="bd">(kamu: ${x.t==='each'?x.have+' warna':x.have})</span>`:''}</div>`).join('');
  openModal(`<h3>🏙️ Kota ${esc(K.name)}</h3>
    <p class="bd" style="margin:0 0 8px">${own!=null?`Sudah direbut ${esc(nm(st,own))}.`:'Kota direbut otomatis di akhir giliran saat semua syarat terpenuhi. Kartu bonus = kartu yang sudah kamu beli.'}</p>
    ${rows}<div class="mbtns"><button class="btn pri" data-act="close">Tutup</button></div>`);
}
function kotaRules(){
  return `<h3>🏙️ Saudagar Permata · Ekspansi Kota (2–4 pemain)</h3>
  <p>Cara main sama dengan <b>Klasik</b> (ambil permata, beli kartu, cadangkan + Emas, maksimal 10 token), dengan dua perbedaan:</p>
  <ul>
    <li><b>Tidak ada pahlawan.</b> Di tengah meja ada <b>3 kartu Kota</b>. Tiap kota punya syarat: minimal sekian <b>⭐ poin</b> dan sejumlah <b>kartu bonus</b> warna tertentu, misalnya “⭐12 + 3 Zamrud + 3 Safir”. Ada juga syarat “4× 1 warna” (4 kartu dari satu warna apa pun) dan “1 tiap warna”.</li>
    <li><b>Tidak ada target 15 poin.</b> Di akhir giliranmu, kalau semua syarat sebuah kota terpenuhi, kamu otomatis <b>merebut kota itu</b>. Kalau beberapa terpenuhi sekaligus, kamu mendapat kota dengan syarat poin tertinggi. Tiap pemain hanya bisa punya satu kota, dan tiap kota hanya bisa direbut satu orang.</li>
    <li><b>Ronde terakhir.</b> Kota pertama yang direbut memicu ronde terakhir, sampai giliran kembali ke pemain pertama. Pemain lain masih bisa merebut kota yang tersisa.</li>
    <li><b>Pemenang.</b> Hanya pemain yang punya kota yang bisa menang. Kalau lebih dari satu, yang poinnya tertinggi menang; kalau seri, kartu lebih sedikit menang.</li>
  </ul>
  <p><b>Tips:</b> ketuk kartu kota untuk melihat syarat yang sudah dan belum kamu penuhi. Rencanakan warna kartu sejak awal, karena poin saja tidak cukup.</p>`;
}
