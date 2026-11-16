/* ---------- BOT PEMUKIM ---------- */
const PMB={easy:{noise:3,trade:false,dev:0.3,plan:false,rob:'rand'},normal:{noise:0.6,trade:true,dev:1,plan:true,rob:'lead'},hard:{noise:0,trade:true,dev:1,plan:true,rob:'lead',port:true,lr:true,army:true}};
function pmProd(st,i){const pr={L:0,B:0,W:0,G:0,O:0};st.vtx.forEach((b,v)=>{if(!b||b.p!==i)return;PM_G.verts[v].h.forEach(h=>{const x=st.board.hex[h];if(x.t!=='D'&&h!==st.board.robber)pr[x.t]+=(PM_PIPS[x.n]||0)*(b.c?2:1);});});return pr;}
function pmVScore(st,v,i,lv){
  const pr=pmProd(st,i), have=PM_RES.filter(r=>pr[r]>0), W={L:1.1,B:1.1,W:0.85,G:1,O:0.95};
  if(lv==='hard'){const cities=pmPieces(st,i).s>=2;if(cities){W.O=1.15;W.G=1.1;}}
  let s=0;const ts=new Set();
  PM_G.verts[v].h.forEach(h=>{const x=st.board.hex[h];if(x.t==='D')return;let p=(PM_PIPS[x.n]||0)*W[x.t];if(h===st.board.robber)p*=0.5;if(!have.includes(x.t))p*=1.25;s+=p;ts.add(x.t);});
  s+=ts.size*0.8;
  st.board.ports.forEach(pt=>{const E=PM_G.edges[pt.e];if(E.a===v||E.b===v)s+=pt.t==='any'?1.2:(pr[pt.t]>=5?2.5:0.6);});
  return s;
}
function pmBest(arr,f,noise){let b=null,bv=-1e9;arr.forEach(x=>{const v=f(x)+(noise?Math.random()*noise:0);if(v>bv){bv=v;b=x;}});return b;}
function pmNeedFor(P,c){const m={};PM_RES.forEach(r=>{const d=(c[r]||0)-(P.res[r]||0);if(d>0)m[r]=d;});return m;}
function pmTarget(st,i,lv){
  const P=st.players[i], pc=pmPieces(st,i), spots=pmSettleSpots(st,i);
  const opts=[];
  if(pc.c<4&&pc.s>0)opts.push(['city',PM_COST.city,3.2]);
  if(pc.s<5&&spots.length)opts.push(['settle',PM_COST.settle,3]);
  if(st.devDeck.length)opts.push(['dev',PM_COST.dev,lv==='hard'?1.6:1.3]);
  if(pc.r<15&&!spots.length)opts.push(['road',PM_COST.road,1.5]);
  if(!opts.length)return null;
  return pmBest(opts,o=>o[2]-pmTotal(pmNeedFor(P,o[1]))*0.9,0);
}
/* jalur jalan terpendek ke titik pemukiman bagus */
function pmRoadPlan(st,i,lv){
  const dist=Array(54).fill(Infinity), from=Array(54).fill(-1), q=[];
  st.vtx.forEach((b,v)=>{if(b&&b.p===i){dist[v]=0;q.push(v);}});
  st.edge.forEach((x,e)=>{if(x===i){const E=PM_G.edges[e];[E.a,E.b].forEach(v=>{const b=st.vtx[v];if((!b||b.p===i)&&dist[v]>0){dist[v]=0;q.push(v);}});}});
  while(q.length){const v=q.shift();const b=st.vtx[v];if(b&&b.p!==i)continue;
    for(const e of PM_G.verts[v].e){const x=st.edge[e];if(x!=null&&x!==i)continue;const E=PM_G.edges[e],u=E.a===v?E.b:E.a;const c=dist[v]+(x===i?0:1);
      if(c<dist[u]){dist[u]=c;from[u]=e;x===i?q.unshift(u):q.push(u);}}}
  let best=null,bv=-1e9;
  for(let v=0;v<54;v++){if(!pmCanSettleAt(st,v)||dist[v]===Infinity||dist[v]===0||dist[v]>4)continue;const s=pmVScore(st,v,i,lv)-dist[v]*2.2;if(s>bv){bv=s;best=v;}}
  if(best==null)return null;
  let v=best,e=-1;while(from[v]>=0){const ed=from[v];if(st.edge[ed]==null)e=ed;const E=PM_G.edges[ed];v=E.a===v?E.b:E.a;if(dist[v]===0&&st.edge[ed]==null){e=ed;break;}}
  return e>=0&&pmRoadOk(st,i,e)?e:null;
}
function pmBotRobber(st,i,lv){
  const L=PMB[lv]||PMB.normal, vp=st.players.map((p,j)=>pmVP(st,j,false));
  const cand=[...Array(19).keys()].filter(h=>h!==st.board.robber&&!PM_G.hv[h].some(v=>st.vtx[v]&&st.vtx[v].p===i));
  const h=pmBest(cand.length?cand:[...Array(19).keys()].filter(h=>h!==st.board.robber),h=>{const x=st.board.hex[h];let s=0;
    PM_G.hv[h].forEach(v=>{const b=st.vtx[v];if(b&&b.p!==i)s+=(PM_PIPS[x.n]||0)*(b.c?2:1)*(L.rob==='lead'?1+vp[b.p]*0.25:1)+(pmTotal(st.players[b.p].res)?1:0);});return s;},L.rob==='rand'?6:0.2);
  const vic=pmVictims(st,i,h);
  return {type:'robber',h,v:vic.length?pmBest(vic,j=>vp[j]*2+pmTotal(st.players[j].res)*0.3,0):undefined};
}
function pmBotDiscard(st,i){
  const P=st.players[i], need=st.disc[i], keep={...P.res}, g={};
  for(let k=0;k<need;k++){const r=pmBest(PM_RES.filter(r=>keep[r]>0),r=>keep[r]-(r==='O'||r==='G'?0.4:0),0);keep[r]--;g[r]=(g[r]||0)+1;}
  return {type:'discard',res:g};
}
function pmBotRespond(st,i,lv){
  const o=st.offer, P=st.players[i];
  if(!pmHas(P.res,o.get))return {type:'respond',yes:false};
  if(pmVP(st,o.from,false)>=8)return {type:'respond',yes:false};
  if(lv==='easy')return {type:'respond',yes:Math.random()<0.35};
  const t=pmTarget(st,i,lv), need=t?pmNeedFor(P,t[1]):{};
  const gain=PM_RES.reduce((s,r)=>s+Math.min(o.give[r]||0,need[r]||0),0);
  const lose=PM_RES.reduce((s,r)=>s+Math.min(o.get[r]||0,Math.max(0,(t&&t[1][r]||0)-Math.max(0,P.res[r]-(o.get[r]||0)))),0);
  const fair=pmTotal(o.give)>=pmTotal(o.get);
  return {type:'respond',yes:gain>0&&lose===0&&(fair||gain>=pmTotal(o.get))};
}
function pmBotMove(st,i,lv){
  lv=PMB[lv]?lv:'normal'; const L=PMB[lv], P=st.players[i];
  if(st.phase==='discard')return pmBotDiscard(st,i);
  if(st.phase==='setup'){const S=st.setup;
    if(S.need==='S'){const sp=pmSettleSpots(st,i,true);return {type:'settle',v:pmBest(sp,v=>pmVScore(st,v,i,lv),L.noise)};}
    const es=PM_G.verts[S.v].e.filter(e=>st.edge[e]==null);
    return {type:'road',e:pmBest(es,e=>{const E=PM_G.edges[e],u=E.a===S.v?E.b:E.a;let b=0;PM_G.verts[u].n.forEach(w=>{if(w!==S.v&&pmCanSettleAt(st,w))b=Math.max(b,pmVScore(st,w,i,lv));});return b;},L.noise)};
  }
  const canDev=c=>!st.devPlayed&&P.dev.includes(c);
  const robbed=PM_G.hv[st.board.robber].some(v=>st.vtx[v]&&st.vtx[v].p===i);
  if(st.phase==='roll'){
    if(canDev('K')&&(robbed||(L.army&&P.knights>=2&&(st.largest==null||st.largest!==i))))return {type:'dev',card:'K'};
    return {type:'roll'};
  }
  if(st.phase==='robber')return pmBotRobber(st,i,lv);
  if(st.phase==='steal'){const vp=st.players.map((p,j)=>pmVP(st,j,false));return {type:'steal',v:pmBest(st.vic,j=>vp[j],0)};}
  if(st.phase==='freeroad'){const e=pmRoadPlan(st,i,lv);const sp=pmRoadSpots(st,i);return e!=null?{type:'build',what:'road',e}:sp.length?{type:'build',what:'road',e:sp[Math.floor(Math.random()*sp.length)]}:{type:'skipfree'};}
  if(st.phase!=='main')return {type:'end'};
  if(st.offer&&st.offer.from===i)return {type:'cancel'};
  const pc=pmPieces(st,i), spots=pmSettleSpots(st,i);
  // kartu pembangunan
  if(Math.random()<L.dev){
    if(canDev('K')&&(robbed||(L.army&&P.knights>=2)))return {type:'dev',card:'K'};
    const t=pmTarget(st,i,lv);
    if(canDev('Y')&&t){const need=pmNeedFor(P,t[1]),list=PM_RES.flatMap(r=>Array(need[r]||0).fill(r));if(list.length<=2&&list.length){while(list.length<2)list.push(pmBest(PM_RES,r=>-P.res[r]+(st.bank[r]?0:-99),0));if(list.every(r=>st.bank[r]>0))return {type:'dev',card:'Y',res:list.slice(0,2)};}}
    if(canDev('M')){const r=pmBest(PM_RES,r=>st.players.reduce((s,q,j)=>j===i?s:s+q.res[r],0),0),g=st.players.reduce((s,q,j)=>j===i?s:s+q.res[r],0);if(g>=4)return {type:'dev',card:'M',res:r};}
    if(canDev('R')&&pc.r<=13){const e=pmRoadPlan(st,i,lv);if(e!=null)return {type:'dev',card:'R'};}
  }
  // bangun
  if(pmHas(P.res,PM_COST.city)&&pc.c<4){const cs=pmCitySpots(st,i);if(cs.length)return {type:'build',what:'city',v:pmBest(cs,v=>pmVScore(st,v,i,lv),L.noise)};}
  if(pmHas(P.res,PM_COST.settle)&&pc.s<5&&spots.length)return {type:'build',what:'settle',v:pmBest(spots,v=>pmVScore(st,v,i,lv),L.noise)};
  if(pmHas(P.res,PM_COST.road)&&pc.r<15){
    const wantRoad=!spots.length||(L.lr&&st.lens[i]>=4&&st.longest!==i&&st.lens[i]+2>=Math.max(...st.lens));
    if(wantRoad){const e=L.plan?pmRoadPlan(st,i,lv):null;const sp=pmRoadSpots(st,i);
      if(e!=null)return {type:'build',what:'road',e};
      if(!L.plan&&sp.length)return {type:'build',what:'road',e:sp[Math.floor(Math.random()*sp.length)]};
      if(L.lr&&sp.length&&st.lens[i]>=4)return {type:'build',what:'road',e:pmBest(sp,e=>{st.edge[e]=i;const x=pmLongest(st,i);st.edge[e]=null;return x;},0.1)};}
  }
  if(pmHas(P.res,PM_COST.dev)&&st.devDeck.length){
    const t=pmTarget(st,i,lv);
    if(!t||t[0]==='dev'||lv==='easy'||(t[0]==='road'))return {type:'buydev'};
    const left={...P.res};PM_RES.forEach(r=>left[r]-=(PM_COST.dev[r]||0));
    if(pmHas(left,t[1])||pmTotal(P.res)>=7)return {type:'buydev'};
  }
  // dagang bank / pelabuhan
  if(L.trade||pmTotal(P.res)>7){const t=pmTarget(st,i,lv);
    if(t){const need=pmNeedFor(P,t[1]);const miss=PM_RES.filter(r=>need[r]&&st.bank[r]>0);
      if(miss.length){for(const g of PM_RES.slice().sort((a,b)=>P.res[b]-P.res[a])){const k=pmRate(st,i,g),spare=P.res[g]-(t[1][g]||0);if(spare>=k&&!need[g])return {type:'bank',give:g,get:pmBest(miss,r=>need[r],0)};}}}}
  return {type:'end'};
}
