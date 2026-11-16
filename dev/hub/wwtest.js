class GameErr extends Error{}
const fail=m=>{throw new GameErr(m);};
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const fs=require('fs');eval(fs.readFileSync('content.js','utf8')+'\n'+fs.readFileSync('engines.js','utf8')+'\nglobalThis.H={wwStart,wwAct,wwDeal,wwFinal,wwGet,hubWinners,WW_ROLES,wwPreset};');
const tryE=f=>{try{f();return 'OK';}catch(e){if(!(e instanceof GameErr))throw e;return e.message;}};
// deterministic scenario: 4 players, rig deck
function rig(deal,acts,votes){
  const n=deal.length-3, st={game:'werewolf',players:Array.from({length:n},(_,i)=>({id:'u'+i,nick:'P'+i}))};
  H.wwStart(st); st.dk=require('vm')?null:null;
  st.seed='abc'; st.dk=(()=>{let h=2166136261;for(const ch of 'abc')h=Math.imul(h^ch.charCodeAt(0),16777619)>>>0;let o='';const s=deal.join('');for(let i=0;i<s.length;i++){h=Math.imul(h^(i+7),2654435761)>>>0;o+=((s.charCodeAt(i)^(h&255))).toString(16).padStart(2,'0');}return o;})();
  st.ak=null; st.vk=null; eval('wwPut(st,"ak",{});wwPut(st,"vk",{})');
  for(let i=0;i<n;i++)H.wwAct(st,i,{type:'night',...(acts[i]||{skip:true})});
  const fin=H.wwFinal(st).join('');
  for(let i=0;i<n;i++)if(votes[i]!=null)H.wwAct(st,i,{type:'vote',target:votes[i]});
  if(st.status!=='ended')H.wwAct(st,0,{type:'timeout'});
  return {fin,dead:st.reveal.dead,winBy:st.winBy,w:H.hubWinners(st)};
}
// players: 0 W,1 R,2 T,3 D ; center S,V,I
let r=rig(['W','R','T','D','S','V','I'],{1:{p:0},2:{ps:[0,3]},3:{c:1}},{0:1,1:3,2:3,3:2});
console.log('swap test fin',r.fin,'(expect R W D... -> robber takes W: 0=R,1=W; TM swaps 0,3: 0=D,3=R; drunk(3) swaps with center1: 3=V,c1=R) =>',r.fin==='DWTVSRI', r);
// hunter: 0 H votes 2 ; 1,2 vote 0 -> 0 dies, hunter kills 2 (W)
r=rig(['H','V','W','S','R','T','V'],{4:{}},{0:2,1:0,2:0});
console.log('hunter',r.dead,r.winBy,r.w);
// tanner dies
r=rig(['N','W','V','S','R','T','V'],{},{0:1,1:0,2:0});
console.log('tanner',r.dead,r.winBy,r.w);
// everyone 1 vote -> nobody dies, wolves in play
r=rig(['W','V','V','S','R','T','D'],{3:{c:[0,1]}},{0:1,1:2,2:0});
console.log('nodeath',r.dead,r.winBy,r.w);
// no wolf in play, nobody dies
r=rig(['V','V','S','T','W','W','D'],{2:{c:[0,1]}},{0:1,1:2,2:0});
console.log('nowolf',r.dead,r.winBy,r.w);
// lone wolf peek + minion
r=rig(['W','M','V','W','S','R','T'],{0:{c:0}},{0:2,1:2,2:0});
console.log('minion',r.dead,r.winBy,r.w);
// illegal
{const st={game:'werewolf',players:[0,1,2,3].map(i=>({id:'u'+i}))};H.wwStart(st);const d=H.wwDeal(st);
 const ri=d.indexOf('R'),di=d.indexOf('D');
 if(ri>=0&&ri<4)console.log('robber self:',tryE(()=>H.wwAct(st,ri,{type:'night',p:ri})));
 if(di>=0&&di<4)console.log('drunk skip:',tryE(()=>H.wwAct(st,di,{type:'night',skip:true})));
 console.log('vote at night:',tryE(()=>H.wwAct(st,0,{type:'vote',target:1})));
 console.log('bad deck:',tryE(()=>{const s2={game:'werewolf',roles:['W','V','V'],players:[0,1,2].map(i=>({id:'x'+i}))};H.wwStart(s2);}));
 console.log('one mason:',tryE(()=>{const s2={game:'werewolf',roles:['W','K','V','V','S','R'],players:[0,1,2].map(i=>({id:'x'+i}))};H.wwStart(s2);}));
}
// random fuzz
let stuck=0,W={};
for(let g=0;g<4000;g++){const n=3+g%8;const st={game:'werewolf',players:Array.from({length:n},(_,i)=>({id:'u'+i,nick:'P'+i}))};H.wwStart(st);
  const d=H.wwDeal(st);let guard=0;
  while(st.phase==='night'&&guard++<200){const i=Math.floor(Math.random()*n);if(st.done.includes(i))continue;
    const r=d[i],o=()=>{let x;do x=Math.floor(Math.random()*n);while(x===i);return x;};
    const mv=r==='S'?(Math.random()<.5?{p:o()}:{c:[0,2]}):r==='R'?{p:o()}:r==='T'?(n>=3?{ps:(()=>{const a=o();let b;do b=o();while(b===a);return [a,b];})()}:{skip:true}):r==='D'?{c:Math.floor(Math.random()*3)}:r==='W'?{c:Math.floor(Math.random()*3)}:{};
    try{H.wwAct(st,i,{type:'night',...mv});}catch(e){if(!(e instanceof GameErr))throw e;H.wwAct(st,i,{type:'night',skip:r!=='D',c:0});}
    if(Math.random()<0.02)H.wwAct(st,0,{type:'timeout'});}
  for(let i=0;i<n&&st.status==='playing';i++){if(Math.random()<0.1)continue;let t;do t=Math.floor(Math.random()*n);while(t===i);H.wwAct(st,i,{type:'vote',target:t});}
  if(st.status==='playing')H.wwAct(st,0,{type:'timeout'});
  if(st.status!=='ended')stuck++;
  const f=H.wwFinal(st);if(f.slice().sort().join('')!==d.slice().sort().join(''))throw 'card conservation';
  W[st.winner]=(W[st.winner]||0)+1;}
console.log('fuzz stuck',stuck,W);
