import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:90])
    s=s.replace(a,b)

# 1. Nomor urutan di samping nama
rep('<span class="n">${esc(nm(st,i))}</span>','<span class="ordn" title="Urutan giliran">${i+1}</span><span class="n">${esc(nm(st,i))}</span>')
rep("<span class=\"nm\">${p.bot?'🤖 ':''}","<span class=\"nm\"><span class=\"ordn\" title=\"Urutan giliran\">${i+1}</span>${p.bot?'🤖 ':''}")
rep("<div class=\"pmpn\"><b>${p.bot?'🤖':''}${esc(nm(st,i))}","<div class=\"pmpn\"><b><span class=\"ordn\" title=\"Urutan giliran\">${i+1}</span>${p.bot?'🤖':''}${esc(nm(st,i))}")
rep('<span class="pts">${esc(nm(st,seat))} · ${ptsOf(me)} poin</span>','<span class="pts"><span class="ordn me" title="Urutan giliranmu">${seat+1}</span>${esc(nm(st,seat))} · ${ptsOf(me)} poin</span>')

# 2. Notifikasi giliran setiap kali giliran berganti
rep("""  else if(cur&&cur.st){ if(cur.st.status==='lobby')renderWaiting(); else renderGame(); }
  else $('#app').innerHTML='<div class="panel mute">Memuat meja…</div>';""","""  else if(cur&&cur.st){ if(cur.st.status==='lobby')renderWaiting(); else {renderGame();turnNotice();} }
  else $('#app').innerHTML='<div class="panel mute">Memuat meja…</div>';
  if(view!=='table'||!cur||!cur.st||cur.st.status!=='playing')document.body.classList.remove('myturn','othturn');""")
rep("function myRank(st){","""function turnSeat(st){return st.game==='pemukim'?pmMe(st):actor(st);}
function turnPill(html,cls){let el=$('#turnPill');if(!el){el=document.createElement('div');el.id='turnPill';document.body.appendChild(el);}
  el.className=cls||'';el.innerHTML=html;requestAnimationFrame(()=>el.classList.add('show'));clearTimeout(ui.tpT);ui.tpT=setTimeout(()=>el.classList.remove('show'),2200);}
function turnNotice(){
  const st=cur&&cur.st; if(!st||st.status!=='playing'||cur.guided){document.body.classList.remove('myturn','othturn');return;}
  if(st.game&&st.game!=='pemukim')return;
  const me=turnSeat(st), t=st.turn, mine=me>=0&&t===me;
  document.body.classList.toggle('myturn',mine); document.body.classList.toggle('othturn',!mine);
  const base=(cur.lid||cur.gid||'x')+':', k=base+(st.round||0)+':'+t+':'+(st.phase==='setup'?'s':'');
  if(ui.tnKey===k)return; const first=!ui.tnKey||ui.tnKey.indexOf(base)!==0; ui.tnKey=k;
  if(first&&(st.round||1)<=1&&t===0&&mine)return;        // pop-up urutan awal sudah tampil
  if(first&&!mine&&st.round>1)return;                     // baru membuka meja yang sedang berjalan
  if(mine){const tp=$('#turnPill');if(tp)tp.classList.remove('show');}
  if(mine)rankPop('up','<span class="rpnum">'+(t+1)+'</span>','Giliranmu!',st.players.length>1?'Ayo jalan · kamu urutan '+(t+1):'',2200);
  else turnPill(`▶ Giliran <span class="ordn">${t+1}</span><b>${(st.players[t].bot?'🤖 ':'')+esc(nm(st,t))}</b>`);
}
function myRank(st){""")
# toast lama "Giliranmu!" hanya dipakai game hub lain
rep("""if(prev&&data.status==='playing'&&mi>=0&&data.turn===mi&&(prev.turn!==mi||prev.status!=='playing')){toast('Giliranmu!');ui.sel={};}""",
    """if(prev&&data.status==='playing'&&mi>=0&&data.turn===mi&&(prev.turn!==mi||prev.status!=='playing')){if(isHubGame(data)&&data.game!=='pemukim')toast('Giliranmu!');ui.sel={};}""")

# 3. Highlight giliran lebih jelas: emas = giliran orang lain, hijau = giliranmu
rep("</style>","""/* --- highlight giliran --- */
.ordn{display:inline-grid;place-items:center;min-width:19px;height:19px;padding:0 4px;border-radius:10px;background:var(--panel2);border:1px solid var(--line);color:var(--ink);font:800 11.5px/1 system-ui,sans-serif;margin-right:5px;vertical-align:1px}
.ordn.me{background:#b98f2c;border-color:#b98f2c;color:#1b1406}
.pl.turn,.m-opp.turn,.pmpl.turn{border-color:#ffd25e!important;background:linear-gradient(180deg,rgba(255,210,94,.22),rgba(255,210,94,.06))!important;box-shadow:0 0 0 2px #ffd25e,0 0 18px rgba(255,210,94,.55)!important;animation:turnGlow 1.6s ease-in-out infinite alternate}
.turn .ordn{background:#ffd25e;border-color:#ffd25e;color:#1b1406}
@keyframes turnGlow{from{box-shadow:0 0 0 2px #ffd25e,0 0 6px rgba(255,210,94,.35)}to{box-shadow:0 0 0 2px #ffd25e,0 0 22px rgba(255,210,94,.75)}}
.pl.mine-pl.turn,.pmpl.me.turn,body.myturn .m-ctrl{border-color:#45d483!important;background:linear-gradient(180deg,rgba(69,212,131,.25),rgba(69,212,131,.07))!important;box-shadow:0 0 0 2px #45d483,0 0 20px rgba(69,212,131,.6)!important;animation:myGlow 1.2s ease-in-out infinite alternate}
.pl.mine-pl.turn .ordn,.pmpl.me.turn .ordn,body.myturn .ordn.me{background:#45d483;border-color:#45d483;color:#062512}
@keyframes myGlow{from{box-shadow:0 0 0 2px #45d483,0 0 6px rgba(69,212,131,.4)}to{box-shadow:0 0 0 3px #45d483,0 0 26px rgba(69,212,131,.85)}}
body.myturn .m-top b{color:#45d483}
body.light .pl.turn,body.light .m-opp.turn,body.light .pmpl.turn{background:#fff3cc!important}
body.light .pl.mine-pl.turn,body.light .pmpl.me.turn,body.light.myturn .m-ctrl{background:#dcf8e7!important}
#turnPill{position:fixed;left:50%;top:14px;transform:translate(-50%,-140%);z-index:58;pointer-events:none;background:#2a2346;color:#f3eefe;border:1.5px solid #ffd25e;border-radius:999px;padding:8px 16px;font-size:15px;box-shadow:0 8px 24px #0008;transition:transform .25s ease,opacity .25s;opacity:0;white-space:nowrap;max-width:94vw;overflow:hidden;text-overflow:ellipsis}
#turnPill.show{transform:translate(-50%,0);opacity:1}
#turnPill .ordn{background:#ffd25e;color:#1b1406;border-color:#ffd25e;margin:0 5px}
body.light #turnPill{background:#fff;color:#2a2346}
@media (prefers-reduced-motion:reduce){.pl.turn,.m-opp.turn,.pmpl.turn,.pl.mine-pl.turn,.pmpl.me.turn,body.myturn .m-ctrl{animation:none}}
</style>""")
open(p,'w').write(s)
print('ok')
