class GameErr extends Error{}
const fail=m=>{throw new GameErr(m);};
eval(require('fs').readFileSync(__dirname+'/jualan.js','utf8'));
function run(nT,lv,split){
  const st={nteams:nT,split,botLevel:lv,players:[{id:'h1',team:0},{id:'h2',team:0},{id:'h3',team:1}]};
  jyStart(st);
  // humans in teams 0/1 -> make them bots-equivalent: use all=true
  let g=0;
  while(st.status==='playing'&&g++<2000){const x=jyBotNext(st,true);if(!x)throw new Error('stuck '+st.phase+JSON.stringify(jyWaiting(st)));jyApplyBot(st,x);}
  return st;
}
let N=300,agg={};
for(const nT of [2,3,4])for(const lv of ['easy','normal']){
  let cash=[],wins={},reach=0,sells=0,errs=0;
  for(let i=0;i<N;i++){let st;try{st=run(nT,lv,i%2===0);}catch(e){errs++;if(errs<3)console.log(e.message);continue;}
    st.teams.forEach(T=>{cash.push(T.cash);if(T.cash>=5000)reach++;sells+=T.sold;});
  }
  cash.sort((a,b)=>a-b);
  console.log(`T=${nT} ${lv}: median kas ${cash[cash.length>>1]} min ${cash[0]} max ${cash[cash.length-1]} reach5jt ${(reach/cash.length*100).toFixed(0)}% avgSold ${(sells/cash.length).toFixed(1)} errs ${errs}`);
}
// sample log
const st=run(2,'normal',true); console.log(st.log.slice(0,14).map(l=>l.m).join('\n'));
