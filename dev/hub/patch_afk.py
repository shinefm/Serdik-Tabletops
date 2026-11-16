import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:90])
    s=s.replace(a,b)

# 1. Autopilot: pemain berstatus auto dimainkan seperti bot
rep("""  const p=st.players[st.turn]; if(!p||!p.bot){return;}
  const key=cur.gid+':'+st.v; if(ui.obKey===key)return;""","""  const p=st.players[st.turn]; if(!p||!(p.bot||p.auto)){return;}
  const key=cur.gid+':'+st.v; if(ui.obKey===key)return;""")
rep("""  if(st.phase==='discard'){const j=Object.keys(st.disc||{}).map(Number).find(j=>st.players[j].bot);return j!=null?{j,mv:pmBotDiscard(st,j)}:null;}
  if(st.offer){const j=st.players.findIndex((p,j)=>p.bot&&j!==st.offer.from&&st.offer.resp[j]==null);if(j>=0)return {j,mv:pmBotRespond(st,j,st.players[j].level||'normal')};}
  const t=st.turn;if(st.players[t].bot){""","""  const AB=q=>q&&(q.bot||(!cur||!cur.local)&&q.auto);
  if(st.phase==='discard'){const j=Object.keys(st.disc||{}).map(Number).find(j=>AB(st.players[j]));return j!=null?{j,mv:pmBotDiscard(st,j)}:null;}
  if(st.offer){const j=st.players.findIndex((p,j)=>AB(p)&&j!==st.offer.from&&st.offer.resp[j]==null);if(j>=0)return {j,mv:pmBotRespond(st,j,st.players[j].level||'normal')};}
  const t=st.turn;if(AB(st.players[t])){""")

# 2. Mesin AFK + panel
rep("function myRank(st){","""/* ================= FAILSAFE: LAPOR AFK =================
   Lapor manual lewat kotak pemain. Hitung mundur baru mulai setelah SEMUA pemain lain
   (selain bot & yang dilaporkan) ikut melapor. Tiap pemain hanya bisa MEMULAI laporan sekali per game. */
const AFK_GATHER=5*60e3, AFK_COUNT=60e3, AFK_SOLO=120e3;
function afkGameOk(st){return st&&!cur.local&&st.status==='playing'&&(!st.game||st.game==='pemukim');}
function afkHumans(st){return st.players.map((q,i)=>i).filter(i=>!st.players[i].bot&&!st.players[i].auto);}
function afkVoters(st,t){return afkHumans(st).filter(i=>i!==t);}
function afkCanTarget(st,me,t){const q=st.players[t];return q&&t!==me&&!q.bot&&!q.auto;}
function afkReport(s,me,t){
  if(me<0||s.players[me].bot||s.players[me].auto)fail('Kamu tidak bisa melapor');
  if(!afkCanTarget(s,me,t))fail('Pemain ini tidak bisa dilaporkan');
  const uid=s.players[me].id, a=s.afk;
  if(a&&a.tid!==s.players[t].id)fail('Masih ada laporan AFK untuk '+nm(s,s.players.findIndex(q=>q.id===a.tid))+' yang berjalan');
  if(a){ if(a.stage!=='vote')fail('Hitung mundur sudah berjalan'); if(!a.yes.includes(uid))a.yes.push(uid); }
  else{ s.afkUsed=s.afkUsed||{}; if(s.afkUsed[uid])fail('Kamu sudah memakai jatah memulai laporan AFK di game ini');
    if(afkVoters(s,t).length<=1){const pend=s.game==='pemukim'?pmPending(s):[s.turn];
      if(!pend.includes(t)||Date.now()-(s.turnAt||0)<AFK_SOLO)fail('Di game 2 orang, laporan baru bisa dikirim kalau dia sedang dapat giliran dan belum jalan selama 2 menit');}
    s.afkUsed[uid]=1; s.afk={t,tid:s.players[t].id,by:uid,yes:[uid],at:Date.now(),stage:'vote',until:Date.now()+AFK_GATHER}; }
  const A=s.afk; if(afkVoters(s,t).every(i=>A.yes.includes(s.players[i].id))){A.stage='count';A.until=Date.now()+AFK_COUNT;}
}
function afkCancel(s,me){const a=s.afk;if(!a)throw NOOP;if(a.by!==s.players[me].id)fail('Hanya pelapor pertama yang bisa membatalkan');s.afk=null;s.afkNote={m:nm(s,me)+' membatalkan laporan AFK',at:Date.now()};}
function afkHere(s,me){const uid=s.players[me].id;if(s.afk&&s.afk.tid===uid){s.afk=null;s.afkNote={m:nm(s,me)+' kembali, laporan AFK dibatalkan',at:Date.now()};}if(s.players[me].auto){delete s.players[me].auto;s.afkNote={m:nm(s,me)+' kembali bermain sendiri (autopilot dimatikan)',at:Date.now()};}}
function afkResolve(s){
  const a=s.afk; if(!a)throw NOOP;
  const t=s.players.findIndex(q=>q.id===a.tid);
  if(t<0||s.status!=='playing'||s.players[t].auto){s.afk=null;return;}
  if(Date.now()<a.until)throw NOOP;
  if(a.stage==='vote'){s.afk=null;s.afkNote={m:'Laporan AFK kedaluwarsa (tidak semua pemain ikut melapor)',at:Date.now()};return;}
  s.afkNote={m:'🤖 '+nm(s,t)+' tidak merespons — kini dimainkan autopilot',at:Date.now()}; s.players[t].auto=true; s.afk=null;
}
function afkCommit(fn,okMsg){commitOnline(fn).then(()=>{if(okMsg)toast(okMsg);}).catch(e=>{if(!e||!e.noop)toast((e&&e.message)||'Gagal, coba lagi');});}
function afkPlAttr(st,i){if(!cur||cur.local||online!=='on'||canWrite===false||!st||!afkGameOk(st))return '';const me=meIdx(st);if(me<0||!afkCanTarget(st,me,i))return '';return ' data-act="afkpl" data-i="'+i+'" title="Ketuk untuk melaporkan AFK"';}
function afkPlModal(i){
  const st=cur.st, me=meIdx(st), a=st.afk, uid=st.players[me]&&st.players[me].id; if(!afkCanTarget(st,me,i))return;
  const name=esc(nm(st,i)), vs=afkVoters(st,i);
  let body, btn='';
  if(a&&a.tid!==st.players[i].id){body=`Masih ada laporan AFK untuk <b>${esc(nm(st,st.players.findIndex(q=>q.id===a.tid)))}</b>. Tunggu sampai selesai dulu.`;}
  else if(a&&a.stage==='count'){body=`Semua sudah melapor. <b>${name}</b> sedang diberi waktu 1 menit untuk merespons.`;}
  else if(a&&a.yes.includes(uid)){body=`Kamu sudah melapor. Menunggu pemain lain ikut melapor (${a.yes.length}/${vs.length}).`;}
  else if(a){body=`<b>${esc(nm(st,st.players.findIndex(q=>q.id===a.by)))}</b> sudah melaporkan <b>${name}</b> AFK (${a.yes.length}/${vs.length}). Ikut melapor?`;btn='<button class="btn pri" data-act="afkgo" data-i="'+i+'">🚨 Ikut lapor</button>';}
  else if(st.afkUsed&&st.afkUsed[uid]){body='Kamu sudah memakai jatah memulai laporan AFK di game ini. Kamu masih bisa <b>ikut melapor</b> kalau pemain lain yang memulai.';}
  else{body=`Laporkan <b>${name}</b> tidak aktif (AFK)?`;btn='<button class="btn pri" data-act="afkgo" data-i="'+i+'">🚨 Laporkan AFK</button>';}
  openModal(`<h3>🚨 ${name}</h3><p style="font-size:14.5px;margin:0 0 8px">${body}</p>
    <div class="mute" style="font-size:12.5px;line-height:1.5">Cara kerja: semua pemain lain (selain bot) harus ikut melapor. Setelah semua melapor, ${name} punya <b>1 menit</b> untuk merespons. Kalau tidak, gilirannya dimainkan <b>autopilot 🤖</b> sampai dia kembali dan menekan “Ambil alih”. Poinnya tetap miliknya. Tiap pemain hanya bisa <b>memulai</b> laporan sekali per game.${vs.length<=1?' <br>Karena pemainnya cuma 2 orang, laporan baru bisa dikirim kalau dia sedang dapat giliran dan belum jalan selama <b>2 menit</b>; hitung mundur langsung mulai.':''}</div>
    <div class="mbtns"><button class="btn" data-act="close">Tutup</button>${btn}</div>`);
}
function afkBarHTML(st){
  const me=meIdx(st); if(me<0)return '';
  const a=st.afk, P=st.players[me];
  if(P.auto)return `<div class="afkbar mine"><span>🤖 <b>Autopilot</b> sedang memainkan giliranmu.</span><button class="btn sm pri" data-act="afkhere">🙋 Ambil alih</button></div>`;
  if(!a)return '';
  const t=st.players.findIndex(q=>q.id===a.tid), left=Math.max(0,Math.ceil((a.until-Date.now())/1000)), vs=afkVoters(st,t), n=vs.filter(i=>a.yes.includes(st.players[i].id)).length;
  if(t===me)return a.stage==='count'?`<div class="afkbar alarm"><span>🚨 <b>Kamu dilaporkan AFK!</b> Dalam <b data-afkleft>${left}</b> detik giliranmu dimainkan autopilot.</span><button class="btn pri" data-act="afkhere">🙋 Saya di sini!</button></div>`
    :`<div class="afkbar top"><span>⚠️ Ada yang melaporkanmu AFK (${n}/${vs.length}).</span><button class="btn sm pri" data-act="afkhere">🙋 Saya di sini</button></div>`;
  if(a.stage==='vote'){const voted=a.yes.includes(P.id);
    return `<div class="afkbar top"><span>🚨 <b>${esc(nm(st,t))}</b> dilaporkan AFK · ${n}/${vs.length} pemain melapor</span>${voted?(a.by===P.id?'<button class="btn sm" data-act="afkcancel">Batalkan</button>':''):`<button class="btn sm pri" data-act="afkgo" data-i="${t}">🚨 Ikut lapor</button>`}</div>`;}
  return `<div class="afkbar top"><span>⏳ <b>${esc(nm(st,t))}</b> punya <b data-afkleft>${left}</b> detik untuk merespons, lalu dimainkan autopilot 🤖</span></div>`;
}
function afkTick(){
  let bar=$('#afkBar');
  const st=cur&&cur.st;
  if(view!=='table'||!cur||!st||!afkGameOk(st)||online!=='on'){if(bar)bar.remove();return;}
  if(st.afkNote&&st.afkNote.at!==ui.afkNoteAt){ui.afkNoteAt=st.afkNote.at;if(Date.now()-st.afkNote.at<15000)toast(st.afkNote.m);}
  const h=afkBarHTML(st);
  if(!bar){bar=document.createElement('div');bar.id='afkBar';document.body.appendChild(bar);}
  const key=h.replace(/<[^>]*data-afkleft[^>]*>\\d+</g,'');
  if(bar._k!==key){bar._k=key;bar.innerHTML=h;}else{const l=bar.querySelector('[data-afkleft]');if(l&&st.afk)l.textContent=Math.max(0,Math.ceil((st.afk.until-Date.now())/1000));}
  const a=st.afk, me=meIdx(st);
  if(a&&me>=0&&canWrite!==false&&!ui.afkBusy){
    const t=st.players.findIndex(q=>q.id===a.tid), gone=t<0||st.players[t].auto;
    const late=Date.now()-a.until;
    if(gone||late>(me===t?0:600+me*500)){ui.afkBusy=true;const at=a.at;
      commitOnline(s=>{if(!s.afk||s.afk.at!==at)throw NOOP;afkResolve(s);}).catch(()=>{}).finally(()=>{ui.afkBusy=false;});}
  }
}
setInterval(afkTick,500);
function myRank(st){""")

# 3. Klik
rep("""    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;""","""    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;
    case 'afkpl':afkPlModal(+el.dataset.i);break;
    case 'afkgo':{closeModal();const i=+el.dataset.i;afkCommit(s=>afkReport(s,meIdx(s),i),'🚨 Laporan AFK tercatat');break;}
    case 'afkcancel':afkCommit(s=>afkCancel(s,meIdx(s)));break;
    case 'afkhere':afkCommit(s=>afkHere(s,meIdx(s)),'👍 Kamu kembali memegang kendali');break;""")

# 4. Kotak pemain bisa diketuk; langkah sendiri membatalkan laporan atas dirimu
rep("""    return `<div class="pl ${own?'mine-pl':''} ${st.status==='playing'&&st.turn===i?'turn':''}">""","""    return `<div class="pl ${own?'mine-pl':''} ${st.status==='playing'&&st.turn===i?'turn':''} ${st.afk&&st.afk.tid===p.id?'afk-rep':''}"${afkPlAttr(st,i)}>""")
rep("""    return `<div class="pmpl ${i===st.turn&&!ended?'turn':''} ${i===me?'me':''}">""","""    return `<div class="pmpl ${i===st.turn&&!ended?'turn':''} ${i===me?'me':''} ${st.afk&&st.afk.tid===p.id?'afk-rep':''}"${afkPlAttr(st,i)}>""")
rep("""        doMove(st,pi,mv);
      });""","""        doMove(st,pi,mv);
        if(st.afk&&st.afk.tid===myId&&!mv.force)st.afk=null;
      });""")
rep("""  try{await commitOnline(s=>{const k=meIdx(s);if(k<0)fail('Kamu bukan pemain meja ini');pmAct(s,k,mv);});ui.pmMode=null;}""","""  try{await commitOnline(s=>{const k=meIdx(s);if(k<0)fail('Kamu bukan pemain meja ini');pmAct(s,k,mv);if(s.afk&&s.afk.tid===myId)s.afk=null;});ui.pmMode=null;}""")

rep("function nm(st,i){const p=st.players[i];if(!p)return '?';return p.nick||NAMES[p.id]||('Pemain '+(i+1));}",
    "function nm(st,i){const p=st.players[i];if(!p)return '?';return (p.nick||NAMES[p.id]||('Pemain '+(i+1)))+(p.auto&&!p.bot?' 🤖':'');}")

# 5. CSS
rep("#connBadge{","""#afkBar{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:55;width:min(560px,calc(100vw - 20px));pointer-events:none}
#afkBar:has(.top){bottom:auto;top:8px}
.pl[data-act=afkpl],.pmpl[data-act=afkpl]{cursor:pointer}
.pl.afk-rep,.pmpl.afk-rep{outline:2px dashed #ff8a8a;outline-offset:2px}
.afkbar.top{font-size:13px;padding:7px 10px}
#afkBar:empty{display:none}
.afkbar{pointer-events:auto;display:flex;align-items:center;gap:8px 10px;flex-wrap:wrap;justify-content:center;text-align:center;background:#2a2346;color:#f3eefe;border:1.5px solid #b98f2c;border-radius:14px;padding:10px 12px;font-size:14px;box-shadow:0 8px 24px #0007}
.afkbar.soft{background:#221d3a;border-color:#5b5280}
.afkbar.mine{background:#4a3d1c;color:#fbecc4}
.afkbar.alarm{background:#7a2230;border-color:#ff8a8a;font-size:16px;animation:afkp 1s ease-in-out infinite alternate}
@keyframes afkp{from{box-shadow:0 0 0 0 #ff6b6b88}to{box-shadow:0 0 0 10px #ff6b6b00}}
body.light .afkbar{background:#fff;color:#2a2346}body.light .afkbar.alarm{background:#ffe1e1;color:#5a1020}body.light .afkbar.mine{background:#fff4d6;color:#4a3d1c}
#connBadge{""")
open(p,'w').write(s)
print('ok')
s=open(p).read()
rep("""    return `<div class="m-opp ${st.status==='playing'&&st.turn===i?'turn':''}">""","""    return `<div class="m-opp ${st.status==='playing'&&st.turn===i?'turn':''} ${st.afk&&st.afk.tid===p.id?'afk-rep':''}"${afkPlAttr(st,i)}>""")
s=s.replace(".pl[data-act=afkpl],.pmpl[data-act=afkpl]{cursor:pointer}",".pl[data-act=afkpl],.pmpl[data-act=afkpl],.m-opp[data-act=afkpl]{cursor:pointer}\n.m-opp.afk-rep{outline:2px dashed #ff8a8a;outline-offset:1px}")
open(p,'w').write(s)
