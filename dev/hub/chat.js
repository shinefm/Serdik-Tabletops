/* ---------- Chat meja online ----------
   Tab "Chat" di samping "Catatan" pada setiap game online.
   Pesan lewat Realtime Database chat/<gid> selama game berlangsung saja: tidak masuk Firestore,
   riwayat, atau replay, dan seluruh chat dihapus begitu game selesai atau meja dihapus. */
const CH={gid:null,api:null,unsub:null,msgs:[],seen:{},el:null,unread:0,wiped:false,last:0,member:false,tok:0,at:0,noApi:false};
ui.logTab=ui.logTab||'log';
function chatOn(){return !!(CH.gid&&cur&&!cur.local&&cur.gid===CH.gid);}
function chatWant(){return (!CH.noApi&&view==='table'&&online==='on'&&cur&&!cur.local&&cur.gid&&cur.st&&cur.st.status&&cur.st.status!=='lobby')?cur.gid:null;}
function chatCls(){return chatOn()?' haschat':'';}
function logSum(title){
  if(!chatOn())return title;
  const t=ui.logTab==='chat'?'chat':'log';
  return `<span class="lgtabs" role="tablist"><button type="button" role="tab" data-lt="log" class="${t==='log'?'on':''}" aria-selected="${t==='log'}">${title}</button><button type="button" role="tab" data-lt="chat" class="${t==='chat'?'on':''}" aria-selected="${t==='chat'}">💬 Chat<i class="cbadge"${CH.unread?'':' hidden'}>${CH.unread}</i></button></span>`;
}
function logPanes(logs){
  if(!chatOn())return logs;
  const t=ui.logTab==='chat'?'chat':'log';
  return `<div class="lgpane lglog"${t==='log'?'':' hidden'}>${logs}</div><div class="lgpane" id="chatSlot"${t==='chat'?'':' hidden'}></div>`;
}
async function chatApi(){
  if(CH.api)return CH.api;
  try{const a=await claude.use('chat');if(a&&a.send)CH.api=a;}catch(e){}
  return CH.api;
}
function chatStop(){
  if(CH.unsub){try{CH.unsub();}catch(e){}}
  CH.unsub=null;CH.gid=null;CH.msgs=[];CH.seen={};CH.unread=0;CH.wiped=false;CH.member=false;CH.tok++;
  if(CH.el){CH.el.remove();CH.el=null;}
}
function chatStart(gid){
  chatStop(); CH.gid=gid; CH.at=Date.now(); const tok=CH.tok;
  chatBuild();
  chatApi().then(api=>{
    if(!api||tok!==CH.tok){if(!api&&tok===CH.tok){CH.noApi=true;chatStop();render();}return;}
    const st=cur&&cur.st;
    if(st&&meIdx(st)>=0&&canWrite!==false){CH.member=true;api.join(gid).catch(()=>{});}
    CH.unsub=api.on(gid,m=>{if(tok!==CH.tok)return;chatAdd(m);});
    chatMaybeWipe();
  });
}
/* game selesai: chat dihapus dari server, layar tetap menampilkan pesan sampai keluar meja */
function chatMaybeWipe(){
  if(!CH.gid||CH.wiped||!cur||!cur.st||cur.st.status!=='ended')return;
  CH.wiped=true; chatInputState();
  if(CH.member&&CH.api)CH.api.clear(CH.gid).catch(()=>{});
}
function chatBuild(){
  const el=document.createElement('div'); el.className='chatbox';
  el.innerHTML=`<div class="chatlist" role="log" aria-live="polite" aria-label="Pesan chat"><div class="chatempty">Belum ada pesan. Sapa teman semejamu 👋</div></div>
    <form class="chatin" autocomplete="off"><input type="text" maxlength="200" placeholder="Tulis pesan…" aria-label="Tulis pesan chat" enterkeyhint="send"><button class="btn pri sm" type="submit">Kirim</button></form>
    <div class="chatnote">Chat hanya selama game berjalan dan dihapus otomatis saat game selesai.</div>`;
  el.querySelector('form').addEventListener('submit',e=>{e.preventDefault();chatSend();});
  CH.el=el; chatInputState();
}
function chatInputState(){
  if(!CH.el)return;
  const inp=CH.el.querySelector('input'), btn=CH.el.querySelector('button'), note=CH.el.querySelector('.chatnote');
  const st=cur&&cur.st, seated=!!(st&&meIdx(st)>=0&&canWrite!==false);
  const off=CH.wiped||!seated;
  inp.disabled=off; btn.disabled=off;
  inp.placeholder=CH.wiped?'Game selesai — chat ditutup':!seated?'Hanya pemain di meja ini yang bisa mengirim pesan':'Tulis pesan…';
  note.textContent=CH.wiped?'Game selesai. Chat sudah dihapus dari server dan hilang saat kamu keluar dari meja.':'Chat hanya selama game berjalan dan dihapus otomatis saat game selesai.';
}
function chatTime(ts){try{const d=new Date(ts);return String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');}catch(e){return '';}}
function chatAdd(m){
  if(!m||!m.id||CH.seen[m.id]||typeof m.t!=='string')return;
  CH.seen[m.id]=1; CH.msgs.push(m); if(CH.msgs.length>80)CH.msgs.shift();
  if(!CH.el)return;
  const list=CH.el.querySelector('.chatlist'), atEnd=list.scrollHeight-list.scrollTop-list.clientHeight<40;
  const e=list.querySelector('.chatempty'); if(e)e.remove();
  const mine=m.u===myId, row=document.createElement('div');
  row.className='cmsg'+(mine?' me':'');
  row.innerHTML=`<span class="cn">${mine?'Kamu':esc(m.n||'Pemain')}</span><span class="ct">${esc(m.t)}</span><span class="cw">${chatTime(m.ts)}</span>`;
  list.appendChild(row);
  while(list.children.length>80)list.firstChild.remove();
  if(atEnd||mine)list.scrollTop=list.scrollHeight;
  if(!mine&&!chatVisible()&&!(m.ts&&m.ts<CH.at-3000)){CH.unread++;chatBadge();toast('💬 '+(m.n||'Pemain')+': '+m.t.slice(0,60));}
}
function chatVisible(){
  const slot=document.getElementById('chatSlot');
  if(!slot||slot.hidden)return false;
  const d=slot.closest('details'); return !d||d.open;
}
function chatBadge(){
  document.querySelectorAll('.lgtabs .cbadge').forEach(b=>{b.textContent=CH.unread;b.hidden=!CH.unread;});
}
async function chatSend(){
  if(!CH.el||!chatOn()||CH.wiped)return;
  const inp=CH.el.querySelector('input'), t=inp.value.replace(/\s+/g,' ').trim().slice(0,200);
  if(!t)return;
  const now=Date.now(); if(now-CH.last<700){toast('Pelan-pelan ya 🙂');return;}
  const st=cur.st, me=meIdx(st); if(me<0||canWrite===false)return;
  CH.last=now; inp.value='';
  const name=String(nm(st,me)).replace(/ 🤖$/,'').slice(0,40)||'Pemain';
  try{const api=await chatApi();if(!api)throw 0;if(!CH.member){CH.member=true;await api.join(CH.gid).catch(()=>{});}await api.send(CH.gid,name,t);}
  catch(e){toast('Pesan gagal terkirim');if(!inp.value)inp.value=t;}
}
/* setiap render: elemen chat yang sama dipindah ke slot baru supaya ketikan & fokus tidak hilang */
function chatMount(){
  if(!CH.el)return;
  const slot=document.getElementById('chatSlot');
  if(!slot){if(CH.el.parentNode)CH.el.remove();return;}
  if(CH.el.parentNode!==slot){slot.appendChild(CH.el);const l=CH.el.querySelector('.chatlist');l.scrollTop=l.scrollHeight;}
  chatInputState();
  if(chatVisible()&&CH.unread){CH.unread=0;chatBadge();}
}
function chatSwitch(det,t){
  ui.logTab=t;
  det.querySelectorAll('.lgtabs [data-lt]').forEach(b=>{const on=b.dataset.lt===t;b.classList.toggle('on',on);b.setAttribute('aria-selected',on);});
  det.querySelectorAll('.lgpane').forEach(p=>{p.hidden=(p.id==='chatSlot')!==(t==='chat');});
  if(t==='chat'){CH.unread=0;chatBadge();const l=CH.el&&CH.el.querySelector('.chatlist');if(l)l.scrollTop=l.scrollHeight;}
}
document.addEventListener('click',e=>{
  const b=e.target.closest&&e.target.closest('.lgtabs [data-lt]'); if(!b)return;
  e.preventDefault(); e.stopPropagation();
  const det=b.closest('details'), t=b.dataset.lt;
  if(det&&det.open&&ui.logTab===t){det.open=false;ui.logOpen=false;return;}
  if(det&&!det.open){det.open=true;ui.logOpen=true;}
  chatSwitch(det||document,t);
},true);
const _renderNoChat=render;
render=function(){
  const want=chatWant();
  if(want!==CH.gid){if(want)chatStart(want);else chatStop();}
  const inp=CH.el&&CH.el.querySelector('input'), foc=!!(inp&&document.activeElement===inp);
  let a=0,b=0; if(foc){a=inp.selectionStart;b=inp.selectionEnd;}
  _renderNoChat();
  chatMount();
  chatMaybeWipe();
  if(foc&&inp.isConnected){inp.focus({preventScroll:true});try{inp.setSelectionRange(a,b);}catch(e){}}
};
