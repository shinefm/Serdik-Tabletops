class GameErr extends Error{}
const fail=m=>{throw new GameErr(m);};
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const fs=require('fs');eval(fs.readFileSync('content.js','utf8')+'\n'+fs.readFileSync('engines.js','utf8')+'\nglobalThis.H={rapatStart,rapatAct,rapatRoles,hubWinners,rapatSide};');
const W={I:0,O:0},why={};let errs=0;
for(let g=0;g<3000;g++){const n=5+g%6;const st={game:'rapat',special:g%3!==0,players:Array.from({length:n},(_,i)=>({id:'u'+i,nick:'P'+i}))};H.rapatStart(st);
 const roles=H.rapatRoles(st);let steps=0;
 while(st.status==='playing'&&steps++<400){
  try{
   if(Math.random()<0.08){H.rapatAct(st,0,{type:'timeout'});continue;}
   if(st.phase==='propose'){const t=shuffle(st.players.map((p,i)=>i)).slice(0,st.missions[st.mi].size);H.rapatAct(st,st.leader,{type:'propose',team:t});}
   else if(st.phase==='vote'){const i=st.players.findIndex((p,i)=>st.votes[i]==null);H.rapatAct(st,i,{type:'vote',yes:Math.random()<0.6});}
   else if(st.phase==='mission'){const i=st.team.find(i=>!st.played.includes(i));H.rapatAct(st,i,{type:'play',card:H.rapatSide(roles[i])==='O'&&Math.random()<0.5?'f':'s'});}
   else if(st.phase==='shoot'){const d=roles.indexOf('D');H.rapatAct(st,d,{type:'shoot',target:(d+1+Math.floor(Math.random()*(n-1)))%n});}
  }catch(e){if(!(e instanceof GameErr))throw e;errs++;}
 }
 if(st.status!=='ended')throw 'stuck '+st.phase;
 W[st.winner]++;why[st.winBy]=(why[st.winBy]||0)+1;
 const w=H.hubWinners(st);if(w.some((x,i)=>x!==(H.rapatSide(roles[i])===st.winner)))throw 'winners';
}
console.log(W,why,'errs',errs);
