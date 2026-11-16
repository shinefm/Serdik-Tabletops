class GameErr extends Error{}
const fail=m=>{throw new GameErr(m);};
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const fs=require('fs');eval(fs.readFileSync(__dirname+'/pemukim.js','utf8')+'\n'+fs.readFileSync(__dirname+'/pemukim_bot.js','utf8')+'\nglobalThis.H={PM_G,pmStart,pmAct,pmBotMove,pmBotRespond,pmVP,pmTotal,pmLongest,pmPieces,PM_RES};');
console.log('geom',H.PM_G.hexes.length,H.PM_G.verts.length,H.PM_G.edges.length,'coast',H.PM_G.coast.length);
function play(levels,maxSteps=6000){
  const n=levels.length, st={game:'pemukim',players:levels.map((l,i)=>({id:'b'+i,nick:'B'+i,bot:true,level:l}))};
  H.pmStart(st); let steps=0, errs=0;
  while(st.status==='playing'&&steps++<maxSteps){
    const who=st.phase==='discard'?Number(Object.keys(st.disc)[0]):st.turn;
    const mv=H.pmBotMove(st,who,levels[who]);
    try{H.pmAct(st,who,mv);}catch(e){if(!(e instanceof GameErr))throw e;errs++;if(errs<4)console.log('ERR',st.phase,JSON.stringify(mv),e.message);try{H.pmAct(st,who,{type:'end'});}catch(e2){if(st.phase==='robber')H.pmAct(st,who,{type:'robber',h:(st.board.robber+1)%19});}}
    // conservation
    const tot=r=>st.bank[r]+st.players.reduce((s,p)=>s+p.res[r],0);
    if(H.PM_RES.some(r=>tot(r)!==19))throw 'conservation '+JSON.stringify(st.bank);
  }
  return {st,steps,errs};
}
const N=+(process.argv[2]||200);
for(const cfg of [['normal','normal','normal','normal'],['hard','normal','normal','normal'],['hard','easy','easy'],['normal','easy','easy','easy'],['hard','hard','normal']]){
  const wins=Array(cfg.length).fill(0);let rounds=0,stuck=0,errs=0,lr=0,la=0;
  for(let g=0;g<N;g++){const r=play(cfg);errs+=r.errs;if(r.st.status!=='ended'){stuck++;continue;}wins[r.st.winner]++;rounds+=r.st.round;if(r.st.longest!=null)lr++;if(r.st.largest!=null)la++;}
  console.log(cfg.join('/'),'wins',wins,'avgRounds',(rounds/(N-stuck)).toFixed(1),'stuck',stuck,'errs',errs,'LR%',(lr/N*100|0),'LA%',(la/N*100|0));
}
