/* ---------- PEMUKIM NUSANTARA (aturan dasar Catan, 3–4 pemain) ---------- */
const PM_RES=['L','B','W','G','O'];
const PM_RN={L:'Kayu',B:'Bata',W:'Ternak',G:'Padi',O:'Bijih'};
const PM_RI={L:'🪵',B:'🧱',W:'🐐',G:'🌾',O:'⛏️'};
const PM_TER={L:'Hutan',B:'Bukit',W:'Padang',G:'Sawah',O:'Gunung',D:'Tanah tandus'};
const PM_COST={road:{L:1,B:1},settle:{L:1,B:1,W:1,G:1},city:{G:2,O:3},dev:{W:1,G:1,O:1}};
const PM_DEVN={K:'Ksatria',V:'Poin Kemenangan',R:'Bangun Jalan',Y:'Panen Raya',M:'Monopoli'};
const PM_DEVI={K:'⚔️',V:'🏆',R:'🛤️',Y:'🎁',M:'💰'};
const PM_PIPS={2:1,3:2,4:3,5:4,6:5,8:5,9:4,10:3,11:2,12:1};
/* geometri papan standar: 19 heks (radius 2), 54 titik, 72 sisi */
const PM_G=(()=>{
  const hexes=[];for(let q=-2;q<=2;q++)for(let r=-2;r<=2;r++)if(Math.abs(q+r)<=2)hexes.push([q,r]);
  hexes.sort((a,b)=>a[1]-b[1]||a[0]-b[0]);
  const S3=Math.sqrt(3), vk={}, verts=[], hv=[], edges=[], ek={};
  const center=([q,r])=>[S3*(q+r/2),1.5*r];
  hexes.forEach((h,hi)=>{const [cx,cy]=center(h), vs=[];
    for(let k=0;k<6;k++){const a=Math.PI/180*(60*k-90), x=+(cx+Math.cos(a)).toFixed(3), y=+(cy+Math.sin(a)).toFixed(3), key=x+','+y;
      if(vk[key]==null){vk[key]=verts.length;verts.push({x,y,h:[],e:[],n:[]});} vs.push(vk[key]); verts[vk[key]].h.push(hi);}
    hv.push(vs);
    for(let k=0;k<6;k++){const a=vs[k],b=vs[(k+1)%6],key=Math.min(a,b)+'-'+Math.max(a,b);
      if(ek[key]==null){ek[key]=edges.length;edges.push({a:Math.min(a,b),b:Math.max(a,b),h:[]});verts[a].e.push(ek[key]);verts[b].e.push(ek[key]);verts[a].n.push(b);verts[b].n.push(a);}
      edges[ek[key]].h.push(hi);}
  });
  const hn=hexes.map((h,i)=>hexes.map((g,j)=>j!==i&&Math.max(Math.abs(h[0]-g[0]),Math.abs(h[1]-g[1]),Math.abs(h[0]+h[1]-g[0]-g[1]))===1?j:-1).filter(j=>j>=0));
  const coast=edges.map((e,i)=>e.h.length===1?i:-1).filter(i=>i>=0).sort((i,j)=>{const m=e=>{const A=verts[edges[e].a],B=verts[edges[e].b];return Math.atan2((A.y+B.y)/2,(A.x+B.x)/2);};return m(i)-m(j);});
  return {hexes,center:hexes.map(center),verts,hv,edges,hn,coast};
})();
function pmNewBoard(){
  const G=PM_G;
  for(let tries=0;tries<500;tries++){
    const t=shuffle(['L','L','L','L','B','B','B','W','W','W','W','G','G','G','G','O','O','O','D']);
    const nums=shuffle([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]);
    const hex=t.map(x=>({t:x,n:x==='D'?0:nums.pop()}));
    const hot=hex.map((h,i)=>h.n===6||h.n===8?i:-1).filter(i=>i>=0);
    if(hot.some(i=>G.hn[i].some(j=>hot.includes(j))))continue;
    const pt=shuffle(['any','any','any','any','L','B','W','G','O']), off=Math.floor(Math.random()*3);
    const ports=[0,3,7,10,13,17,20,23,27].map((k,j)=>({e:G.coast[(k+off)%G.coast.length],t:pt[j]}));
    return {hex,robber:t.indexOf('D'),ports};
  }
  return pmNewBoard();
}
function pmTotal(r){return PM_RES.reduce((s,k)=>s+(r[k]||0),0);}
function pmHas(r,c){return Object.keys(c).every(k=>(r[k]||0)>=c[k]);}
function pmPay(st,p,c){Object.keys(c).forEach(k=>{p.res[k]-=c[k];st.bank[k]+=c[k];});}
function pmStart(st){
  const n=st.players.length; if(n<3||n>4)fail('Pemukim Nusantara untuk 3–4 pemain');
  st.board=pmNewBoard(); st.vtx=Array(54).fill(null); st.edge=Array(72).fill(null);
  st.bank={L:19,B:19,W:19,G:19,O:19};
  st.devDeck=shuffle([...'KKKKKKKKKKKKKK','V','V','V','V','V','R','R','Y','Y','M','M']);
  st.players.forEach(p=>{p.res={L:0,B:0,W:0,G:0,O:0};p.dev=[];p.devNew=[];p.knights=0;p.vpDev=0;});
  st.turn=0; st.round=1; st.phase='setup'; st.setup={i:0,need:'S',v:null}; st.dice=null;
  st.devPlayed=false; st.largest=null; st.longest=null; st.lens=Array(n).fill(0); st.offer=null; st.free=0; st.rret=null;
  st.status='playing'; st.turnAt=Date.now();
  st.log=[{p:-1,m:'🏝️ Pulau baru terbentuk. Tiap pemain menaruh 2 pemukiman dan 2 jalan (urutan maju, lalu mundur).'}];
}
function pmSetupOrder(n){const a=[...Array(n).keys()];return [...a,...a.slice().reverse()];}
function pmVP(st,i,all){const p=st.players[i];let v=0;
  st.vtx.forEach(x=>{if(x&&x.p===i)v+=x.c?2:1;});
  if(st.largest===i)v+=2; if(st.longest===i)v+=2; if(all)v+=p.dev.concat(p.devNew).filter(c=>c==='V').length; return v;}
function pmCanSettleAt(st,v){if(st.vtx[v])return false;return !PM_G.verts[v].n.some(u=>st.vtx[u]);}
function pmSettleSpots(st,i,setup){return PM_G.verts.map((V,v)=>v).filter(v=>pmCanSettleAt(st,v)&&(setup||PM_G.verts[v].e.some(e=>st.edge[e]===i)));}
function pmRoadOk(st,i,e,fromV){
  if(st.edge[e]!=null)return false; const E=PM_G.edges[e];
  if(fromV!=null)return E.a===fromV||E.b===fromV;
  return [E.a,E.b].some(v=>{const b=st.vtx[v];if(b&&b.p===i)return true;if(b&&b.p!==i)return false;return PM_G.verts[v].e.some(f=>f!==e&&st.edge[f]===i);});
}
function pmRoadSpots(st,i){return PM_G.edges.map((E,e)=>e).filter(e=>pmRoadOk(st,i,e));}
function pmCitySpots(st,i){return st.vtx.map((x,v)=>x&&x.p===i&&!x.c?v:-1).filter(v=>v>=0);}
function pmPieces(st,i){let s=0,c=0;st.vtx.forEach(x=>{if(x&&x.p===i){if(x.c)c++;else s++;}});return {s,c,r:st.edge.filter(x=>x===i).length};}
function pmRate(st,i,r){let best=4;st.board.ports.forEach(pt=>{const E=PM_G.edges[pt.e];if([E.a,E.b].some(v=>st.vtx[v]&&st.vtx[v].p===i)){if(pt.t===r)best=Math.min(best,2);else if(pt.t==='any')best=Math.min(best,3);}});return best;}
function pmLongest(st,i){
  const mine=st.edge.map((x,e)=>x===i?e:-1).filter(e=>e>=0); if(!mine.length)return 0;
  const used=new Set(); let best=0;
  const dfs=(v,len)=>{best=Math.max(best,len); const b=st.vtx[v]; if(len>0&&b&&b.p!==i)return;
    for(const e of PM_G.verts[v].e){if(st.edge[e]!==i||used.has(e))continue;used.add(e);const E=PM_G.edges[e];dfs(E.a===v?E.b:E.a,len+1);used.delete(e);}};
  mine.forEach(e=>{const E=PM_G.edges[e];dfs(E.a,0);dfs(E.b,0);});
  return best;
}
function pmUpdateLongest(st){
  const n=st.players.length, L=st.players.map((p,i)=>pmLongest(st,i)); st.lens=L;
  const h=st.longest, mx=Math.max(...L);
  if(h!=null&&L[h]>=5&&L[h]>=mx)return;
  const c=L.map((x,i)=>x===mx&&mx>=5?i:-1).filter(i=>i>=0);
  const nh=c.length===1?c[0]:(h!=null&&c.includes(h)?h:null);
  if(nh!==h){st.longest=nh; if(nh!=null)st.log.push({p:nh,m:`🛤️ meraih Jalan Terpanjang (${mx} ruas, +2 poin).`}); else if(h!=null)st.log.push({p:-1,m:'🛤️ Jalan Terpanjang lepas dan belum ada pemiliknya.'});}
}
function pmProduce(st,sum){
  const n=st.players.length, gain=st.players.map(()=>({L:0,B:0,W:0,G:0,O:0}));
  st.board.hex.forEach((h,hi)=>{if(h.n!==sum||hi===st.board.robber)return;
    PM_G.hv[hi].forEach(v=>{const b=st.vtx[v];if(b)gain[b.p][h.t]+=b.c?2:1;});});
  const parts=[];
  PM_RES.forEach(r=>{const tot=gain.reduce((s,g)=>s+g[r],0); if(!tot)return; const who=gain.map((g,i)=>g[r]?i:-1).filter(i=>i>=0);
    if(tot>st.bank[r]){ if(who.length>1){gain.forEach(g=>g[r]=0);parts.push(`${PM_RN[r]} di bank kurang, tidak ada yang dapat`);return;} gain[who[0]][r]=st.bank[r]; }
    who.forEach(i=>{st.players[i].res[r]+=gain[i][r];st.bank[r]-=gain[i][r];});});
  const got=gain.map((g,i)=>{const s=PM_RES.filter(r=>g[r]).map(r=>`${g[r]} ${PM_RN[r]}`).join(', ');return s?`${st.players[i].nick||'P'+(i+1)}: ${s}`:'';}).filter(Boolean);
  return got.concat(parts);
}
function pmNextAfterRobber(st){st.phase=st.rret||'main';st.rret=null;}
function pmCheckWin(st,i){
  if(st.status!=='playing'||i!==st.turn)return;
  const v=pmVP(st,i,true); if(v>=10){st.status='ended';st.phase='ended';st.winner=i;st.endedAt=Date.now();st.turnAt=null;st.offer=null;
    st.log.push({p:i,m:`🏆 mencapai ${v} poin dan memenangkan pulau!`});}
}
function pmStealFrom(st,pi,v){
  const p=st.players[v], pool=PM_RES.flatMap(r=>Array(p.res[r]).fill(r));
  if(!pool.length){st.log.push({p:pi,m:`mencoba mencuri dari ${st.players[v].nick||'P'+(v+1)}, tapi kartunya kosong.`});return null;}
  const r=pool[Math.floor(Math.random()*pool.length)]; p.res[r]--; st.players[pi].res[r]++;
  st.log.push({p:pi,m:`mencuri 1 kartu dari ${st.players[v].nick||'P'+(v+1)}.`,priv:{[pi]:`kamu dapat ${PM_RN[r]}`,[v]:`kamu kehilangan ${PM_RN[r]}`}});
  return r;
}
function pmVictims(st,pi,h){return [...new Set(PM_G.hv[h].map(v=>st.vtx[v]).filter(b=>b&&b.p!==pi).map(b=>b.p))].filter(j=>pmTotal(st.players[j].res)>0);}
function pmEndTurn(st){
  const p=st.players[st.turn]; p.dev=p.dev.concat(p.devNew); p.devNew=[];
  st.turn=(st.turn+1)%st.players.length; if(st.turn===0)st.round++;
  st.phase='roll'; st.dice=null; st.devPlayed=false; st.offer=null; st.free=0; st.turnAt=Date.now();
}
function pmAct(st,pi,mv){
  if(st.status!=='playing')fail('Permainan sudah selesai');
  const n=st.players.length, P=st.players[pi], nm_=i=>st.players[i].nick||'Pemain '+(i+1);
  const own=()=>{if(pi!==st.turn)fail('Bukan giliranmu');};
  st.last={p:pi,m:''}; if(st.log.length>160)st.log=st.log.slice(-120);
  if(mv.type==='discard'){
    if(st.phase!=='discard'||!st.disc||!st.disc[pi])fail('Kamu tidak perlu membuang kartu');
    const need=st.disc[pi], g=mv.res||{}; if(pmTotal(g)!==need||!pmHas(P.res,g))fail(`Pilih tepat ${need} kartu untuk dibuang`);
    pmPay(st,P,g); delete st.disc[pi]; st.log.push({p:pi,m:`membuang ${need} kartu.`});
    if(!Object.keys(st.disc).length){st.disc=null;st.phase='robber';st.turnAt=Date.now();} return;
  }
  if(mv.type==='respond'){
    const o=st.offer; if(!o||pi===o.from)fail('Tidak ada tawaran untukmu');
    if(mv.yes&&!pmHas(P.res,o.get))fail('Kartumu tidak cukup untuk tawaran ini');
    o.resp[pi]=mv.yes?'yes':'no'; return;
  }
  own();
  if(st.phase==='setup'){
    const S=st.setup, order=pmSetupOrder(n);
    if(S.need==='S'){if(mv.type!=='settle')fail('Taruh pemukiman dulu');const v=mv.v;if(!(v>=0&&v<54)||!pmCanSettleAt(st,v))fail('Tidak bisa membangun di situ (harus berjarak 2 ruas dari pemukiman lain)');
      st.vtx[v]={p:pi,c:false}; S.v=v; S.need='R';
      if(S.i>=n){const got=[];PM_G.verts[v].h.forEach(h=>{const t=st.board.hex[h].t;if(t!=='D'){P.res[t]++;st.bank[t]--;got.push(PM_RN[t]);}});st.log.push({p:pi,m:`menaruh pemukiman kedua dan mendapat ${got.join(', ')||'tidak ada kartu'}.`});}
      else st.log.push({p:pi,m:'menaruh pemukiman pertama.'});
      return;}
    if(mv.type!=='road')fail('Taruh jalan di samping pemukiman barumu');
    if(!pmRoadOk(st,pi,mv.e,S.v))fail('Jalan harus menempel pada pemukiman yang baru kamu taruh');
    st.edge[mv.e]=pi; S.i++; S.need='S'; S.v=null; pmUpdateLongest(st);
    if(S.i>=order.length){st.phase='roll';st.turn=0;st.setup=null;st.log.push({p:-1,m:'🎲 Persiapan selesai. Permainan dimulai!'});}
    else st.turn=order[S.i];
    st.turnAt=Date.now(); return;
  }
  if(mv.type==='dev'){
    if(!['roll','main'].includes(st.phase))fail('Kartu pembangunan dimainkan sebelum lempar dadu atau di fase utama');
    if(st.devPlayed)fail('Hanya 1 kartu pembangunan per giliran'); const c=mv.card;
    const k=P.dev.indexOf(c); if(k<0||c==='V')fail(P.devNew.includes(c)?'Kartu yang baru dibeli baru bisa dimainkan giliran berikutnya':'Kamu tidak punya kartu itu');
    if(c!=='K'&&st.phase!=='main')fail('Hanya Ksatria yang boleh dimainkan sebelum lempar dadu');
    if(c==='Y'){const a=mv.res||[];if(a.length!==2||!a.every(r=>PM_RES.includes(r)))fail('Pilih 2 kartu sumber daya');
      const need={};a.forEach(r=>need[r]=(need[r]||0)+1);if(!pmHas(st.bank,need))fail('Bank tidak punya cukup kartu itu');}
    if(c==='M'&&!PM_RES.includes(mv.res))fail('Pilih 1 jenis sumber daya');
    if(c==='R'&&!pmRoadSpots(st,pi).length)fail('Tidak ada tempat untuk jalan baru');
    P.dev.splice(k,1); st.devPlayed=true;
    if(c==='K'){P.knights++; st.log.push({p:pi,m:'⚔️ memainkan Ksatria.'});
      if(P.knights>=3&&(st.largest==null||P.knights>st.players[st.largest].knights)&&st.largest!==pi){st.largest=pi;st.log.push({p:pi,m:`⚔️ meraih Pasukan Terbesar (${P.knights} ksatria, +2 poin).`});}
      st.rret=st.phase; st.phase='robber'; pmCheckWin(st,pi); return;}
    if(c==='Y'){mv.res.forEach(r=>{P.res[r]++;st.bank[r]--;});st.log.push({p:pi,m:`🎁 Panen Raya: mengambil ${mv.res.map(r=>PM_RN[r]).join(' & ')}.`});return;}
    if(c==='M'){let got=0;st.players.forEach((q,j)=>{if(j===pi)return;got+=q.res[mv.res];q.res[mv.res]=0;});P.res[mv.res]+=got;st.log.push({p:pi,m:`💰 Monopoli ${PM_RN[mv.res]}: mengambil ${got} kartu dari semua pemain.`});return;}
    if(c==='R'){st.free=2;st.phase='freeroad';st.log.push({p:pi,m:'🛤️ Bangun Jalan: membangun 2 jalan gratis.'});return;}
  }
  if(st.phase==='roll'){
    if(mv.type!=='roll')fail('Lempar dadu dulu');
    const d=mv.dice&&mv.dice.length===2?mv.dice:[1+Math.floor(Math.random()*6),1+Math.floor(Math.random()*6)], s=d[0]+d[1];
    st.dice=d; st.turnAt=Date.now();
    if(s===7){const disc={};st.players.forEach((q,j)=>{const t=pmTotal(q.res);if(t>7)disc[j]=Math.floor(t/2);});
      st.log.push({p:pi,m:`🎲 melempar 7! ${Object.keys(disc).length?'Yang memegang lebih dari 7 kartu harus membuang setengah.':'Perampok bergerak.'}`});
      if(Object.keys(disc).length){st.disc=disc;st.phase='discard';}else st.phase='robber'; st.rret='main'; return;}
    const got=pmProduce(st,s); st.phase='main';
    st.log.push({p:pi,m:`🎲 melempar ${s}. ${got.length?got.join(' · '):'Tidak ada yang mendapat hasil bumi.'}`}); return;
  }
  if(st.phase==='discard')fail('Menunggu pemain membuang kartu');
  if(st.phase==='robber'){
    if(mv.type!=='robber')fail('Pindahkan perampok dulu');
    const h=mv.h; if(!(h>=0&&h<19)||h===st.board.robber)fail('Pindahkan perampok ke petak lain');
    st.board.robber=h; const vic=pmVictims(st,pi,h);
    st.log.push({p:pi,m:`🦹 memindahkan perampok ke ${PM_TER[st.board.hex[h].t]}${st.board.hex[h].n?' '+st.board.hex[h].n:''}.`});
    if(vic.length===0){pmNextAfterRobber(st);return;}
    if(vic.length===1||(mv.v!=null&&vic.includes(mv.v))){pmStealFrom(st,pi,vic.length===1?vic[0]:mv.v);pmNextAfterRobber(st);return;}
    st.phase='steal'; st.vic=vic; return;
  }
  if(st.phase==='steal'){if(mv.type!=='steal'||!st.vic.includes(mv.v))fail('Pilih pemain yang mau dicuri');pmStealFrom(st,pi,mv.v);st.vic=null;pmNextAfterRobber(st);return;}
  if(st.phase==='freeroad'){
    if(mv.type==='build'&&mv.what==='road'){if(!pmRoadOk(st,pi,mv.e))fail('Tidak bisa membangun jalan di situ');if(pmPieces(st,pi).r>=15)fail('Jalanmu sudah habis (15)');
      st.edge[mv.e]=pi;st.free--;pmUpdateLongest(st);if(st.free<=0||!pmRoadSpots(st,pi).length||pmPieces(st,pi).r>=15){st.free=0;st.phase='main';}pmCheckWin(st,pi);return;}
    if(mv.type==='skipfree'){st.free=0;st.phase='main';return;}
    fail('Bangun jalan gratismu dulu');
  }
  if(st.phase!=='main')fail('Aksi tidak sesuai fase');
  if(mv.type==='build'){
    const w=mv.what, pc=pmPieces(st,pi);
    if(w==='road'){if(!pmHas(P.res,PM_COST.road))fail('Butuh 1 Kayu + 1 Bata');if(pc.r>=15)fail('Jalanmu sudah habis (15)');if(!pmRoadOk(st,pi,mv.e))fail('Jalan harus tersambung ke jalan/pemukimanmu');
      pmPay(st,P,PM_COST.road);st.edge[mv.e]=pi;st.log.push({p:pi,m:'membangun jalan.'});pmUpdateLongest(st);}
    else if(w==='settle'){if(!pmHas(P.res,PM_COST.settle))fail('Butuh Kayu, Bata, Ternak, Padi');if(pc.s>=5)fail('Pemukimanmu sudah habis (5)');
      if(!pmSettleSpots(st,pi).includes(mv.v))fail('Pemukiman harus di ujung jalanmu dan berjarak 2 ruas dari pemukiman lain');
      pmPay(st,P,PM_COST.settle);st.vtx[mv.v]={p:pi,c:false};st.log.push({p:pi,m:'membangun pemukiman (+1 poin).'});pmUpdateLongest(st);}
    else if(w==='city'){if(!pmHas(P.res,PM_COST.city))fail('Butuh 2 Padi + 3 Bijih');if(pc.c>=4)fail('Kotamu sudah habis (4)');
      const b=st.vtx[mv.v];if(!b||b.p!==pi||b.c)fail('Kota dibangun di atas pemukimanmu');
      pmPay(st,P,PM_COST.city);b.c=true;st.log.push({p:pi,m:'meningkatkan pemukiman jadi kota (+1 poin).'});}
    else fail('Bangunan tidak dikenal');
    pmCheckWin(st,pi); return;
  }
  if(mv.type==='buydev'){if(!pmHas(P.res,PM_COST.dev))fail('Butuh Ternak, Padi, Bijih');if(!st.devDeck.length)fail('Kartu pembangunan sudah habis');
    pmPay(st,P,PM_COST.dev);const c=st.devDeck.pop();P.devNew.push(c);st.log.push({p:pi,m:'membeli kartu pembangunan.',priv:{[pi]:`kamu dapat ${PM_DEVN[c]}`}});pmCheckWin(st,pi);return;}
  if(mv.type==='bank'){const g=mv.give,t=mv.get;if(!PM_RES.includes(g)||!PM_RES.includes(t)||g===t)fail('Pilih sumber daya yang berbeda');
    const k=pmRate(st,pi,g);if(P.res[g]<k)fail(`Butuh ${k} ${PM_RN[g]}`);if(st.bank[t]<1)fail(`Bank kehabisan ${PM_RN[t]}`);
    P.res[g]-=k;st.bank[g]+=k;P.res[t]++;st.bank[t]--;st.log.push({p:pi,m:`menukar ${k} ${PM_RN[g]} → 1 ${PM_RN[t]} ${k===4?'dengan bank':'lewat pelabuhan'}.`});return;}
  if(mv.type==='offer'){const g=mv.give||{},t=mv.get||{};
    if(!pmTotal(g)||!pmTotal(t))fail('Isi kartu yang diberi dan diminta');if(PM_RES.some(r=>g[r]&&t[r]))fail('Jangan menukar jenis yang sama');if(!pmHas(P.res,g))fail('Kartumu tidak cukup');
    const clean=o=>{const x={};PM_RES.forEach(r=>{if(o[r]>0)x[r]=Math.floor(o[r]);});return x;};
    st.offer={from:pi,give:clean(g),get:clean(t),resp:{},id:(st.offer&&st.offer.id||0)+1};
    st.log.push({p:pi,m:`menawarkan ${pmResTxt(st.offer.give)} untuk ${pmResTxt(st.offer.get)}.`});return;}
  if(mv.type==='cancel'){st.offer=null;return;}
  if(mv.type==='accept'){const o=st.offer;if(!o)fail('Tidak ada tawaran');const j=mv.p;if(o.resp[j]!=='yes')fail('Pemain itu belum menerima');
    const Q=st.players[j];if(!pmHas(P.res,o.give)||!pmHas(Q.res,o.get))fail('Kartu salah satu pihak sudah tidak cukup');
    PM_RES.forEach(r=>{const a=o.give[r]||0,b=o.get[r]||0;P.res[r]+=b-a;Q.res[r]+=a-b;});
    st.log.push({p:pi,m:`berdagang dengan ${nm_(j)}: ${pmResTxt(o.give)} ⇄ ${pmResTxt(o.get)}.`});st.offer=null;return;}
  if(mv.type==='end'){st.log.push({p:pi,m:'mengakhiri giliran.'});pmEndTurn(st);return;}
  fail('Aksi tidak dikenal');
}
function pmResTxt(o){return PM_RES.filter(r=>o[r]).map(r=>`${o[r]} ${PM_RN[r]}`).join(' + ')||'—';}
function pmPending(st){
  if(st.status!=='playing')return [];
  if(st.phase==='discard')return Object.keys(st.disc||{}).map(Number);
  return [st.turn];
}
