import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:90])
    s=s.replace(a,b)

# Tombol "kembali" HP/browser: tutup pop-up dulu, lalu kembali ke lobi (sama seperti tombol ← Lobi)
rep("""function openModal(html){$('#mbox').innerHTML=html;$('#modal').classList.add('open');}
function closeModal(){$('#modal').classList.remove('open');$('#mbox').innerHTML='';}""","""function openModal(html){$('#mbox').innerHTML=html;$('#modal').classList.add('open');navGuard();}
function closeModal(){$('#modal').classList.remove('open');$('#mbox').innerHTML='';if(view!=='table')navPop();}
/* --- riwayat browser: satu entri "penjaga" selama ada meja / pop-up terbuka --- */
function modalOpen(){const m=$('#modal');return !!(m&&m.classList.contains('open'));}
function navGuard(url){try{if(view!=='table'&&!modalOpen())return;
  if(history.state&&history.state.sg){if(url&&location.hash!==url)history.replaceState({sg:1},'',url);return;}
  history.pushState({sg:1},'',url||location.href);}catch(e){}}
function navPop(){try{if(ui.navSkip)return;if(history.state&&history.state.sg){ui.navSkip=1;history.back();}}catch(e){}}
window.addEventListener('popstate',()=>{
  if(ui.navSkip){ui.navSkip=0;setTimeout(()=>navGuard(),0);return;}
  if(modalOpen())closeModal();
  else if(view==='table')leaveTable();
  setTimeout(()=>navGuard(),0);
});""")

# Buka meja online: hash meja hanya ada di entri penjaga
rep("""  try{if(location.hash!=='#meja-'+gid)location.hash='meja-'+gid;}catch(e){}
  cur.retry=0; watchTable(gid);""","""  navGuard('#meja-'+gid);
  cur.retry=0; watchTable(gid);""")

# Kembali ke lobi: buang entri penjaga (kalau keluar lewat tombol di layar)
rep("""  cur=null; view='lobby'; ui.sel={}; closeModal();
  try{if(location.hash)history.replaceState(null,'',location.pathname+location.search);}catch(e){try{location.hash='';}catch(_){}}""","""  cur=null; view='lobby'; ui.sel={}; closeModal();
  try{if(history.state&&history.state.sg)navPop();else if(location.hash)history.replaceState(null,'',location.pathname+location.search);}catch(e){try{location.hash='';}catch(_){}}""")

# Setiap render meja: pastikan penjaga ada
rep("""  if(view!=='table'||!cur||!cur.st||cur.st.status!=='playing')document.body.classList.remove('myturn','othturn');""","""  if(view!=='table'||!cur||!cur.st||cur.st.status!=='playing')document.body.classList.remove('myturn','othturn');
  if(view==='table')navGuard();""")
open(p,'w').write(s)
print('ok')
