import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:90])
    s=s.replace(a,b)

# 1. Listener meja: sambung ulang otomatis, cek ulang sebelum menganggap meja hilang
rep("""  cur.unsub=db.doc('games/'+gid).onSnapshot(s=>{
    if(!cur||cur.gid!==gid)return;
    if(!s.exists){ if(!s.metadata.fromCache){ if(cur.st&&cur.st.status==='ended'){if(cur.unsub){cur.unsub();cur.unsub=null;}return;}
        toast(cur.st&&staleGame(cur.st,Date.now())?'Meja dihapus karena 2 jam tidak dimainkan':'Meja tidak ditemukan atau sudah dihapus');backToLobby();} return; }
    applyState(s.data());
  },()=>toast('Koneksi ke meja terputus — muat ulang halaman'));
  if(room)room.presence({uid:myId,g:gid}).catch(()=>{});
  render();
}""","""  cur.retry=0; watchTable(gid);
  if(room)room.presence({uid:myId,g:gid}).catch(()=>{});
  render();
}
function watchTable(gid){
  if(!cur||cur.gid!==gid||cur.local)return;
  if(cur.unsub){try{cur.unsub();}catch(e){}cur.unsub=null;}
  cur.unsub=db.doc('games/'+gid).onSnapshot(s=>{
    if(!cur||cur.gid!==gid)return;
    cur.retry=0; cur.lostAt=0;
    if(!s.exists){ if(!s.metadata.fromCache){ if(cur.st&&cur.st.status==='ended'){if(cur.unsub){cur.unsub();cur.unsub=null;}return;}
        confirmGone(gid);} return; }
    cur.missing=0; applyState(s.data());
  },()=>tableLost(gid));
}
async function confirmGone(gid){
  // jangan langsung keluar: cek ulang beberapa kali (sinyal HP sering putus sesaat)
  for(let i=0;i<3;i++){
    await sleep(1500*(i+1));
    if(!cur||cur.gid!==gid)return;
    try{const d=await db.doc('games/'+gid).get();if(d.exists){applyState(d.data());watchTable(gid);return;}}catch(e){}
  }
  if(!cur||cur.gid!==gid)return;
  toast(cur.st&&staleGame(cur.st,Date.now())?'Meja dihapus karena 2 jam tidak dimainkan':'Meja tidak ditemukan atau sudah dihapus');backToLobby();
}
function tableLost(gid){
  if(!cur||cur.gid!==gid)return;
  cur.unsub=null; cur.retry=(cur.retry||0)+1; if(!cur.lostAt)cur.lostAt=Date.now();
  if(cur.retry===1)toast('📶 Koneksi ke meja terputus — menyambung ulang…');
  setConnBadge(true);
  const wait=Math.min(20000,1500*Math.pow(1.6,cur.retry-1));
  clearTimeout(cur.retryT); cur.retryT=setTimeout(()=>{if(cur&&cur.gid===gid&&!cur.unsub)watchTable(gid);},wait);
}
function setConnBadge(on){
  let b=$('#connBadge');
  if(!on){if(b)b.remove();return;}
  if(!b){b=document.createElement('button');b.id='connBadge';b.className='btn sm';b.setAttribute('data-act','reconnect');b.textContent='📶 Menyambung ulang… ketuk untuk coba lagi';document.body.appendChild(b);}
}
function reconnectNow(){
  if(online!=='on'||!db)return;
  if(cur&&!cur.local&&cur.gid){const gid=cur.gid;cur.retry=0;
    db.doc('games/'+gid).get().then(d=>{if(cur&&cur.gid===gid&&d.exists)applyState(d.data());}).catch(()=>{});
    watchTable(gid);}
  if(!lobbyUnsub||ui.lobbyErr){try{if(lobbyUnsub)lobbyUnsub();}catch(e){}lobbyUnsub=null;subscribeLobby();}
  if(room)room.presence({uid:myId,g:cur&&!cur.local?cur.gid:null}).catch(()=>{});
}
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')reconnectNow();});
window.addEventListener('online',reconnectNow);""")

# badge hilang saat data masuk lagi
rep("""function applyState(data){
  if(!cur||cur.local||!data)return;""","""function applyState(data){
  if(!cur||cur.local||!data)return;
  setConnBadge(false);""")

# keluar meja: hentikan percobaan sambung ulang
rep("""  if(cur&&cur.unsub)cur.unsub();
  if(cur&&cur.botTimer)clearTimeout(cur.botTimer);
  cur=null; view='lobby'; ui.sel={}; closeModal();""","""  if(cur&&cur.unsub)cur.unsub();
  if(cur&&cur.botTimer)clearTimeout(cur.botTimer);
  if(cur&&cur.retryT)clearTimeout(cur.retryT); setConnBadge(false);
  cur=null; view='lobby'; ui.sel={}; closeModal();""")

# 2. Lobi: sambung ulang otomatis kalau listener putus
rep("""  },()=>{clearTimeout(timer);lobbyLoaded=true;if(view==='lobby')render();});
}""","""  },()=>{clearTimeout(timer);lobbyLoaded=true;lobbyUnsub=null;if(view==='lobby')render();
    ui.lobRetry=(ui.lobRetry||0)+1;setTimeout(()=>{if(!lobbyUnsub)subscribeLobby();},Math.min(20000,2000*ui.lobRetry));});
}""")

# 3. tombol sambung ulang
rep("""    case 'restartlocal':restartLocal();break;""","""    case 'restartlocal':restartLocal();break;
    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;""")

# 4. CSS
rep("</style>","""#connBadge{position:fixed;left:50%;top:10px;transform:translateX(-50%);z-index:60;background:#7a2a2a;color:#fff;border:1px solid #c66;box-shadow:0 4px 14px #0006}
</style>""")
open(p,'w').write(s)
print('ok')

# 5. Lobi: bedakan "gagal memuat" vs "belum ada meja", plus baris status akun untuk diagnosa
s=open(p).read()
rep("""        <div class="tables" id="tableList"></div>""","""        <div class="tables" id="tableList"></div>
        <div class="mute" id="acctLine" style="font-size:11.5px;margin-top:10px;opacity:.75"></div>""")
rep("""  if(online!=='on'){list.innerHTML='<div class="mute" style="font-size:14px">Daftar meja online akan muncul di sini.</div>';$('#lobbyStatus').textContent='';return;}""","""  {const al=$('#acctLine');if(al){const t=online==='on'?`Akun: ${ui.email||'(email tidak terbaca)'} · ID ${String(myId||'').slice(2,8)} · ${canWrite===false?'hanya bisa melihat':'bisa main'} · versi ${BUILD_TAG}`:(online==='off'?`Belum login / data online tidak tersedia · versi ${BUILD_TAG}`:'');if(al.textContent!==t)al.textContent=t;}}
  if(online!=='on'){list.innerHTML='<div class="mute" style="font-size:14px">Daftar meja online akan muncul di sini.</div>';$('#lobbyStatus').textContent='';return;}
  if(ui.lobbyErr&&!lobbyGames.length){$('#lobbyStatus').textContent='Gagal memuat';list.innerHTML=`<div class="gwarn" style="font-size:14px">⚠️ Daftar meja gagal dimuat (${esc(ui.lobbyErr)}). Biasanya karena sinyal atau akses akun.<div style="margin-top:8px"><button class="btn sm pri" data-act="reconnect">🔄 Coba lagi</button></div></div>`;return;}""")
rep("""    lobbyGames=s.docs.filter(d=>d.exists).map(d=>({...d.data(),_id:d.id}));""","""    lobbyGames=s.docs.filter(d=>d.exists).map(d=>({...d.data(),_id:d.id})); ui.lobbyErr=null; ui.lobRetry=0;""")
rep("""  },()=>{clearTimeout(timer);lobbyLoaded=true;lobbyUnsub=null;if(view==='lobby')render();""","""  },e=>{clearTimeout(timer);lobbyLoaded=true;lobbyUnsub=null;ui.lobbyErr=String((e&&(e.code||e.message))||'koneksi').slice(0,80);if(view==='lobby')render();""")
rep("const IDLE_MS=2*3600e3;","const IDLE_MS=2*3600e3;\nconst BUILD_TAG='11.12-g';")
open(p,'w').write(s)
print('ok2')

# 6. Banner di paling atas lobi: meja yang sedang kamu ikuti + jumlah meja aktif
s=open(p).read()
rep("""  {const gs=$('#gateSlot');if(gs){const h=accessGateHTML();""","""  {const gs=$('#gateSlot');if(gs){const h=accessGateHTML()+myTablesBanner();""")
rep("function accessGateHTML(){","""function myTablesBanner(){
  if(online!=='on'||!myId||EDITION==='latihan')return '';
  const now=Date.now(), act=lobbyGames.filter(g=>(g.status==='lobby'||g.status==='playing')&&!staleGame(g,now));
  const mine=act.filter(g=>(g.players||[]).some(p=>p.id===myId));
  const others=act.length-mine.length;
  if(!mine.length&&!others)return '';
  const row=g=>{const st={players:g.players||[]};const myturn=g.status==='playing'&&(g.players||[])[g.turn]&&g.players[g.turn].id===myId;
    return `<div class="trow" style="padding:8px 0"><div style="min-width:0"><b>${esc(g.name||'Meja')}</b> <span class="pill ${esc(g.status)}">${g.status==='lobby'?'Menunggu':'Berjalan'}</span>${myturn?' <span class="pill" style="background:#b98f2c;color:#1b1406">Giliranmu!</span>':''}
      <div class="mute" style="font-size:12.5px">${(g.players||[]).map((p,i)=>(p.bot?'🤖':'')+esc(nm(st,i))).join(', ')}</div></div>
      <button class="btn sm pri" data-act="open" data-g="${esc(g._id)}">▶ Lanjutkan</button></div>`;};
  return `<section class="panel" style="border:1.5px solid #b98f2c">${mine.length?`<h2 style="font-size:18px;margin:0 0 4px">🎲 Meja kamu</h2>${mine.map(row).join('')}`:''}
    ${others?`<button class="btn sm" style="margin-top:${mine.length?8:0}px" data-act="gotables">👀 Lihat ${others} meja lain yang aktif ↓</button>`:''}</section>`;
}
function accessGateHTML(){""")
rep("""    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;""","""    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;
    case 'gotables':{const t=$('#tableList');if(t)t.scrollIntoView({behavior:'smooth',block:'start'});break;}""")
open(p,'w').write(s)
print('ok3')
s=open(p).read()
rep("if(ui.gateH!==h){ui.gateH=h;gs.innerHTML=h;}","if(gs._h!==h){gs._h=h;gs.innerHTML=h;}")
open(p,'w').write(s)

# 7. Hapus meja buatan sendiri langsung dari lobi
s=open(p).read()
DEL="""${(g.host===myId||isOwnerFlag)&&canWrite!==false?`<button class="btn sm danger" data-act="lobdel" data-g="${esc(g._id)}" data-n="${esc(g.name||'Meja')}" aria-label="Hapus meja ${esc(g.name||'')}" title="Hapus meja">🗑</button>`:''}"""
rep("""      <button class="btn sm ${seated?'ok':''}" data-act="open" data-g="${esc(g._id)}">""","      "+DEL+"""<button class="btn sm ${seated?'ok':''}" data-act="open" data-g="${esc(g._id)}">""")
rep("""      <button class="btn sm pri" data-act="open" data-g="${esc(g._id)}">▶ Lanjutkan</button></div>`;};""","""      <span class="row" style="gap:6px;flex-wrap:nowrap">"""+DEL+"""<button class="btn sm pri" data-act="open" data-g="${esc(g._id)}">▶ Lanjutkan</button></span></div>`;};""")
rep("""    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;""","""    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;
    case 'lobdel':{const g=lobbyGames.find(x=>x._id===el.dataset.g);ui.lobDel=el.dataset.g;openModal(`<h3>🗑 Hapus “${esc(el.dataset.n)}”?</h3><p class="mute" style="font-size:14px">${g&&g.status==='playing'?'Game di meja ini <b>sedang berjalan</b>. ':''}Meja dihapus untuk semua pemain dan tidak bisa dikembalikan.</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn danger" data-act="lobdelok">Hapus meja</button></div>`);break;}
    case 'lobdelok':{closeModal();const id=ui.lobDel;ui.lobDel=null;if(!id)break;try{await db.doc('games/'+id).delete();lobbyGames=lobbyGames.filter(x=>x._id!==id);toast('🗑 Meja dihapus');render();}catch(err){toast('Gagal menghapus meja');}break;}""")
open(p,'w').write(s)
