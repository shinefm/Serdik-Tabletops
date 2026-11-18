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
  const req=kotaReq(id,p||{cards:[],pat:[]});
  const ico=x=>x.t==='pts'?`<span class="kp">${x.n}</span>`:x.t==='c'?`<span class="kc c-${x.c}">${x.n}</span>`:x.t==='same'?`<span class="kc kany">${x.n}</span>`:'<span class="kc keach">1</span>';
  const txt=x=>x.t==='pts'?`<b>Minimal ${x.n} poin</b> (⭐ poin dari kartu yang sudah kamu beli).`
    :x.t==='c'?`<b>${x.n} kartu ${wn(x.c)}</b> yang sudah kamu beli.`
    :x.t==='same'?`<b>${x.n} kartu dari satu warna yang sama</b>, warnanya bebas. Contoh: ${x.n} kartu Merah, atau ${x.n} kartu Biru.`
    :`<b>Minimal 1 kartu dari tiap warna</b>: Putih, Biru, Hijau, Merah, dan Hitam.`;
  const have=x=>!p?'':x.t==='pts'?`kamu punya ${x.have} poin`:x.t==='each'?`kamu punya ${x.have} dari 5 warna`:x.t==='same'?`warna terbanyakmu ${x.have} kartu`:`kamu punya ${x.have}`;
  const rows=req.map(x=>`<div class="kirow ${p?(x.ok?'ok':'no'):''}"><div class="kiico">${ico(x)}</div><div class="kitx">${txt(x)}${p?`<div class="bd">${x.ok?'✅':'⬜'} ${have(x)}${x.ok?'':` · kurang ${x.t==='each'?(5-x.have)+' warna':Math.max(0,x.n-x.have)}`}</div>`:''}</div></div>`).join('');
  const done=p&&req.every(x=>x.ok);
  const status=own!=null?`🏁 Sudah direbut <b>${esc(nm(st,own))}</b>.`
    :p&&p.kota?`Kamu sudah punya Kota ${esc(KOTA[p.kota].name)}. Tiap pemain hanya bisa punya satu kota.`
    :done?'✅ <b>Semua syarat terpenuhi!</b> Kota ini direbut otomatis di akhir giliranmu.'
    :'Penuhi <b>semua</b> syarat di bawah. Kota direbut otomatis di akhir giliranmu.';
  openModal(`<div class="kinfoart">${kotaArt(id)}</div><h3>🏙️ Kota ${esc(K.name)}</h3>
    <p style="font-size:14px;margin:0 0 8px">${status}</p>
    <div class="kirows">${rows}</div>
    <details class="kileg"><summary>❓ Arti ikon di kartu kota</summary>
      <div class="kirow"><div class="kiico"><span class="kp">12</span></div><div class="kitx">Kotak emas = poin minimal.</div></div>
      <div class="kirow"><div class="kiico"><span class="kc c-r">3</span></div><div class="kitx">Kartu berwarna = jumlah kartu bonus warna itu (diskon permanen dari kartu yang sudah dibeli, bukan token permata).</div></div>
      <div class="kirow"><div class="kiico"><span class="kc kany">4</span></div><div class="kitx">Kartu abu-abu bergaris (tanpa warna) = sekian kartu dari <b>satu warna yang sama</b>, warnanya bebas.</div></div>
      <div class="kirow"><div class="kiico"><span class="kc keach">1</span></div><div class="kitx">Kartu pelangi = minimal 1 kartu dari <b>tiap</b> warna.</div></div>
      <div class="bd" style="margin-top:6px">Garis hijau di kartu kota = syarat yang sudah kamu penuhi. Kota pertama yang direbut memicu ronde terakhir, dan hanya pemilik kota yang bisa menang.</div>
    </details>
    <div class="mbtns"><button class="btn pri" data-act="close">Mengerti</button></div>`);
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
/* ---------- bot khusus Ekspansi Kota ----------
   Tiap giliran: hitung jarak ke tiap kota (kekurangan poin & warna, dibandingkan lawan),
   bidik 1 kota utama + 1 cadangan, nilai kartu menurut jalur itu, rebut kota bila bisa,
   dan hambat lawan yang tinggal satu kartu lagi. */
const P_KOTA={vp:1.0,vc:2.4,vc2:0.8,vb:1.1,vbDecay:0.13,tx:1.15,buyG:0.62,res9:8,two:0.45,scarce:0.35,ptsPer:2.4,comp:2.5,sec:0.35};
const P_KOTA_N=Object.assign({},P_KOTA,{vc:1.9,comp:0,sec:0,noDeny:1,tx:1.05});
function kotaDist(st,id,q){
  const K=KOTA[id], b=bonusOf(q), pts=ptsOf(q);
  let col=0; const need={};
  for(const c in K.need){const d=Math.max(0,K.need[c]-b[c]);if(d){need[c]=d;col+=d;}}
  if(K.same){const best=[...COLORS].sort((x,y)=>(b[y]+(K.need[y]?0:0))-(b[x]))[0];const d=Math.max(0,K.same-b[best]);if(d){need[best]=(need[best]||0)+d;col+=d;}}
  if(K.each)for(const c of COLORS)if(b[c]<1){need[c]=(need[c]||0)+1;col++;}
  const pd=Math.max(0,K.pts-pts);
  return {id,col,pd,need,E:col+Math.max(0,pd-col*1.3)/P_KOTA.ptsPer};
}
function kotaTargets(st,pi){
  const p=st.players[pi], free=st.cities.filter(id=>kotaOwner(st,id)==null);
  const opps=st.players.filter((q,i)=>i!==pi&&!q.kota);
  const list=free.map(id=>{const d=kotaDist(st,id,p);const oe=opps.length?Math.min(...opps.map(q=>kotaDist(st,id,q).E)):99;
    d.score=d.E+(oe<d.E-0.5?P_KOTA.comp*Math.min(1,(d.E-oe)/2):0);return d;}).sort((a,b)=>a.score-b.score);
  return list;
}
function kotaPlan(st,pi,P){
  const p=st.players[pi], b=bonusOf(p), ncards=p.cards.length, T=kotaTargets(st,pi);
  const main=T[0], sec=T[1];
  const want={w:0,u:0,g:0,r:0,k:0};
  if(main)for(const c in main.need)want[c]+=Math.min(1,main.need[c]/1.5)+0.25*main.need[c];
  if(sec)for(const c in sec.need)want[c]+=P.sec*Math.min(1,sec.need[c]/1.5);
  const pd=main?main.pd:0, col=main?main.col:0;
  const vpK=pd>0?1+Math.min(2,pd/Math.max(1,col*2+1)):0.3;
  const late=!!main&&(main.E<=2.5)||st.endTriggered;
  const cands=[];
  for(const t of [1,2,3])st.market['t'+t].forEach((id,slot)=>{if(id)cands.push({id,src:{tier:t,slot},res:false});});
  p.res.forEach((id,k)=>cands.push({id,src:{res:k},res:true}));
  for(const x of cands){const c=CARDS[x.id];const d={};let sum=0,mx=0,short=0;
    for(const cl of COLORS){const nd=Math.max(0,(c.cost[cl]||0)-b[cl]-p.t[cl]);d[cl]=nd;sum+=nd;mx=Math.max(mx,nd);if(nd>st.bank[cl])short+=nd-st.bank[cl];}
    const eff=Math.max(0,sum-p.t.y), gold=p.t.y;
    const Tn=eff===0?0:Math.max(Math.ceil(eff/3),Math.ceil(Math.max(0,mx-gold)/2))+(short>gold?Math.ceil(short-gold):0);
    const colorV=want[c.b]>0?P.vc*Math.min(1.4,want[c.b]):0;
    const engine=late?0:Math.max(0,P.vb-P.vbDecay*ncards)*(colorV>0?1:0.6);
    let val=c.pts*P.vp*vpK+colorV+engine;
    if(pd===0&&col===0)val=c.pts*0.5+0.1;
    x.d=d;x.T=Tn;x.val=val;x.sc=val/Math.pow(Tn+1,P.tx);x.afford=!!payFor(p,c);}
  return {p,cands,late,want,main};
}
function kotaThreats(st,pi){
  /* kartu pasar yang bisa dibeli seorang lawan sekarang dan langsung membuatnya merebut kota */
  const free=st.cities.filter(id=>kotaOwner(st,id)==null), out=[];
  st.players.forEach((q,qi)=>{if(qi===pi||q.kota)return;
    for(const t of [1,2,3])st.market['t'+t].forEach((id,slot)=>{if(!id)return;const c=CARDS[id];if(!payFor(q,c))return;
      const q2={...q,cards:[...q.cards,id]};if(free.some(cid=>kotaOk(cid,q2)))out.push({tier:t,slot,qi});});});
  return out;
}
function kotaThreat(st,pi){
  /* hanya layak dihambat kalau tiap lawan yang terancam cuma punya satu jalan lewat pasar */
  const th=kotaThreats(st,pi); if(!th.length)return null;
  const by={};th.forEach(x=>{(by[x.qi]=by[x.qi]||[]).push(x);});
  const n=st.players.length; let best=null;
  for(const qi in by){if(by[qi].length!==1)continue;const d=((+qi)-pi+n)%n;if(!best||d<best.d)best={...by[qi][0],d};}
  return best;
}
function kotaMove(st,pi,P){
  P=P||P_KOTA; const p=st.players[pi], n=st.players.length;
  // 1) langkah yang langsung merebut kota (pilih yang memberi poin terbanyak)
  if(!p.kota){let win=null;
    for(const r of legalMoves(st,pi)){const q=r.s.players[pi];if(q.kota){const v=ptsOf(q)+(r.mv.type==='buy'?0.5:0);if(!win||v>win.v)win={mv:r.mv,v};}}
    if(win)return win.mv;}
  const {cands,late,want,main}=kotaPlan(st,pi,P); const opts=[];
  // 2) hambat lawan yang tinggal satu kartu lagi
  const th=P.noDeny?null:kotaThreat(st,pi);
  if(th){const c=CARDS[st.market['t'+th.tier][th.slot]];if(payFor(p,c))opts.push({type:'buy',tier:th.tier,slot:th.slot});else if(p.res.length<MAXRES)opts.push({type:'reserve',tier:th.tier,slot:th.slot});}
  const buys=cands.filter(x=>x.afford);
  const ranked=[...cands].sort((a,c)=>c.sc-a.sc), target=ranked[0];
  if(buys.length){buys.sort((a,c)=>c.val-a.val);const bb=buys[0];if(!target||target.afford||bb.val>=P.buyG*target.sc*(target.T+1)||(late&&bb.val>0.6))opts.push({type:'buy',...bb.src});}
  const tgt=ranked.filter(x=>!x.afford).slice(0,3), tw={w:0,u:0,g:0,r:0,k:0};
  tgt.forEach((x,i)=>{const wgt=i===0?1:(i===1?0.45:0.2);for(const c of COLORS)tw[c]+=Math.min(x.d[c],st.bank[c])*wgt*x.sc;});
  const avail=COLORS.filter(c=>st.bank[c]>0), tok=tokTotal(p);
  if(target&&!target.afford&&target.src.tier&&p.res.length<MAXRES&&st.bank.y>0){const short=COLORS.some(c=>target.d[c]>st.bank[c]);if(short||tok>=P.res9)opts.push({type:'reserve',...target.src});}
  if(avail.length){
    const wv=c=>tw[c]+(st.bank[c]<=2?P.scarce*tw[c]:0)+0.05*(want[c]||0);
    const order=[...avail].sort((a,c)=>wv(c)-wv(a)), top=order[0];
    if(target&&target.d[top]>=2&&st.bank[top]>=4&&(order.filter(c=>tw[c]>0).length<=1||tw[top]*P.two>(tw[order[1]]||0)+(tw[order[2]]||0)))opts.push({type:'take',picks:{[top]:2}});
    const pk={};order.slice(0,3).forEach(c=>pk[c]=1);opts.push({type:'take',picks:pk});
    if(order.length<3)COLORS.forEach(c=>{if(st.bank[c]>=4)opts.push({type:'take',picks:{[c]:2}});});
  }
  if(target&&p.res.length<MAXRES&&target.src.tier)opts.push({type:'reserve',...target.src});
  if(buys.length)opts.push({type:'buy',...buys[0].src});
  for(const t of [3,2,1])if(p.res.length<MAXRES&&st.decks['t'+t].length){opts.push({type:'reserve',deck:t});break;}
  opts.push({type:'pass'});
  const keep=c=>(target?(target.d[c]||0)*10:0)+(tw[c]||0)+(c==='y'?100:0);
  for(const mv of opts){
    try{doMove(clone(st),pi,mv);return mv;}
    catch(e){if(e.code==='DISCARD'){const t={...e.extra.t},dis={};let over=e.extra.over;
        while(over>0){const c=ALL.filter(x=>t[x]>0).sort((a,z)=>(keep(a)-t[a]*0.5)-(keep(z)-t[z]*0.5))[0];t[c]--;dis[c]=(dis[c]||0)+1;over--;}
        const m2={...mv,discard:dis};try{doMove(clone(st),pi,m2);return m2;}catch(_){}}}
  }
  return {type:'pass'};
}

/* ---------- bot Kota v2: cari langkah terbaik lewat penilaian keadaan ---------- */
const P_KV={gam:0.784,wB:1.609,wBd:0.05,wPts:0.353,wE:3.2,wE2:0.921,tx:1.343,tok:0.067,gold:0.1,resPen:0.613,comp:3.122,ptsPer:2.705,depth:3,beam:5,beam2:4,d2:0.92,deny:40};
const P_KV_N=Object.assign({},P_KV,{depth:2,beam:4,noise:1.6,noDeny:1});
function kvDist(id,q,P){
  const K=KOTA[id], b=bonusOf(q), pts=ptsOf(q);let col=0;const need={};
  for(const c in K.need){const d=Math.max(0,K.need[c]-b[c]);if(d){need[c]=d;col+=d;}}
  if(K.same){let best=COLORS[0];for(const c of COLORS)if(b[c]>b[best])best=c;const d=Math.max(0,K.same-b[best]);if(d){need[best]=(need[best]||0)+d;col+=d;}}
  if(K.each)for(const c of COLORS)if(b[c]<1){need[c]=(need[c]||0)+1;col++;}
  const pd=Math.max(0,K.pts-pts);
  return {id,col,pd,need,E:col+Math.max(0,pd-col*1.2)/P.ptsPer};
}
function kvTargets(s,pi,P){
  const p=s.players[pi], free=s.cities.filter(id=>kotaOwner(s,id)==null), opps=s.players.filter((q,i)=>i!==pi&&!q.kota);
  return free.map(id=>{const d=kvDist(id,p,P);const oe=opps.length?Math.min(...opps.map(q=>kvDist(id,q,P).E)):99;d.score=d.E+(oe<d.E-0.5?P.comp*Math.min(1,(d.E-oe)/2):0);return d;}).sort((a,b)=>a.score-b.score);
}
function kvReal(p,main,sec,P){
  /* nilai nyata keadaan pemain: mesin diskon + poin + kemajuan ke kota utama/cadangan */
  const n=p.cards.length, eng=n*Math.max(0.2,P.wB-P.wBd*n);
  const m=kvDist(main.id,p,P), s2=sec?kvDist(sec.id,p,P):null;
  return eng+P.wPts*ptsOf(p)-P.wE*m.E-(s2?P.wE2*s2.E:0);
}
function kvEval(s,pi,P,tg){
  const p=s.players[pi];
  if(p.kota)return 1000+ptsOf(p);
  const T=tg||kvTargets(s,pi,P); if(!T.length)return ptsOf(p);
  const main=T[0], sec=T[1]||null, b=bonusOf(p), base=kvReal(p,main,sec,P);
  const gains=[];
  const look=(id,res)=>{const c=CARDS[id];let sum=0,mx=0;for(const cl of COLORS){const d=Math.max(0,(c.cost[cl]||0)-b[cl]-p.t[cl]);sum+=d;mx=Math.max(mx,d);}
    const eff=Math.max(0,sum-p.t.y);const Tn=eff===0?0:Math.max(Math.ceil(eff/3),Math.ceil(Math.max(0,mx-p.t.y)/2));
    const g=kvReal({...p,cards:[...p.cards,id]},main,sec,P)-base; if(g<=0)return;
    gains.push(g*P.gam/Math.pow(Tn+1,P.tx));};
  for(const t of [1,2,3])s.market['t'+t].forEach(id=>{if(id)look(id);});p.res.forEach(id=>look(id,1));
  gains.sort((a,b)=>b-a);const pot=(gains[0]||0)+0.4*(gains[1]||0)+0.2*(gains[2]||0);
  return base+pot+P.tok*tokTotal(p)+P.gold*p.t.y-P.resPen*(p.res.length>=MAXRES?1:0);
}
function kvMoves(st,pi,P){
  const out=[],seen=new Set(),p0=st.players[pi];
  const tg=kvTargets(st,pi,P), main=tg[0];
  const keepScore=c=>c==='y'?99:((main&&main.need[c])?3:0);
  const add=(mv,s2)=>{const k=JSON.stringify(mv);if(seen.has(k))return;seen.add(k);out.push({mv,s:s2});};
  for(const r of legalMoves(st,pi)){
    if(r.mv.type==='take'&&r.mv.discard){
      // buang ulang dengan prioritas rencana
      const s1=clone(st);let over=0;try{doMove(s1,pi,{type:'take',picks:r.mv.picks});add(r.mv.picks&&{type:'take',picks:r.mv.picks},s1);continue;}catch(e){if(e.code!=='DISCARD')continue;over=e.extra.over;var t=e.extra.t;}
      const tt={...t},dis={};while(over>0){const c=ALL.filter(x=>tt[x]>0).sort((a,z)=>(keepScore(a)*2-tt[a])-(keepScore(z)*2-tt[z]))[0];tt[c]--;dis[c]=(dis[c]||0)+1;over--;}
      const m2={...r.mv,discard:dis};const s2=clone(st);try{doMove(s2,pi,m2);
        const same=ALL.every(c=>s2.players[pi].t[c]===p0.t[c]);if(!same)add(m2,s2);}catch(_){}
      const sameA=ALL.every(c=>r.s.players[pi].t[c]===p0.t[c]);if(!sameA)add(r.mv,r.s);
    }else add(r.mv,r.s);
  }
  return out;
}
function kotaMove2(st,pi,P){
  P=P||P_KV; const p=st.players[pi];
  const ms=kvMoves(st,pi,P);
  if(!ms.length)return {type:'pass'};
  if(!p.kota){let win=null;for(const r of ms){const q=r.s.players[pi];if(q.kota){const v=ptsOf(q);if(!win||v>win.v)win={mv:r.mv,v};}}if(win)return win.mv;}
  const th=P.noDeny?null:kotaThreat(st,pi);
  let best=null;
  for(const r of ms){let v=kvEval(r.s,pi,P);
    if(th&&((r.mv.type==='buy'||r.mv.type==='reserve')&&r.mv.tier===th.tier&&r.mv.slot===th.slot))v+=P.deny||6;
    if(r.mv.type==='pass')v-=5;
    if(P.noise)v+=(Math.random()-0.5)*P.noise;
    if(!best||v>best.v)best={mv:r.mv,v};}
  return best.mv;
}

function kotaMove3(st,pi,P){
  /* pandangan dua langkah milik sendiri (lawan dianggap diam), beam dari penilaian satu langkah */
  P=P||P_KV; const p=st.players[pi];
  const ms=kvMoves(st,pi,P); if(!ms.length)return {type:'pass'};
  if(!p.kota){let win=null;for(const r of ms){const q=r.s.players[pi];if(q.kota){const v=ptsOf(q);if(!win||v>win.v)win={mv:r.mv,v};}}if(win)return win.mv;}
  const th=P.noDeny?null:kotaThreat(st,pi);
  const sc=ms.map(r=>{let v=kvEval(r.s,pi,P);if(r.mv.type==='pass')v-=5;if(th&&(r.mv.type==='buy'||r.mv.type==='reserve')&&r.mv.tier===th.tier&&r.mv.slot===th.slot)v+=P.deny||6;return {r,v};}).sort((a,b)=>b.v-a.v);
  if((P.depth||1)<2)return sc[0].r.mv;
  let best=null;
  for(const x of sc.slice(0,P.beam||6)){
    const s1=clone(x.r.s); s1.turn=pi; s1.status='playing';
    let b2=x.v;
    if(!s1.players[pi].kota){for(const r2 of kvMoves(s1,pi,P)){const v2=(r2.s.players[pi].kota?1000:kvEval(r2.s,pi,P))*P.d2+(1-P.d2)*x.v;if(v2>b2)b2=v2;}}
    const tot=b2+(x.v-sc[0].v)*0.15+(P.noise?(Math.random()-0.5)*P.noise:0);
    if(!best||tot>best.tot)best={mv:x.r.mv,tot};
  }
  return best.mv;
}

function kvSearch(s,pi,P,d){
  /* nilai terbaik yang bisa dicapai dalam d langkah milik sendiri */
  const ms=kvMoves(s,pi,P); if(!ms.length)return kvEval(s,pi,P);
  const sc=ms.map(r=>({r,v:r.s.players[pi].kota?1000+ptsOf(r.s.players[pi]):kvEval(r.s,pi,P)-(r.mv.type==='pass'?5:0)})).sort((a,b)=>b.v-a.v);
  if(d<=1||sc[0].v>=1000)return sc[0].v;
  let best=sc[0].v;
  for(const x of sc.slice(0,P.beam2||4)){const s1=clone(x.r.s);s1.turn=pi;s1.status='playing';const v=kvSearch(s1,pi,P,d-1)*P.d2+(1-P.d2)*x.v;if(v>best)best=v;}
  return best;
}
function kotaMoveD(st,pi,P){
  P=P||P_KV; const p=st.players[pi];
  const ms=kvMoves(st,pi,P); if(!ms.length)return {type:'pass'};
  if(!p.kota){let win=null;for(const r of ms){const q=r.s.players[pi];if(q.kota){const v=ptsOf(q);if(!win||v>win.v)win={mv:r.mv,v};}}if(win)return win.mv;}
  const th=P.noDeny?null:kotaThreat(st,pi);
  const sc=ms.map(r=>{let v=kvEval(r.s,pi,P);if(r.mv.type==='pass')v-=5;if(th&&(r.mv.type==='buy'||r.mv.type==='reserve')&&r.mv.tier===th.tier&&r.mv.slot===th.slot)v+=P.deny||6;return {r,v};}).sort((a,b)=>b.v-a.v);
  const D=P.depth||1; if(D<2)return sc[0].r.mv;
  let best=null;
  for(const x of sc.slice(0,P.beam||6)){const s1=clone(x.r.s);s1.turn=pi;s1.status='playing';
    const v=(s1.players[pi].kota?1000:kvSearch(s1,pi,P,D-1))*P.d2+(1-P.d2)*x.v+(P.noise?(Math.random()-0.5)*P.noise:0);
    if(!best||v>best.v)best={mv:x.r.mv,v};}
  return best.mv;
}
