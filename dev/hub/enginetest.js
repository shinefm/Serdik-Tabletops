class GameErr extends Error{}
const fail=m=>{throw new GameErr(m);};
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const fs=require('fs');eval(fs.readFileSync('content.js','utf8')+'\n'+fs.readFileSync('engines.js','utf8')+'\nglobalThis.H={sandiStart,sandiAct,sandiKey,sandiLeft,rapatStart,rapatAct,rapatRoles,hubWinners,packTerms,termOf,TERMS,obf,deobf,sandiNormalize};');
// content checks
for(const mk in H.TERMS){const L=H.TERMS[mk];const dup=L.map(t=>t[0].toLowerCase()).filter((w,i,a)=>a.indexOf(w)!==i);console.log(mk,L.length,'terms',dup.length?'DUP '+dup:'', 'maxlen',Math.max(...L.map(t=>t[0].length)), L.filter(t=>t[0].length>14).map(t=>t[0]).join('|'));}
console.log('obf roundtrip',H.deobf(H.obf('rbnxrrbb','abc'),'abc')==='rbnxrrbb');
// sandi random games
let stats={r:0,b:0,audit:0,errs:0,turns:[]};
for(let g=0;g<500;g++){
  const n=4+g%5; const st={game:'sandi',pack:['mix','MK01','MK02','MK03','MK04','MK05','MK06'][g%7],players:Array.from({length:n},(_,i)=>({id:'u'+i,nick:'P'+i}))};
  H.sandiStart(st);
  if(st.words.length!==25)throw 'words';
  const k=H.sandiKey(st);if(k.filter(c=>c==='x').length!==1)throw 'key';
  let steps=0;
  while(st.status==='playing'&&steps++<500){
    const team=st.turnTeam, mem=st.players.map((p,i)=>i).filter(i=>st.players[i].team===team);
    const ket=mem.find(i=>st.players[i].ketua), gs=mem.filter(i=>!st.players[i].ketua);
    try{
      if(st.phase==='clue'){ if(Math.random()<0.05){H.sandiAct(st,ket,{type:'timeout'});continue;} H.sandiAct(st,ket,{type:'clue',word:'Petunjuk'+steps,num:1+Math.floor(Math.random()*3)}); }
      else{ const un=st.rev.map((r,i)=>r?-1:i).filter(i=>i>=0);
        // guesser: 70% picks own colour
        const own=un.filter(i=>k[i]===team); const pick=Math.random()<0.7&&own.length?own[0]:un[Math.floor(Math.random()*un.length)];
        if(st.left<st.clue.n+1&&Math.random()<0.3) H.sandiAct(st,gs[0],{type:'endturn'}); else H.sandiAct(st,gs[0],{type:'guess',i:pick}); }
    }catch(e){ if(!(e instanceof GameErr))throw e; stats.errs++; }
  }
  if(st.status!=='ended')throw 'stuck';
  stats[st.winner]++; if(/Audit/.test(st.winBy))stats.audit++; stats.turns.push(st.round);
  const w=H.hubWinners(st); if(w.filter(Boolean).length!==st.players.filter(p=>p.team===st.winner).length)throw 'winners';
}
console.log('sandi',{r:stats.r,b:stats.b,audit:stats.audit,errs:stats.errs});
// illegal checks
{const st={game:'sandi',players:Array.from({length:4},(_,i)=>({id:'u'+i}))};H.sandiStart(st);const t=st.turnTeam;const ket=st.players.findIndex(p=>p.team===t&&p.ketua);const gu=st.players.findIndex(p=>p.team===t&&!p.ketua);const opp=st.players.findIndex(p=>p.team!==t);
 const tryE=(f)=>{try{f();return 'OK';}catch(e){return e.message;}};
 const bw=H.termOf(st.words[3]).w;
 console.log('opp clue:',tryE(()=>H.sandiAct(st,opp,{type:'clue',word:'x',num:1})));
 console.log('guesser clue:',tryE(()=>H.sandiAct(st,gu,{type:'clue',word:'x',num:1})));
 console.log('board word clue:',tryE(()=>H.sandiAct(st,ket,{type:'clue',word:bw.split(/[\s/-]+/)[0],num:1})));
 console.log('two words:',tryE(()=>H.sandiAct(st,ket,{type:'clue',word:'dua kata',num:1})));
 console.log('guess before clue:',tryE(()=>H.sandiAct(st,gu,{type:'guess',i:0})));
 console.log('ok clue:',tryE(()=>H.sandiAct(st,ket,{type:'clue',word:'Rantai',num:2})));
 console.log('ketua guess:',tryE(()=>H.sandiAct(st,ket,{type:'guess',i:0})));
 console.log('endturn w/o guess:',tryE(()=>H.sandiAct(st,gu,{type:'endturn'})));}
// rapat random games
let R={I:0,O:0,errs:0,why:{}};
for(let g=0;g<600;g++){
  const n=5+g%6; const st={game:'rapat',special:g%3!==0,players:Array.from({length:n},(_,i)=>({id:'u'+i,nick:'P'+i}))};
  H.rapatStart(st); const roles=H.rapatRoles(st);
  if(roles.filter(r=>r==='O'||r==='D').length!=={5:2,6:2,7:3,8:3,9:3,10:4}[n])throw 'roles';
  let steps=0;
  while(st.status==='playing'&&steps++<2000){
    try{
      if(st.phase==='propose'){const m=st.missions[st.mi];const t=[...Array(n).keys()].sort(()=>Math.random()-.5).slice(0,m.size);H.rapatAct(st,st.leader,{type:'propose',team:t});}
      else if(st.phase==='vote'){for(let i=0;i<n;i++){if(st.phase!=='vote')break;H.rapatAct(st,i,{type:'vote',yes:Math.random()<0.6});}}
      else if(st.phase==='mission'){for(const i of st.team.slice()){if(st.phase!=='mission')break;const evil=roles[i]==='O'||roles[i]==='D';H.rapatAct(st,i,{type:'play',card:evil&&Math.random()<0.6?'f':'s'});}}
      else if(st.phase==='shoot'){const d=roles.indexOf('D');let t=Math.floor(Math.random()*n);if(t===d)t=(t+1)%n;H.rapatAct(st,d,{type:'shoot',target:t});}
    }catch(e){if(!(e instanceof GameErr))throw e;R.errs++;}
  }
  if(st.status!=='ended')throw 'rapat stuck '+st.phase;
  R[st.winner]++; R.why[st.winBy]=(R.why[st.winBy]||0)+1;
}
console.log('rapat',R);
{const st={game:'rapat',players:Array.from({length:7},(_,i)=>({id:'u'+i}))};H.rapatStart(st);const roles=H.rapatRoles(st);const good=roles.findIndex(r=>r==='I'||r==='A');
 const tryE=(f)=>{try{f();return 'OK';}catch(e){return e.message;}};
 console.log('wrong size:',tryE(()=>H.rapatAct(st,st.leader,{type:'propose',team:[0]})));
 console.log('non-leader:',tryE(()=>H.rapatAct(st,(st.leader+1)%7,{type:'propose',team:[0,1]})));
 const team=[good,(good+1)%7];H.rapatAct(st,st.leader,{type:'propose',team});for(let i=0;i<7;i++)H.rapatAct(st,i,{type:'vote',yes:true});
 console.log('phase after all yes:',st.phase,'good sabotage:',tryE(()=>H.rapatAct(st,good,{type:'play',card:'f'})),'outsider:',tryE(()=>H.rapatAct(st,team.includes(3)?4:3,{type:'play',card:'s'})));}
