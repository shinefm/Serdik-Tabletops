class GameErr extends Error{}
const fail=m=>{throw new GameErr(m);};
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const fs=require('fs');eval(fs.readFileSync(__dirname+'/pemukim.js','utf8')+'\n'+fs.readFileSync(__dirname+'/pemukim_bot.js','utf8')+';globalThis.PM_G=PM_G;');
const T=(name,f)=>{try{const r=f();console.log((r===true?'✔':'✘'),name,r===true?'':r);}catch(e){console.log('✘',name,'THREW',e.message);}};
const E=f=>{try{f();return 'OK';}catch(e){if(!(e instanceof GameErr))throw e;return e.message;}};
function fresh(n=3){const st={game:'pemukim',players:Array.from({length:n},(_,i)=>({id:'p'+i,nick:'P'+i}))};pmStart(st);return st;}
function setupDone(st){while(st.phase==='setup'){pmAct(st,st.turn,pmBotMove(st,st.turn,'normal'));}return st;}
T('setup order snake & resources',()=>{const st=fresh(3);const seq=[];while(st.phase==='setup'){if(st.setup.need==='S')seq.push(st.turn);pmAct(st,st.turn,pmBotMove(st,st.turn,'normal'));}
  return JSON.stringify(seq)==='[0,1,2,2,1,0]'&&st.players.every(p=>pmTotal(p.res)<=3)&&st.phase==='roll'&&st.turn===0||JSON.stringify(seq);});
T('distance rule',()=>{const st=fresh(3);pmAct(st,0,{type:'settle',v:20});const nb=PM_G.verts[20].n[0];const e=PM_G.verts[20].e[0];pmAct(st,0,{type:'road',e});return E(()=>pmAct(st,1,{type:'settle',v:nb})).includes('jarak')||'allowed adjacent';});
T('setup road must touch new settlement',()=>{const st=fresh(3);pmAct(st,0,{type:'settle',v:20});const far=PM_G.verts[40].e[0];return E(()=>pmAct(st,0,{type:'road',e:far})).includes('menempel');});
T('roll 7 discard & robber',()=>{const st=setupDone(fresh(3));st.players[1].res={L:5,B:4,W:0,G:0,O:0};pmAct(st,0,{type:'roll',dice:[3,4]});
  if(st.phase!=='discard'||st.disc[1]!==4)return 'phase '+st.phase+JSON.stringify(st.disc);
  const bad=E(()=>pmAct(st,1,{type:'discard',res:{L:3}}));pmAct(st,1,{type:'discard',res:{L:2,B:2}});
  return bad.includes('tepat 4')&&st.phase==='robber'&&pmTotal(st.players[1].res)===5;});
T('robber cannot stay',()=>{const st=setupDone(fresh(3));pmAct(st,0,{type:'roll',dice:[3,4]});if(st.phase==='discard')return 'skip';return E(()=>pmAct(st,0,{type:'robber',h:st.board.robber})).includes('petak lain');});
T('dev card not same turn',()=>{const st=setupDone(fresh(3));pmAct(st,0,{type:'roll',dice:[2,2]});st.players[0].res={L:0,B:0,W:1,G:1,O:1};st.devDeck.push('K');pmAct(st,0,{type:'buydev'});
  const r=E(()=>pmAct(st,0,{type:'dev',card:'K'}));pmAct(st,0,{type:'end'});return r.includes('giliran berikutnya')&&st.players[0].dev.includes('K');});
T('knight before roll returns to roll',()=>{const st=setupDone(fresh(3));st.players[0].dev=['K'];pmAct(st,0,{type:'dev',card:'K'});const h=(st.board.robber+3)%19;pmAct(st,0,{type:'robber',h});if(st.phase==='steal')pmAct(st,0,{type:'steal',v:st.vic[0]});return st.phase==='roll'&&st.players[0].knights===1||st.phase;});
T('one dev per turn',()=>{const st=setupDone(fresh(3));pmAct(st,0,{type:'roll',dice:[2,2]});st.players[0].dev=['Y','Y'];pmAct(st,0,{type:'dev',card:'Y',res:['O','O']});return E(()=>pmAct(st,0,{type:'dev',card:'Y',res:['G','G']})).includes('1 kartu');});
T('monopoly',()=>{const st=setupDone(fresh(3));pmAct(st,0,{type:'roll',dice:[2,2]});st.players.forEach(p=>p.res.O=2);st.players[0].dev=['M'];pmAct(st,0,{type:'dev',card:'M',res:'O'});return st.players[0].res.O===6&&st.players[1].res.O===0;});
T('bank 4:1 and port',()=>{const st=setupDone(fresh(3));pmAct(st,0,{type:'roll',dice:[2,2]});st.players[0].res={L:4,B:0,W:0,G:0,O:0};const r=pmRate(st,0,'L');pmAct(st,0,{type:'bank',give:'L',get:'O'});return st.players[0].res.O===1&&st.players[0].res.L===4-r;});
T('player trade',()=>{const st=setupDone(fresh(3));pmAct(st,0,{type:'roll',dice:[2,2]});st.players[0].res={L:2,B:0,W:0,G:0,O:0};st.players[1].res={L:0,B:0,W:0,G:0,O:1};
  pmAct(st,0,{type:'offer',give:{L:2},get:{O:1}});pmAct(st,1,{type:'respond',yes:true});pmAct(st,0,{type:'accept',p:1});return st.players[0].res.O===1&&st.players[1].res.L===2&&!st.offer;});
T('longest road award & break',()=>{const st=fresh(3);
  // manual: player0 builds chain of 5 roads along a path
  st.phase='main';st.turn=0;st.setup=null;let path=null,v0=0;
  const find=(v,seen,acc)=>{if(acc.length===6)return acc;for(const e of PM_G.verts[v].e){const E=PM_G.edges[e];const u=E.a===v?E.b:E.a;if(seen.has(u))continue;seen.add(u);const r=find(u,seen,[...acc,{e,u}]);if(r)return r;seen.delete(u);}return null;};
  for(v0=0;!path;v0++)path=find(v0,new Set([v0]),[]);v0--;st.vtx[v0]={p:0,c:false};
  st.players[0].res={L:9,B:9,W:0,G:0,O:0};for(const s of path.slice(0,5))pmAct(st,0,{type:'build',what:'road',e:s.e});
  if(st.longest!==0)return 'no award '+st.lens;
  // opponent settlement in the middle breaks it
  st.vtx[path[2].u]={p:1,c:false};pmUpdateLongest(st);return st.longest===null&&st.lens[0]===3||('after break '+st.longest+' '+st.lens);});
T('bank shortage rule',()=>{const st=setupDone(fresh(3));const h=st.board.hex.findIndex((x,i)=>x.t!=='D'&&i!==st.board.robber&&PM_G.hv[i].filter(v=>st.vtx[v]).map(v=>st.vtx[v].p).filter((p,_,a)=>a.indexOf(p)!==a.lastIndexOf(p)||true).length>=1);
  const t=st.board.hex[h].t;st.bank[t]=0;const before=st.players.map(p=>p.res[t]);const tot=()=>st.bank[t]+st.players.reduce((s,p)=>s+p.res[t],0);st.players[0].res[t]+=19-tot();
  const n=st.board.hex[h].n;pmAct(st,0,{type:'roll',dice:[Math.min(6,n-1),n-Math.min(6,n-1)]});return st.bank[t]>=0;});
T('win at 10 on own turn',()=>{const st=setupDone(fresh(3));pmAct(st,0,{type:'roll',dice:[2,2]});st.players[0].devNew=['V','V','V','V','V','V','V','V'];st.players[0].res={L:0,B:0,W:1,G:1,O:1};st.devDeck.push('K');pmAct(st,0,{type:'buydev'});return st.status==='ended'&&st.winner===0||pmVP(st,0,true);});
T('cannot act out of turn',()=>{const st=setupDone(fresh(3));return E(()=>pmAct(st,1,{type:'roll'})).includes('Bukan');});
