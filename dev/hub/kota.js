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
/* ---------- ilustrasi kota (gaya kartu retro: 5 nada warna, siluet datar) ---------- */
const KPAL={jkt:'k',sby:'u',plg:'r',smg:'w',bdg:'g',mdn:'x',mks:'r',bpn:'k',yog:'w',dps:'g'};
function kCandi(x,s,f){let o='',y=62,w=18*s;for(let i=0;i<4;i++){const h=(i<3?8.5:8)*s,nw=w*0.72;o+=`<path d="M${x-w/2} ${y}h${w}l${-(w-nw)/2} ${-h}h${-nw}z" fill="${f}"/>`;y-=h;w=nw;}return o+`<path d="M${x-w/2} ${y}h${w}L${x} ${y-10*s}z" fill="${f}"/>`;}
const KART={
 jkt:p=>`<rect width="100" height="70" fill="${p.e}"/><circle cx="80" cy="15" r="7" fill="${CR}"/><circle cx="14" cy="11" r="1" fill="${p.a}"/><circle cx="30" cy="20" r=".8" fill="${p.a}"/><circle cx="64" cy="8" r=".9" fill="${p.a}"/><circle cx="92" cy="30" r=".8" fill="${p.a}"/><path d="M0 70V40h10V30h8v12h6V26h10v44Z" fill="${p.d}"/><path d="M66 70V30h10v8h8V22h9v14h7v34Z" fill="${p.d}"/><path d="M3 44h2v2H3zM13 34h2v2h-2zM28 30h2v2h-2zM28 40h2v2h-2zM70 34h2v2h-2zM87 26h2v2h-2zM87 40h2v2h-2zM79 44h2v2h-2z" fill="#f0c55e"/><path d="M47.6 22h4.8l1.6 32h-8z" fill="${p.a}"/><path d="M47 21h6v2h-6z" fill="${p.c}"/><path d="M50 8q4 5 2.6 9q-1 3-2.6 4q-1.6-1-2.6-4q-1.4-4 2.6-9z" fill="#f0c55e"/><path d="M36 54h28l-4 6H40z" fill="${p.c}"/><path d="M30 60h40v4H30z" fill="${p.b}"/><path d="M0 64h100v6H0z" fill="${p.c}"/>`,
 sby:p=>`<rect width="100" height="70" fill="${p.a}"/><circle cx="18" cy="17" r="9" fill="${CR}"/><path d="M0 52h100v18H0z" fill="${p.c}"/><path d="M6 60q6-2 12 0M40 65q6-2 12 0M74 59q6-2 12 0" stroke="${p.b}" stroke-width="1.5" fill="none"/><path d="M37.5 16L8 44M37.5 16L18 44M37.5 16L27 44M37.5 16L47 44M64.5 16L53 44M64.5 16L73 44M64.5 16L82 44M64.5 16L92 44" stroke="${p.d}" stroke-width=".8"/><path d="M34 14h3v38h-3zM38 14h3v38h-3zM61 14h3v38h-3zM65 14h3v38h-3z" fill="${p.e}"/><path d="M34 22h7v2h-7zM61 22h7v2h-7z" fill="${p.e}"/><path d="M0 44h100v3H0z" fill="${p.d}"/><path d="M14 47h3v6h-3zM48 47h4v6h-4zM84 47h3v6h-3z" fill="${p.d}"/>`,
 plg:p=>`<rect width="100" height="70" fill="${p.a}"/><circle cx="80" cy="15" r="8" fill="${CR}"/><path d="M0 50h100v20H0z" fill="${p.b}"/><path d="M6 58q6-2 12 0M44 63q6-2 12 0M80 57q6-2 12 0" stroke="${p.a}" stroke-width="1.5" fill="none"/><path d="M38 19L50 40M62 19L50 40M38 26L45 40M62 26L55 40" stroke="${p.d}" stroke-width="1.3"/><path d="M28 12h10v38H28zM62 12h10v38H62z" fill="${p.d}"/><path d="M26 12l7-7l7 7zM60 12l7-7l7 7z" fill="${p.e}"/><path d="M31 17h4v10h-4zM65 17h4v10h-4z" fill="${p.b}"/><path d="M38 16h24v3H38z" fill="${p.d}"/><path d="M0 40h100v4H0z" fill="${p.e}"/><path d="M8 54h14l-3 4h-8zM78 60h14l-3 4h-8z" fill="${p.e}"/><path d="M11 54v-4h8v4z" fill="${p.d}"/>`,
 smg:p=>{let w='';for(const x of [37,43,51,57])for(const y of [38,50])w+=`<path d="M${x} ${y+8}v-5q2-3 4 0v5z" fill="${p.e}"/>`;for(const x of [12,16,80,84])w+=`<path d="M${x} 58v-5q1.5-2.5 3 0v5z" fill="${p.e}"/>`;
  return `<rect width="100" height="70" fill="${p.a}"/><circle cx="84" cy="14" r="7" fill="#f0c55e"/><path d="M8 34h84v28H8z" fill="${p.b}"/><path d="M6 30h88l-2 4H8z" fill="${p.d}"/><path d="M22 18h11v44H22zM67 18h11v44H67z" fill="${p.c}"/><path d="M21 18q6.5-11 13 0zM66 18q6.5-11 13 0z" fill="${p.e}"/><path d="M27.5 8V4M72.5 8V4" stroke="${p.e}" stroke-width="1.2"/><path d="M24 24h7v6h-7zM69 24h7v6h-7z" fill="${p.e}"/>${w}<path d="M0 62h100v8H0z" fill="${p.d}"/><path d="M4 62q0-8 5-9q5 1 5 9zM88 62q0-8 5-9q5 1 5 9z" fill="${p.c}"/>`;},
 bdg:p=>`<rect width="100" height="70" fill="${p.a}"/><circle cx="16" cy="15" r="7" fill="${CR}"/><path d="M0 42L20 26h30L78 38L100 30V70H0z" fill="${p.b}"/><path d="M10 46h80v16H10z" fill="${CR}"/><path d="M8 46l6-5h72l6 5z" fill="${p.e}"/><path d="M42 30h16v32H42z" fill="${CR}"/><path d="M40 30l4-6h12l4 6z" fill="${p.e}"/><path d="M45 24l2-5h6l2 5z" fill="${p.d}"/><path d="M50 19V5" stroke="${p.e}" stroke-width="1"/><circle cx="50" cy="8" r="1.2" fill="${p.e}"/><circle cx="50" cy="10.6" r="1.2" fill="${p.e}"/><circle cx="50" cy="13.2" r="1.2" fill="${p.e}"/><circle cx="50" cy="15.8" r="1.2" fill="${p.e}"/><path d="M14 50h4v6h-4zM22 50h4v6h-4zM30 50h4v6h-4zM66 50h4v6h-4zM74 50h4v6h-4zM82 50h4v6h-4zM47 35h6v8h-6z" fill="${p.d}"/><path d="M46 52h8v10h-8z" fill="${p.d}"/><path d="M0 62h100v8H0z" fill="${p.c}"/>`,
 mdn:p=>{let a='';for(const x of [13,22,31,63,72,81])a+=`<path d="M${x} 62v-9q3-4 6 0v9z" fill="${p.e}"/>`;
  return `<rect width="100" height="70" fill="${p.a}"/><path d="M8 16q4-4 9-2q4-4 9 0q3 2 0 4H8q-3-1 0-2zM70 10q4-4 9-2q4-4 9 0q3 2 0 4H70q-3-1 0-2z" fill="${p.b}"/><path d="M8 42h84v20H8z" fill="${p.c}"/><path d="M6 40h88v3H6z" fill="${p.e}"/><path d="M38 40q0-14 12-18q12 4 12 18z" fill="${p.d}"/><path d="M50 22v-6" stroke="${p.e}" stroke-width="1.2"/><circle cx="50" cy="15" r="1.5" fill="${p.c}"/><path d="M13 40q0-8 7-11q7 3 7 11zM73 40q0-8 7-11q7 3 7 11z" fill="${p.d}"/><path d="M20 29v-4M80 29v-4" stroke="${p.e}" stroke-width="1"/>${a}<path d="M45 62V50q5-6 10 0v12z" fill="${p.e}"/><path d="M0 62h100v8H0z" fill="${p.d}"/>`;},
 mks:p=>`<rect width="100" height="70" fill="${p.a}"/><circle cx="70" cy="36" r="16" fill="${p.b}"/><path d="M0 50h100v20H0z" fill="${p.c}"/><path d="M4 58q6-2 12 0M40 64q6-2 12 0M80 57q6-2 12 0" stroke="${p.b}" stroke-width="1.5" fill="none"/><path d="M36 50V12M56 50V16" stroke="${p.e}" stroke-width="1.6"/><path d="M37.5 14l14 6v24H37.5zM57.5 18l12 6v20H57.5zM34.5 16L21 46h13.5z" fill="${CR}"/><path d="M16 50h60l-9 8H26z" fill="${p.e}"/><path d="M76 50l12-7" stroke="${p.e}" stroke-width="1.5"/><path d="M20 50h52" stroke="${p.d}" stroke-width="1.5"/><path d="M12 24q2-2 4 0q2-2 4 0M84 16q2-2 4 0q2-2 4 0" stroke="${p.e}" stroke-width="1" fill="none"/>`,
 bpn:p=>`<rect width="100" height="70" fill="${p.a}"/><circle cx="82" cy="14" r="7" fill="${CR}"/><path d="M20 14h6v42h-6zM30 22h5v34h-5z" fill="${p.d}"/><path d="M20 22h6M20 30h6M20 38h6M20 46h6M30 30h5M30 40h5" stroke="${p.b}" stroke-width="1"/><path d="M44 10h3v46h-3z" fill="${p.e}"/><path d="M45.5 1q4.5 4.5 2 9h-4q-2.5-4.5 2-9z" fill="#f08a3c"/><path d="M45.5 4q2 2.5 .8 6h-1.6q-1.2-3.5 .8-6z" fill="#ffe14d"/><path d="M26 46h30M35 50h21" stroke="${p.e}" stroke-width="1.4"/><path d="M56 40h18v16H56zM76 44h16v12H76z" fill="${p.c}"/><ellipse cx="65" cy="40" rx="9" ry="2.5" fill="${p.b}"/><ellipse cx="84" cy="44" rx="8" ry="2.2" fill="${p.b}"/><path d="M0 56h100v14H0z" fill="${p.e}"/><path d="M0 62h100v8H0z" fill="${p.c}"/><path d="M8 66q6-2 12 0M60 66q6-2 12 0" stroke="${p.b}" stroke-width="1.3" fill="none"/>`,
 yog:p=>`<rect width="100" height="70" fill="${p.a}"/><path d="M0 50L28 20h9L70 50z" fill="${p.b}"/><path d="M31 18q-3-6 2-9q4-4 9 0q5-3 8 1" stroke="${p.c}" stroke-width="2.2" fill="none" stroke-linecap="round"/>${kCandi(40,.62,p.c)}${kCandi(82,.62,p.c)}${kCandi(61,1,p.d)}<path d="M0 62h100v8H0z" fill="${p.c}"/><path d="M8 62q0-7 4-8q4 1 4 8z" fill="${p.d}"/>`,
 dps:p=>{let m='';for(let i=0;i<5;i++){const w=16-2.6*i,y=46-5*i;m+=`<path d="M${50-w/2} ${y}h${w}l-2.2 -3.4h${-(w-4.4)}z" fill="${p.e}"/>`;}
  return `<rect width="100" height="70" fill="${p.a}"/><circle cx="80" cy="15" r="8" fill="${CR}"/><path d="M48.8 46h2.4V62h-2.4z" fill="${p.e}"/>${m}<path d="M20 62V42H24V34H28V26H33V18H38V12H44V62Z" fill="${p.d}"/><path d="M80 62V42H76V34H72V26H67V18H62V12H56V62Z" fill="${p.d}"/><path d="M24 42h20M28 34h16M76 42H56M72 34H56" stroke="${p.b}" stroke-width="1"/><path d="M42 62h16v-3H42z" fill="${p.c}"/><path d="M10 62q2-14-1-26" stroke="${p.e}" stroke-width="1.8" fill="none"/><path d="M9 36q-7-1-10 4M9 36q6-3 11 1M9 36q-3-6-8-6M9 36q4-6 9-5" stroke="${p.d}" stroke-width="2.4" fill="none" stroke-linecap="round"/><path d="M0 62h100v8H0z" fill="${p.c}"/>`;}
};
const KSVG={};
function kotaArt(id){return KSVG[id]||(KSVG[id]=`<svg viewBox="0 0 100 70" preserveAspectRatio="xMidYMid slice">${KART[id](RPAL[KPAL[id]])}</svg>`);}
/* ---------- tampilan ---------- */
function kotaTile(st,id,p){
  const K=KOTA[id], own=kotaOwner(st,id), req=p?kotaReq(id,p):null;
  const mark=i=>req?(req[i].ok?' ok':' no'):'';
  let k=1;
  const reqs=[];
  for(const c in K.need)reqs.push(`<span class="kc c-${c}${mark(k++)}" title="${K.need[c]} kartu ${CNAME[c]}">${K.need[c]}</span>`);
  if(K.same)reqs.push(`<span class="kc kany${mark(k++)}" title="${K.same} kartu dari satu warna apa pun">${K.same}</span>`);
  if(K.each)reqs.push(`<span class="kc keach${mark(k++)}" title="Minimal 1 kartu dari tiap warna">1</span>`);
  const ready=req&&own==null&&!p.kota&&req.every(x=>x.ok);
  return `<div class="kota kt-${KPAL[id]} ${own!=null?'taken':''} ${ready?'ready':''}" data-act="kotainfo" data-id="${id}">
    <div class="kart">${kotaArt(id)}<div class="kn">${esc(K.name)}</div>${own!=null?`<div class="kstamp">🏁 ${esc(nm(st,own))}</div>`:ready?'<div class="kstamp ok">✅ Siap</div>':''}</div>
    <div class="kside ${reqs.length>=3?'many':''}"><span class="kp${mark(0)}" title="Minimal ${K.pts} poin">${K.pts}</span>${reqs.length?'<span class="kplus">+</span>'+reqs.join(''):''}</div></div>`;
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
  openModal(`<div class="kinfoart">${kotaArt(id)}</div><h3>🏙️ Kota ${esc(K.name)}</h3>
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
