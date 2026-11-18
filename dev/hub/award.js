/* ================= Animasi dapat pahlawan / bangsawan / kota ================= */
function awardKey(){return cur?(cur.local?'L'+(cur.lid||''):'G'+(cur.gid||'')):'';}
function awardWatch(st){
  if(!st||isHubGame(st)||!st.players)return;
  const key=awardKey(); if(!key)return;
  const snap=st.players.map(p=>({pat:[...(p.pat||[])],roy:[...(p.roy||[])],kota:p.kota||null}));
  ui.awSeen=ui.awSeen||{};
  const prev=ui.awSeen[key]; ui.awSeen[key]=snap;
  if(!prev||prev.length!==snap.length||cur.guided)return;
  const seat=actor(st);
  snap.forEach((s,i)=>{
    const who=i===seat?'Kamu':nm(st,i);
    s.pat.filter(id=>!prev[i].pat.includes(id)).forEach(id=>awardQueue({kind:'pat',id,i,who,me:i===seat}));
    s.roy.filter(id=>!prev[i].roy.includes(id)).forEach(id=>awardQueue({kind:'roy',id,i,who,me:i===seat}));
    if(s.kota&&!prev[i].kota)awardQueue({kind:'kota',id:s.kota,i,who,me:i===seat});
  });
}
function awardQueue(a){ui.awQ=ui.awQ||[];ui.awQ.push(a);if(!ui.awBusy)awardNext();}
function awardNext(){
  const a=(ui.awQ||[]).shift(); if(!a){ui.awBusy=false;return;}
  ui.awBusy=true; const st=cur&&cur.st;
  let card='',title='',sub='';
  if(a.kind==='pat'){const P=PAT[a.id];card=`<div class="awpat">${patronHTML(a.id)}</div>`;title=`${esc(a.who)} mendapat dukungan`;sub=`<b>${esc(P.name)}</b> · +3 poin`;}
  else if(a.kind==='roy'){card=`<div class="awpat awroy">${royalHTML(st,a.id)}</div>`;title=`${esc(a.who)} mendapat bangsawan`;sub=`+${ROYALS[a.id].pts} poin`;}
  else{const K=KOTA[a.id];card=`<div class="awkota"><div class="kart">${kotaArt(a.id)}<div class="kn">${esc(K.name)}</div></div></div>`;title=`${esc(a.who)} ${a.me?'merebut':'merebut'} Kota ${esc(K.name)}!`;sub=st&&st.status==='playing'?'Ini ronde terakhir!':'🏙️ Kota direbut';}
  const el=document.createElement('div'); el.className='awov '+(a.me?'me':''); el.setAttribute('role','status');
  el.innerHTML=`<div class="awrays"></div><div class="awbox"><div class="awcard">${card}</div><div class="awtxt"><div class="awt">${title}</div><div class="aws">${sub}</div></div></div>${a.me?'<div class="awconf">'+Array.from({length:14},(_,k)=>`<i style="--k:${k}"></i>`).join('')+'</div>':''}`;
  const done=()=>{if(el._d)return;el._d=1;el.classList.add('out');setTimeout(()=>{el.remove();awardNext();},350);};
  el.addEventListener('click',done); document.body.appendChild(el);
  try{if(a.me&&navigator.vibrate)navigator.vibrate([60,40,90]);}catch(e){}
  setTimeout(done,a.kind==='kota'?3400:2800);
}
