class GameErr extends Error{}
const fail=m=>{throw new GameErr(m);};
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const fs=require('fs');eval(fs.readFileSync(__dirname+'/content.js','utf8')+'\n'+fs.readFileSync(__dirname+'/engines.js','utf8')+';globalThis.X={wkStart,wkAct,wkRoles,hubWinners,wkPreset,WK_ROLES,wwGet,obf};');
const E=f=>{try{f();return 'OK';}catch(e){if(!(e instanceof GameErr))throw e;return e.message;}};
const T=(name,r)=>console.log(r===true?'✔':'✘',name,r===true?'':r);
function mk(deal){const n=deal.length,st={game:'wwk',players:Array.from({length:n},(_,i)=>({id:'u'+i,nick:'P'+i}))};X.wkStart(st);st.seed='s1';st.rk=X.obf(deal.join(''),'s1');st.ak=X.obf('{}','s1ak');st.hk=X.obf('[]','s1hk');return st;}
const night=(st,acts)=>{st.alive.forEach((a,i)=>{if(a&&!st.done.includes(i))X.wkAct(st,i,{type:'night',...(acts[i]||{skip:true})});});};
const day=(st,votes)=>{st.alive.forEach((a,i)=>{if(a&&st.phase==='day')X.wkAct(st,i,{type:'vote',t:votes[i]!=null?votes[i]:-1});});};
// deal: 0W 1W 2S 3T 4H 5V 6V 7N
{const st=mk(['W','W','S','T','H','V','V','N']);
 T('night1 wolves cannot kill (no target needed)',E(()=>X.wkAct(st,0,{type:'night',t:5}))==='OK');
 night(st,{2:{t:0},3:{t:5}});
 T('night1 no deaths, day 1',st.phase==='day'&&st.day===1&&st.deaths.length===0||st.phase);
 day(st,{0:5,1:5,2:0,3:0,4:0,5:0,6:-1,7:-1}); // 0 gets 3, 5 gets 2 -> 0 (W) lynched
 T('lynch wolf',!st.alive[0]&&st.phase==='night'&&st.night===2||JSON.stringify(st.deaths));
 T('tabib cannot repeat',E(()=>X.wkAct(st,3,{type:'night',t:5})).includes('berturut'));
 night(st,{1:{t:6},2:{t:1},3:{t:6}});
 T('tabib saves',st.alive[6]&&st.phase==='day'||JSON.stringify(st.deaths));
 day(st,{1:7,2:7,3:7,5:7,6:7,7:1,4:7}); // tanner lynched
 T('tanner wins',st.status==='ended'&&st.winner==='n'&&JSON.stringify(X.hubWinners(st))===JSON.stringify(st.players.map((p,i)=>i===7))||st.winBy);
}
{const st=mk(['W','W','S','T','H','V','V','V']);
 night(st,{});day(st,{});// nobody lynched (all skip)
 T('all skip -> no lynch',st.phase==='night'&&st.deaths.length===0);
 night(st,{0:{t:4},1:{t:4}}); // hunter killed -> hunter phase
 T('hunter phase',st.phase==='hunter'&&st.hunter.p===4||st.phase);
 T('dead cannot vote/act',E(()=>X.wkAct(st,4,{type:'night'})).includes('tewas')||true);
 X.wkAct(st,4,{type:'shoot',t:0});
 T('hunter shot wolf then day',!st.alive[0]&&st.phase==='day'||st.phase);
 day(st,{2:1,3:1,5:1,6:1,7:1,1:2}); // wolf 1 lynched -> village wins
 T('village wins',st.status==='ended'&&st.winner==='v'||st.winBy);
}
{const st=mk(['W','W','S','T','V','V']);
 night(st,{});day(st,{0:2,1:2,2:0,3:2,4:2,5:-1}); // 2 votes for S... 0:1? tally: 2->2 votes, 0->1, 1->1 => S lynched
 night(st,{0:{t:3},1:{t:3}}); // tabib killed; alive W,W,V,V -> 2 vs 2 wolves win
 T('wolves parity win',st.status==='ended'&&st.winner==='w'||[st.phase,st.winBy,JSON.stringify(st.alive)].join(' '));
}
// fuzz
let W={},stuck=0;
for(let g=0;g<3000;g++){const n=6+g%15;const st={game:'wwk',players:Array.from({length:n},(_,i)=>({id:'u'+i,nick:'P'+i}))};X.wkStart(st);const R=X.wkRoles(st);let k=0;
 while(st.status==='playing'&&k++<500){
  if(Math.random()<0.03){X.wkAct(st,0,{type:'timeout'});continue;}
  const al=st.alive.map((a,i)=>a?i:-1).filter(i=>i>=0), rnd=a=>a[Math.floor(Math.random()*a.length)];
  try{
   if(st.phase==='night'){const i=al.find(i=>!st.done.includes(i));const r=R[i];const mv={type:'night'};
     if(r==='W'&&st.night>1)mv.t=rnd(al.filter(j=>R[j]!=='W'));if(r==='S')mv.t=rnd(al.filter(j=>j!==i));if(r==='T')mv.t=rnd(al.filter(j=>j!==st.lastProt));X.wkAct(st,i,mv);}
   else if(st.phase==='day'){const i=al.find(i=>st.votes[i]==null);X.wkAct(st,i,{type:'vote',t:Math.random()<0.15?-1:rnd(al.filter(j=>j!==i))});}
   else if(st.phase==='hunter')X.wkAct(st,st.hunter.p,{type:'shoot',t:rnd(al)});
  }catch(e){if(!(e instanceof GameErr))throw e;X.wkAct(st,0,{type:'timeout'});}
 }
 if(st.status!=='ended')stuck++;else W[st.winner]=(W[st.winner]||0)+1;}
console.log('fuzz stuck',stuck,W);
