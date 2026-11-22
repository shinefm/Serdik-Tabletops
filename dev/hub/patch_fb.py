"""Bangun edisi Firebase dari saudagar-permata.html (edisi liga) -> fbapp/out/index.html"""
import sys,re,os,shutil
DEV=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=DEV+'/saudagar-permata.html'; OUT=os.environ.get('OUT') or os.path.dirname(DEV)
s=open(SRC).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:100])
    s=s.replace(a,b)

# 1. muat Firebase SDK + konfigurasi + adaptor sebelum skrip game
first=s.index('<script>')
s=s[:first]+'''<script src="fb/firebase-app-compat.js"></script>
<script src="fb/firebase-auth-compat.js"></script>
<script src="fb/firebase-firestore-compat.js"></script>
<script src="fb/firebase-database-compat.js"></script>
<script src="firebase-config.js"></script>
<script src="shim.js"></script>
'''+s[first:]

# 2. link halaman = alamat situs sendiri
rep("const ARTIFACT_URL='https://claude.ai/artifact/JGRDMJqpVSu1bvSWXVa2eG';","const ARTIFACT_URL=location.origin+location.pathname;")
rep("const LEAGUE_URL='https://claude.ai/artifact/JGRDMJqpVSu1bvSWXVa2eG', PRACTICE_URL='https://claude.ai/artifact/7P5Jvn3qiMsHsC9c7qvtoh';","const LEAGUE_URL=location.origin+location.pathname, PRACTICE_URL=location.origin+location.pathname;")
rep("<title>Serdik Tabletop — P3MDI</title>","<title>Serdik Tabletop</title>")
rep("const BUILD_TAG='11.12-g';","const BUILD_TAG='fb-18';")

# 3. teks yang menyebut login Claude / undangan
rep("Mode online tidak tersedia di tampilan ini (perlu masuk ke akun Claude dan membuka halaman ini dari tautan yang dibagikan). Kamu tetap bisa <b>main lawan bot</b>.","Masuk dengan akun Google untuk main online bareng teman. Tanpa login kamu tetap bisa <b>main lawan bot</b>.")
rep("(buka di Chrome/Safari & login ke Claude dulu ya)","(buka di Chrome/Safari, lalu masuk dengan Google)",2)
rep("ℹ️ Teman harus membuka link di Chrome/Safari, <b>login ke Claude</b>, dan emailnya <b>sudah kamu undang</b> lewat Share di claude.ai (akses jangan “Viewer”).","ℹ️ Teman cukup membuka link di Chrome/Safari lalu <b>masuk dengan Google</b>. Tidak perlu diundang.")
rep("'Untuk punya profil (terikat ke email akun Claude kamu), main online, dan masuk peringkat, minta pemilik halaman <b>mengundang emailmu sebagai Editor</b>.'","'Untuk punya profil, main online, dan masuk peringkat, <b>masuk dengan akun Google</b>. Gratis dan tanpa undangan.'")
rep("🔒 Terikat ke akun ${ui.email?`<b>${esc(ui.email)}</b>`:'Claude kamu'}</div>","🔒 Masuk dengan Google${ui.email?` · <b>${esc(ui.email)}</b>`:''} · <button class=\"btn sm\" data-act=\"fblogout\" style=\"padding:2px 8px\">Keluar akun</button></div>")
rep("{const al=$('#acctLine');if(al){const t=online==='on'?`Akun: ${ui.email||'(email tidak terbaca)'} · ID ${String(myId||'').slice(2,8)} · ${canWrite===false?'hanya bisa melihat':'bisa main'} · versi ${BUILD_TAG}`",
    "{const al=$('#acctLine');if(al){const t=online==='on'?`Akun: ${ui.email||'(email tidak terbaca)'} · ID ${String(myId||'')} · versi ${BUILD_TAG}`")

# 4. jangan pakai ringkasan lobi sebagai state meja
rep("cur={gid,local:false,st:seed||(fromLobby?stripId(fromLobby):null)};","cur={gid,local:false,st:seed||(fromLobby&&!fromLobby._sum?stripId(fromLobby):null)};")

# 5. tombol login/logout
rep("    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;","""    case 'fblogin':{el.disabled=true;try{await fbLogin();}catch(err){toast(err.message||'Login gagal');}finally{el.disabled=false;}break;}
    case 'fblogout':closeModal();try{await fbLogout();}catch(err){toast('Gagal keluar');}break;
    case 'reconnect':toast('Menyambung ulang…');reconnectNow();break;""")

# 6. fungsi pengganti khusus Firebase (deklarasi terakhir yang berlaku)
OVR=r'''
/* ================= EDISI FIREBASE ================= */
async function commitOnline(mut){
  const gid=cur.gid; let st;
  try{ st=await db.__txn('games/'+gid,d=>{ if(!d)fail('Meja tidak ditemukan'); const s=clone(d); mut(s); s.v=(s.v|0)+1; s.updatedAt=Date.now(); return s; }); }
  catch(e){ if(e instanceof GameErr||(e&&e.noop))throw e; console.warn('commit',e); throw new GameErr(e&&e.code==='permission-denied'?'Akses ditolak. Coba keluar lalu masuk lagi.':'Gagal menyimpan, coba lagi'); }
  if(cur&&cur.gid===gid)applyState(st);
}
function googleBtn(label){return `<button class="btn pri gbtn" data-act="fblogin"><svg viewBox="0 0 48 48" width="20" height="20" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>${label}</button>`;}
function appWarnHTML(){const app=inAppBrowser();if(!app)return '';
  return `<div class="gwarn">⚠️ Kamu membuka link dari <b>${app}</b>. Google tidak mengizinkan login dari browser bawaan ${app}. ${chromeIntent()?`<a class="btn pri" style="margin:6px 0;display:inline-block;text-decoration:none" href="${esc(chromeIntent())}">🌐 Buka di Chrome</a><br>Kalau tombol itu tidak jalan: `:''}ketuk <b>⋮</b> atau ikon kompas di pojok, lalu pilih <b>Buka di Chrome</b> (Android) atau <b>Buka di Safari</b> (iPhone).</div>`;}
function accessGateHTML(){
  if(online!=='off')return '';
  return `<section class="panel gate"><div class="gh"><span class="gi">🔐</span><div><h2>Masuk untuk main online</h2><p class="bd" style="margin:2px 0 0">Satu ketukan dengan akun <b>Google</b>. Setelah masuk kamu bisa membuat meja, masuk ke meja teman, dan punya profil serta peringkat.</p></div></div>
    ${appWarnHTML()}
    <div class="row" style="gap:8px;margin-top:8px">${googleBtn('Masuk dengan Google')}<button class="btn" data-act="gatecopy">🔗 Salin link halaman ini</button></div>
    <p class="bd" style="margin:8px 0 0">Belum mau masuk? Kamu tetap bisa main <b>🤖 lawan bot</b> di bawah, tapi hasilnya tidak tercatat.</p></section>`;
}
function openLoginPop(){
  openModal(`<div style="text-align:center"><div style="font-size:52px;line-height:1.1">🎲</div><h3 style="font-size:22px;margin:6px 0 4px">Masuk dulu, yuk!</h3>
    <p style="font-size:14.5px;line-height:1.55;margin:0 0 10px">Supaya bisa <b>main online bareng teman</b>, punya profil, rekor, dan peringkat, masuk dengan akun <b>Google</b>. Gratis, tanpa undangan.</p></div>
    ${appWarnHTML()}
    <div class="mbtns" style="justify-content:center"><button class="btn" data-act="close">Nanti saja, main lawan bot</button>${googleBtn('Masuk dengan Google')}</div>`);
}
/* lobi hanya didengarkan saat berada di lobi (hemat kuota baca) */
const __fbOpenTable=openTable;
openTable=function(gid,seed){if(lobbyUnsub){try{lobbyUnsub();}catch(e){}lobbyUnsub=null;}return __fbOpenTable(gid,seed);};
const __fbBackToLobby=backToLobby;
backToLobby=function(){const r=__fbBackToLobby.apply(this,arguments);if(online==='on'&&db&&!lobbyUnsub)subscribeLobby();return r;};
function reconnectNow(){
  if(online!=='on'||!db)return;
  if(cur&&!cur.local&&cur.gid){const gid=cur.gid;cur.retry=0;
    db.doc('games/'+gid).get().then(d=>{if(cur&&cur.gid===gid&&d.exists)applyState(d.data());}).catch(()=>{});
    watchTable(gid);}
  else if(!lobbyUnsub||ui.lobbyErr){try{if(lobbyUnsub)lobbyUnsub();}catch(e){}lobbyUnsub=null;subscribeLobby();}
  if(room)room.presence({uid:myId,g:cur&&!cur.local?cur.gid:null}).catch(()=>{});
}
'''
rep("(async function boot(){",OVR+"\n(async function boot(){")
# subscribeLobby boot: jangan berlangganan lobi kalau langsung membuka meja dari link
rep("  subscribeLobby(); setupRoom(); handleHash();","  if(!(location.hash||'').startsWith('#meja-'))subscribeLobby(); setupRoom(); handleHash();")
rep("</style>",".gbtn{display:inline-flex;align-items:center;gap:8px;background:#fff!important;color:#1f1f1f!important;border:1px solid #dadce0!important}\n</style>")

os.makedirs(OUT+'/fb',exist_ok=True)
open(OUT+'/index.html','w').write(s)
# SDK Firebase sudah tersimpan di OUT/fb (versi 10.14.1); disalin ulang hanya kalau folder repo belum punya
REPO=os.path.dirname(DEV)
for f in ['firebase-app-compat.js','firebase-auth-compat.js','firebase-firestore-compat.js','firebase-database-compat.js']:
    if not os.path.exists(OUT+'/fb/'+f): shutil.copy(REPO+'/fb/'+f,OUT+'/fb/'+f)
for f in ['shim.js','firebase-config.js','firestore.rules','database.rules.json','README.md']:
    shutil.copy(DEV+'/fbapp/'+f,OUT+'/'+f)
# video & poster tutorial tinggal di root repo
for f in ['tutorial-permata.mp4','tutorial-permata.jpg','tutorial-duel.mp4','tutorial-duel.jpg','tutorial-jualan.mp4','tutorial-jualan.jpg']:
    if os.path.abspath(OUT)!=os.path.abspath(REPO) and os.path.exists(REPO+'/'+f): shutil.copy(REPO+'/'+f,OUT+'/'+f)
print('fb ok')
