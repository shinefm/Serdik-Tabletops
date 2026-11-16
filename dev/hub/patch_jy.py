import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:100])
    s=s.replace(a,b)
eng=open('hub/jualan.js').read()
rep("\nif(typeof module!=='undefined')module.exports={pmStart,","\n"+eng+"\nif(typeof module!=='undefined')module.exports={jyStart,jyAct,jyBotNext,jyApplyBot,jyWaiting,pmStart,")
rep("  wwk:{icon:'🐺',name:'Werewolf Klasik',min:6,max:20}\n};","  wwk:{icon:'🐺',name:'Werewolf Klasik',min:6,max:20},\n  jualan:{icon:'🛍️',name:'Jualan Yuk',min:1,max:24}\n};")
rep("function isHubGame(st){const g=st&&st.game;return g==='sandi'||","function isHubGame(st){const g=st&&st.game;return g==='jualan'||g==='sandi'||")
rep("function hubAct(st,pi,mv){return st.game==='sandi'?","function hubAct(st,pi,mv){return st.game==='jualan'?jyAct(st,pi,mv):st.game==='sandi'?")
rep("function hubStart(st){return st.game==='sandi'?","function hubStart(st){return st.game==='jualan'?jyStart(st):st.game==='sandi'?")
rep("function hubWinners(st){\n","function hubWinners(st){\n  if(st.game==='jualan')return st.players.map(p=>(st.winner||[]).includes(p.team));\n")
rep("/* ================= ONLINE PLUMBING ================= */",open('hub/jy_ui.js').read()+"\n/* ================= ONLINE PLUMBING ================= */")
rep("  if(isHubGame(cur.st))return cur.st.game==='wwk'?","  if(cur.st.game==='jualan'){renderJualan();maybeEndPopup(cur.st);jyMaybeBot();jyOnlineBot();return;}\n  if(isHubGame(cur.st))return cur.st.game==='wwk'?")
rep("  if(isHubGame(cur.st))return renderWaitingHub();","  if(isHubGame(cur.st))return cur.st.game==='jualan'?renderWaitingJY():renderWaitingHub();")
# buat meja
rep('<option value="pemukim">🏝️ Pemukim Nusantara (3–4)</option></select>','<option value="pemukim">🏝️ Pemukim Nusantara (3–4)</option><option value="jualan">🛍️ Jualan Yuk (2–4 tim)</option></select>')
rep("else if(e.target.value==='pemukim')t.value='180';else if(t.value==='0')t.value='180';","else if(e.target.value==='pemukim')t.value='180';else if(e.target.value==='jualan')t.value='0';else if(t.value==='0')t.value='180';")
rep("el.dataset.g==='pemukim'?'180':(t.value==='0'?'180':t.value);createTable();","el.dataset.g==='pemukim'?'180':el.dataset.g==='jualan'?'0':(t.value==='0'?'180':t.value);createTable();")
rep("    const st=md==='wwk'?{","    const st=md==='jualan'?{name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',game:'jualan',mode:'jualan',timer:tmr,nteams:2,split:false,botLevel:'normal',players:[{id:myId,nick:ui.nick||'',team:0}],v:1}\n      :md==='wwk'?{")
# aksi ruang tunggu
rep("      else if(kind==='timer'){","""      else if(kind==='jyteam'){ if(i<0)fail('Duduk dulu di meja'); st.players[i].team=+ui.jyTeamVal; }
      else if(kind==='jycfg'){ if(st.host!==myId)fail('Hanya tuan rumah'); const c=ui.jyCfg||{}; if(c.nteams)st.nteams=Math.max(2,Math.min(4,+c.nteams)); if(c.split!=null)st.split=c.split==='1'; if(c.botLevel)st.botLevel=c.botLevel; }
      else if(kind==='timer'){""")
rep("st.players.push(hub?{id:myId,nick:ui.nick||''}:newPlayer(myId,ui.nick)); }","st.players.push(hub?(st.game==='jualan'?{id:myId,nick:ui.nick||'',team:jySmallTeam(st)}:{id:myId,nick:ui.nick||''}):newPlayer(myId,ui.nick)); }")
rep("async function tableAction(kind){","function jySmallTeam(st){const n=st.nteams||2,c=Array(n).fill(0);st.players.forEach(p=>{if(p.team>=0&&p.team<n)c[p.team]++;});return c.indexOf(Math.min(...c));}\nasync function tableAction(kind){")
rep("  if(e.target.id==='tmrSel'){ui.tmrVal=e.target.value;tableAction('timer');}","""  if(e.target.id==='tmrSel'){ui.tmrVal=e.target.value;tableAction('timer');}
  if(e.target.id==='jyNt'||e.target.id==='jySp'||e.target.id==='jyLv'){ui.jyCfg={[e.target.id==='jyNt'?'nteams':e.target.id==='jySp'?'split':'botLevel']:e.target.value};tableAction('jycfg');}""")
rep("function inviteText(st,gid){if(st&&isHubGame(st)){const G=GAMES[st.game];return `Ayo main ${G.name} ${G.icon} (${G.min}–${G.max} pemain)!","function inviteText(st,gid){if(st&&isHubGame(st)){const G=GAMES[st.game];return `Ayo main ${G.name} ${G.icon} (${st.game==='jualan'?'2–4 tim, '+(st.split?'bagi peran':'mode sendiri'):G.min+'–'+G.max+' pemain'})!")
# klik
rep("    case 'reconnect':","""    case 'jylocal':jyLocalSetup();break;
    case 'jylocalgo':jyLocalStart();break;
    case 'jyinc':jyInc(el.dataset.k,+el.dataset.d);break;
    case 'jyready':jyReady();break;
    case 'jyinfo':jyInfoModal(el.dataset.q,el.dataset.p);break;
    case 'jyslhelp':{const c_=ui.jySlHelp!=null?ui.jySlHelp:st.round===1;ui.jySlHelp=!c_;render();break;}
    case 'jysum':ui.jySum=!ui.jySum;render();break;
    case 'jyacc':{ui.jyOpen=ui.jyOpen||{};ui.jyOpen[el.dataset.d]=!ui.jyOpen[el.dataset.d];render();break;}
    case 'jyhelp':{const cur_=ui.jyHelpOpen!=null?ui.jyHelpOpen:!!(ui.jyHelpFirst&&st.round===1);ui.jyHelpOpen=!cur_;render();break;}
    case 'jycell':if(ui.jy){ui.jy.cell={q:el.dataset.q,p:el.dataset.p};const T=st.teams[jyMyTeam(st)],c=JY.FEE[el.dataset.p];if(ui.jy.k&&c+ui.jy.k/2*JY.SOLD2>T.bud.sl)ui.jy.k=0;render();}break;
    case 'jyk':if(ui.jy){ui.jy.k=+el.dataset.k;render();}break;
    case 'jysell':{const F=ui.jy;if(!F||!F.cell)break;jyMove({type:'sell',q:F.cell.q,p:F.cell.p,k:F.k});break;}
    case 'jystop':openModal(`<h3>Berhenti jualan?</h3><p style="font-size:14px">Timmu tidak bisa jualan lagi di ronde ini. Sisa stok dan anggaran penjualan tetap tersimpan untuk ronde berikutnya.</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="jystopok">Ya, berhenti</button></div>`);break;
    case 'jystopok':closeModal();jyMove({type:'stop'});break;
    case 'jyend':openJYEnd();break;
    case 'jyjoin':ui.jyTeamVal=el.dataset.t;tableAction('jyteam');break;
    case 'reconnect':""")
# timer
rep("const mine=isHubGame(st)?(st.game==='pemukim'?","const mine=isHubGame(st)?(st.game==='jualan'?jyPending(st).includes(jyMe(st)):st.game==='pemukim'?")
rep("  if(st.game==='pemukim'){const pend=pmPending(st);","""  if(st.game==='jualan'){
    if(cur.local){const s=clone(st);jyTimeoutRun(s);cur.st=s;toast('⏱ Waktu habis — diisi otomatis');if(s.status==='ended')onGameEnded(s);render();return;}
    const me=meIdx(st);if(me<0||canWrite===false)return;const mine=jyPending(st).includes(me);if(!mine&&l>-4000-me*700)return;
    const v=st.v;ui.tmrBusy=true;commitOnline(s=>{if(s.v!==v||s.status!=='playing')throw NOOP;jyTimeoutRun(s);s.turnAt=Date.now();}).catch(()=>{}).finally(()=>{ui.tmrBusy=false;});return;}
  if(st.game==='pemukim'){const pend=pmPending(st);""")
# akhir & statistik
rep("  if(st.game==='pemukim')return pmOnEnded(st);","  if(st.game==='jualan')return jyOnEnded(st);\n  if(st.game==='pemukim')return pmOnEnded(st);")
rep("  if(st.game==='pemukim')return openPmEnd();","  if(st.game==='pemukim')return openPmEnd();\n  if(st.game==='jualan')return openJYEnd();")
rep("const VLAB={klasik:'💎 Klasik',","const VLAB={jualan:'🛍️ Jualan Yuk',klasik:'💎 Klasik',")
rep("function vOf(r){return ['duel','sandi','rapat','werewolf','pemukim','wwk'].includes(","function vOf(r){return ['duel','sandi','rapat','werewolf','pemukim','wwk','jualan'].includes(")
rep("pemukim:cell(),sandi:cell()},bot:{klasik:cell(),duel:cell(),pemukim:cell()}}","pemukim:cell(),jualan:cell(),sandi:cell()},bot:{klasik:cell(),duel:cell(),pemukim:cell(),jualan:cell()}}")
rep("pemukim:c(),sandi:c()},bot:{klasik:c(),duel:c(),pemukim:c()}}","pemukim:c(),jualan:c(),sandi:c()},bot:{klasik:c(),duel:c(),pemukim:c(),jualan:c()}}")
rep(", wkr=S.T.online.wwk||Z;\n  const tot=add(S.T.online.klasik,S.T.online.duel,rap,wwr,wkr,pmo,S.T.bot.klasik,S.T.bot.duel,pmb);",
    ", wkr=S.T.online.wwk||Z, jyo=S.T.online.jualan||Z, jyb=S.T.bot.jualan||Z;\n  const tot=add(S.T.online.klasik,S.T.online.duel,rap,wwr,wkr,pmo,jyo,S.T.bot.klasik,S.T.bot.duel,pmb,jyb);")
rep("${row('🌐 Online · 🏝️ Pemukim',pmo)}","${row('🌐 Online · 🏝️ Pemukim',pmo)}${row('🌐 Online · 🛍️ Jualan Yuk',jyo)}")
rep("${row('🤖 Bot · 🏝️ Pemukim',pmb)}","${row('🤖 Bot · 🏝️ Pemukim',pmb)}${row('🤖 Bot · 🛍️ Jualan Yuk',jyb)}")
rep("${tab('v','pemukim','🏝️ Pemukim')}","${tab('v','pemukim','🏝️ Pemukim')}${tab('v','jualan','🛍️ Jualan')}")
# tutorial
rep("""<button class="btn sm ${which==='pemukim'?'on':''}" data-act="tutorial" data-w="pemukim">🏝️ Pemukim</button>""","""<button class="btn sm ${which==='pemukim'?'on':''}" data-act="tutorial" data-w="pemukim">🏝️ Pemukim</button><button class="btn sm ${which==='jualan'?'on':''}" data-act="tutorial" data-w="jualan">🛍️ Jualan Yuk</button>""")
rep("  if(which==='rapat'||which==='werewolf'||which==='pemukim'||which==='wwk'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class=\"rules tutrules\">${which==='wwk'?wkRules():",
    "  if(which==='jualan'){openModal(`<h3>🎬 Tutorial & aturan</h3>${tabs}<div class=\"tutv\"><video src=\"tutorial-jualan.mp4\" poster=\"tutorial-jualan.jpg\" controls playsinline preload=\"metadata\"></video></div><p class=\"bd\" style=\"margin:8px 0 0\"><b>🛍️ Jualan Yuk</b> · ±45 detik · Papan demand, belanja SDM dan produksi, CR, dana jualan, token Pasti, dan fase jualan.</p><div class=\"rules tutrules\">${jyRules()}</div><div class=\"mbtns\"><button class=\"btn pri\" data-act=\"close\">Siap main!</button></div>`);return;}\n  if(which==='rapat'||which==='werewolf'||which==='pemukim'||which==='wwk'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class=\"rules tutrules\">${which==='wwk'?wkRules():")
# kartu hub
rep("  sandi:{icon:'🕵️',name:'Sandi Syndicate',ply:","  jualan:{icon:'🛍️',name:'Jualan Yuk',ply:'2–4 tim · 1–24 orang · bisa lawan bot',dur:'15–30 menit',kind:'Simulasi bisnis tim · terinspirasi Selling Race',desc:'Jadi direksi perusahaan kain. Keuangan bagi anggaran, SDM rekrut karyawan, Produksi bikin barang, Pemasaran naikkan CR, lalu Penjualan berebut demand pasar. 5 ronde, kas terbanyak menang. Mode sendiri atau bagi peran.',mk:[['MK02','alokasi anggaran'],['MK03','segmen & harga'],['MK04','kapasitas produksi']]},\n  sandi:{icon:'🕵️',name:'Sandi Syndicate',ply:")
rep("    else if(k==='pemukim')b=","    else if(k==='jualan')b=`${EDITION!=='latihan'?'<button class=\"btn pri sm\" data-act=\"hubnew\" data-g=\"jualan\">Buat meja</button>':''}<button class=\"btn sm\" data-act=\"jylocal\">🤖 Lawan bot</button><button class=\"btn sm\" data-act=\"tutorial\" data-w=\"jualan\">🎬 Tutorial</button>`;\n    else if(k==='pemukim')b=")
rep("${['permata','pemukim','rapat','werewolf','sandi'].map(card).join('')}","${['permata','jualan','pemukim','rapat','werewolf','sandi'].map(card).join('')}")
# notifikasi online
rep("function hubNotify(prev,d){\n  if(!prev||prev.status!=='playing'||!isHubGame(d))return;","""function hubNotify(prev,d){
  if(!prev||prev.status!=='playing'||!isHubGame(d))return;
  if(d.game==='jualan'){const me=meIdx(d),t=me>=0?d.players[me].team:-1;
    if(prev.phase==='plan'&&d.phase==='sell')rankPop('up','🛒','Fase jualan!','Urutan: '+d.order.map(i=>d.teams[i].name).join(' → '),3200);
    else if(d.phase==='sell'&&t>=0&&d.order[d.si]===t&&(prev.phase!=='sell'||prev.order[prev.si]!==t)&&jyCan(d,me,t,'sl'))rankPop('up','🛒','Giliran jualan timmu!','Pilih kotak demand yang mau diincar',2600);
    if(d.draw&&(!prev.draw||prev.draw.n!==d.draw.n)&&d.draw.t!==t){const D=d.draw;toast(`${d.teams[D.t].name}: ${JY.QN[D.q]} ${JY.PN[D.p]} → ${D.ok?'laku '+D.units:'gagal'}`);}
    return;}""")
# keluar & main ulang (lawan bot)
rep("async function leaveTable(next){\n  next=next||backToLobby;\n  if(!(cur&&cur.local&&!cur.guided&&cur.st&&cur.st.status==='playing')){next();return;}","""async function leaveTable(next){
  next=next||backToLobby;
  if(!(cur&&cur.local&&!cur.guided&&cur.st&&cur.st.status==='playing')){next();return;}
  if(cur.st.game==='jualan'){ui.afterLeave=next;openModal(`<h3>🚪 Keluar dari Jualan Yuk?</h3><p style="font-size:14px;line-height:1.55;margin:0">Game lawan tim bot ini belum selesai (ronde ${cur.st.round}/${cur.st.rounds}). Progres tidak disimpan.</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn" data-act="restartlocalok">🆕 Main game baru</button><button class="btn pri" data-act="nosavequit">Keluar</button></div>`);return;}""")
rep("function restartCfg(){\n  const st=cur.st,","function restartCfg(){\n  if(cur.st.game==='jualan')return Object.assign({jy:true},ui.lastJy||{me:cur.st.players[0].nick||'Kamu',nbot:cur.st.teams.length-1,level:cur.level||'normal',timer:cur.st.timer||0});\n  const st=cur.st,")
rep("if(L.pm)pmStartCfg(L);else startLocalCfg(L);","if(L.jy)jyStartCfg(L);else if(L.pm)pmStartCfg(L);else startLocalCfg(L);")
css=r""".jywrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:14px;max-width:1180px;margin:0 auto;align-items:start}
.jywrap>.jyhead{grid-column:1/-1}.jywrap>.jyhead+section{grid-row:span 3}
@media(max-width:900px){.jywrap{grid-template-columns:1fr}.jywrap>.jyhead+section{grid-row:auto}}
.jydot{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:-1px;border:1.5px solid rgba(0,0,0,.35)}
.jyh2{font-size:18px;margin:0 0 10px;display:flex;align-items:center;gap:4px;flex-wrap:wrap}.jyh2 small{font-size:12px;font-weight:400;margin-left:6px}
.jymine{border:1.5px solid var(--tc)}
.jytiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}@media(max-width:520px){.jytiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
.jyt{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:7px 9px}.jyt small{display:block;font-size:11.5px;color:var(--mute)}.jyt b{font-size:17px;font-family:Fraunces,serif}
.jybud{font-size:12.5px;color:var(--mute);margin:8px 0 4px;line-height:1.5}.jybud b{color:var(--ink)}
.jytabs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;margin:10px 0 8px}
.jytab{font:inherit;display:flex;flex-direction:column;align-items:center;gap:1px;padding:7px 2px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--ink);cursor:pointer;min-width:0}
.jytab span{font-size:12.5px;font-weight:700}.jytab small{font-size:10.5px;color:var(--mute);max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.jytab.mine{border-color:var(--gold)}.jytab.on{outline:2px solid var(--gold);background:rgba(230,184,76,.14)}
.jybody{min-height:80px}.jyhelp{font-size:13.5px;line-height:1.5;margin:0 0 8px}.jywait{font-size:14px;margin:8px 0}
.jyst{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:6px 0;border-top:1px solid var(--line)}
.jysl b{display:block;font-size:14px}.jysl small{font-size:11.5px;color:var(--mute)}
.jysb{display:flex;align-items:center;gap:8px}.jysb span{min-width:64px;text-align:center;font-weight:700}.jysb .btn{min-width:36px}
.jysum{margin:8px 0;font-size:14px}.jysum .bad,.bad{color:#ff8a8a;font-weight:700}
.jygo{width:100%;margin-top:6px}
.jyabl{margin:6px 0;font-size:12.5px}.jyabl table{border-collapse:collapse;margin:6px 0;width:100%}.jyabl th,.jyabl td{border:1px solid var(--line);padding:4px 6px;text-align:center}
.jydem{display:grid;grid-template-columns:92px repeat(3,minmax(0,1fr));gap:5px}
.jyph,.jyqh{font-size:12.5px;font-weight:700;text-align:center;align-self:center}.jyph small{display:block;font-weight:400;font-size:10.5px;color:var(--mute)}.jyqh{text-align:left}
.jyc{font:inherit;border-radius:10px;border:1.5px solid transparent;padding:8px 2px;display:flex;flex-direction:column;align-items:center;cursor:default;color:#1b1406}
.jyc b{font-size:24px;font-family:Fraunces,serif;line-height:1}.jyc small{font-size:10.5px;opacity:.8}
.jyc.qH{background:#f2d26b}.jyc.qM{background:#7cc9a3}.jyc.qL{background:#8fb8e3}
.jyc.zero{opacity:.35}.jyc.na{opacity:.45;filter:saturate(.4)}.jyc[data-act]{cursor:pointer;border-color:#fff8}.jyc.sel{outline:3px solid var(--gold);outline-offset:1px;border-color:#fff}
.jyords{display:flex;flex-wrap:wrap;gap:5px;margin:4px 0 10px}.jyord{font-size:12px;padding:3px 8px;border-radius:99px;border:1.5px solid;opacity:.75}.jyord.now{opacity:1;font-weight:700;background:rgba(230,184,76,.15)}.jyord.done{opacity:.45;text-decoration:line-through}
.jysp{margin-top:12px;padding-top:10px;border-top:1px solid var(--line)}
.jyboard{display:grid;gap:6px}
.jycash{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.jycash small{color:var(--mute);font-size:12px}.jycash b{font:700 26px Fraunces,serif;color:var(--gold)}.jyminus{font-size:12px;color:#ff9a9a}
.jyrow{display:grid;grid-template-columns:104px minmax(0,1fr);gap:8px;align-items:center;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:6px 8px;min-height:44px}
.jyrl{font-size:12.5px;font-weight:700}.jytot{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.jynone{font-size:12px;color:var(--mute)}.jynum{margin-left:auto;font:700 15px Fraunces,serif}.jymore{font-size:12px;font-weight:700;color:var(--mute)}
.jyp{position:relative;display:inline-block;width:24px;height:30px;flex:none}
.jyp::before{content:"";position:absolute;left:7px;top:0;width:10px;height:10px;border-radius:50%;background:var(--pc)}
.jyp::after{content:"";position:absolute;left:2px;bottom:0;width:20px;height:18px;border-radius:9px 9px 4px 4px;background:var(--pc)}
.jyp i{position:absolute;left:0;right:0;bottom:3px;z-index:1;font:800 9.5px/1 system-ui,sans-serif;text-align:center;color:#14102a;font-style:normal}
.jyp.l1{--pc:#b9bfd0}.jyp.l2{--pc:#5fc4e8}.jyp.l3{--pc:#f0b93f}
.jyp.sm{width:17px;height:22px}.jyp.sm::before{left:5px;width:7px;height:7px}.jyp.sm::after{left:1px;width:15px;height:13px;border-radius:7px 7px 3px 3px}.jyp.sm i{font-size:7.5px;bottom:2px}
.jycube{display:inline-block;width:22px;height:22px;border-radius:5px;flex:none;box-shadow:inset -3px -3px 0 rgba(0,0,0,.22),inset 2px 2px 0 rgba(255,255,255,.4);border:1px solid rgba(0,0,0,.35);vertical-align:-4px}
.jycube.qH{background:#f2d26b}.jycube.qM{background:#7cc9a3}.jycube.qL{background:#8fb8e3}.jycube.sm{width:14px;height:14px;border-radius:3px;box-shadow:inset -2px -2px 0 rgba(0,0,0,.22);vertical-align:-2px}
.jyheart{color:#ff6b8b;font-size:19px;line-height:1}.jycoin{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#e6b84c;color:#5a3d00;font:800 8.5px/1 system-ui,sans-serif;border:1.5px solid #a87a16;flex:none}
.jyp.new,.jycube.new,.jyheart.new,.jycoin.new{outline:2px dashed #fff;outline-offset:1px;border-radius:6px;animation:jypop .25s ease-out}
@keyframes jypop{from{transform:scale(.3);opacity:0}to{transform:none;opacity:1}}
.jyleg{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:11.5px;color:var(--mute);align-items:center}.jyleg span{display:inline-flex;align-items:center;gap:3px}
.jyplan{margin-top:12px;border-top:1px solid var(--line);padding-top:8px}
.jysec{font-size:15px;margin:12px 0 6px;display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}.jywho{font-size:11.5px;font-weight:400;color:var(--mute)}.jywho.me{color:var(--gold);font-weight:700}
.jyits{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-bottom:6px}.jyits.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.jyit{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:8px 4px;display:flex;flex-direction:column;align-items:center;gap:2px;text-align:center;min-width:0}
.jyit.has{border-color:var(--gold);background:rgba(230,184,76,.1)}
.jyii{height:32px;display:flex;align-items:center;gap:3px;font-size:12px}.jyit b{font-size:13.5px}.jyit small{font-size:11px;color:var(--mute);line-height:1.25}
.jyit .jysb{gap:2px;margin-top:4px}.jyit .jysb span{min-width:26px;font:700 17px Fraunces,serif}.jyit .jysb .btn{min-width:32px;width:32px;min-height:36px;font-size:18px;padding:0}.jyits.two .jysb span{min-width:60px}
.jytotal{margin-top:12px;background:var(--panel2);border:1.5px solid var(--gold);border-radius:12px;padding:8px 12px}
.jycalc{display:flex;justify-content:space-between;align-items:baseline;font-size:13.5px;padding:3px 0}.jycalc b{font:700 15px Fraunces,serif}.jycalc.zero{opacity:.45}
.jycalc.sum{border-top:1.5px solid var(--line);margin-top:4px;padding-top:6px;font-size:15px;font-weight:700}.jycalc.sum b{font-size:22px;color:var(--gold)}
.jycalc.kas{font-size:12.5px;color:var(--mute)}.jycalc.kas b{font-size:14px;color:var(--ink)}
.jytotal.over{border-color:#ff8a8a}.jytotal.over .sum b{color:#ff8a8a}
.jybub{margin-left:auto;font:700 14px Fraunces,serif;padding:3px 10px;border-radius:99px;background:var(--panel2);border:1px solid var(--line);color:var(--mute)}.jybub.on{background:var(--gold);color:#1b1406;border-color:var(--gold)}
.jysub{font-style:normal;font-size:11px;color:var(--mute);min-height:15px}.jysub.on b{color:var(--gold)}
.jyits.one{grid-template-columns:1fr}.jyits.one .jysb span{min-width:70px}
.jyprob{display:flex;gap:1.5px;margin:2px 0 1px}.jyprob i{font:800 9.5px/1 system-ui,sans-serif;font-style:normal;width:13px;height:13px;display:grid;place-items:center;border-radius:3px;background:rgba(255,255,255,.7);color:#1b1406}.jyprob i.x{background:#c0392b;color:#fff}
.jypct{font-style:normal;font-size:10.5px;font-weight:700}
.jyc{cursor:pointer}.jyc.info{outline:3px solid #fff;outline-offset:1px}
.jyinfo,.jytap{display:none}
@media(max-width:560px){.jyc .jydt{display:none}.jyc{padding:7px 2px}.jytap{display:block;margin:6px 0 0}
  .jyinfo{display:block;margin-top:8px;border-radius:12px;padding:10px 12px;background:var(--panel2);border:1.5px solid var(--line)}
  .jyinfo.qH{border-color:#f2d26b}.jyinfo.qM{border-color:#7cc9a3}.jyinfo.qL{border-color:#8fb8e3}
  .jyih{display:flex;align-items:center;gap:6px;font-size:15px;margin-bottom:6px}.jyih .btn{margin-left:auto;min-width:32px}
  .jyig{display:grid;grid-template-columns:1fr auto;gap:4px 10px;font-size:13.5px;align-items:center}.jyig span{color:var(--mute)}.jyig b{text-align:right;justify-content:flex-end}.jyig small{font-weight:400;color:var(--mute)}
  .jyin{margin:8px 0 0;font-size:13px}}
.jyacc{border:1px solid var(--line);border-radius:12px;background:var(--panel2);margin-bottom:8px;overflow:hidden}.jyacc.open{border-color:var(--gold)}
.jyah{font:inherit;color:var(--ink);background:none;border:0;width:100%;text-align:left;cursor:pointer;display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:6px 8px;align-items:center;padding:10px 12px}
.jyat{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}.jyat b{font-size:15px}.jyah .jybub{margin:0}.jychev{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--gold);color:#1b1406;font-size:20px;font-weight:800;line-height:1;transition:transform .15s}.jyacc.open .jychev{transform:rotate(180deg)}
.jyah .jytot{grid-column:1/-1;min-height:24px}
.jyab{padding:4px 10px 10px;border-top:1px solid var(--line)}.jyab .jyit{background:var(--panel)}
.jyq{display:flex;align-items:flex-start;gap:8px;margin:0 0 8px}
.jyqb{font:800 13px/1 system-ui,sans-serif;width:22px;height:22px;flex:none;border-radius:50%;border:1.5px solid var(--line);background:var(--panel2);color:var(--mute);cursor:pointer;padding:0}.jyqb.on{border-color:var(--gold);color:var(--gold)}
.jyqt{font-size:11.5px;line-height:1.45;color:var(--mute);margin:2px 0 0}.jyqh2{font-size:11.5px;color:var(--mute);align-self:center}
@media(max-width:900px){.jywrap>.jyhead{order:-2}.jywrap>.jydemp{order:-1}}
.jytap{display:block!important;margin:6px 0 0}
.jyml{display:grid;gap:10px;margin:10px 0}.jymr{display:grid;grid-template-columns:86px minmax(0,1fr);gap:10px;align-items:center}
.jymi{display:flex;justify-content:center;align-items:center;gap:2px;min-height:34px;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:6px 4px}
.jymr b{display:block;font-size:14.5px}.jymr small{font-size:12.5px;color:var(--mute);line-height:1.4}.jybig{font:700 24px Fraunces,serif!important}
.jyprob.lg i{width:14px;height:14px;background:#fff}.jyprob.lg i.x{background:#c0392b}
.jyin{margin:8px 0 0;font-size:13.5px;font-weight:700}
.jyslx{font-size:12.5px;line-height:1.45;color:var(--mute);margin-top:6px}.jyslx b{color:var(--ink)}.jyslx ul{margin:4px 0 0;padding-left:18px}.jyslx li{margin:3px 0}
.jycnt{font-size:13px;font-weight:400;background:var(--panel);border:1px solid var(--line);border-radius:99px;padding:2px 9px;white-space:nowrap}.jycnt b{font:700 15px Fraunces,serif;color:var(--gold)}.jycnt small{color:var(--mute);font-size:11px}
.jyrl .jycnt{display:inline-block;margin-top:3px;padding:1px 6px;white-space:normal}
.jyslx{margin-top:0!important}.jytokv{display:flex;align-items:center;gap:5px;margin:6px 0 2px;flex-wrap:wrap}.jypasti{font:800 10.5px/1 system-ui,sans-serif;padding:4px 8px;border-radius:99px;background:#45d483;color:#062512;border:1.5px solid #1f9d57}
.jysumh{font:inherit;color:var(--ink);background:none;border:0;width:100%;cursor:pointer;display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:8px;align-items:center;padding:2px 0;text-align:left;font-size:14.5px;font-weight:700}
.jysumh b{font:700 24px Fraunces,serif;color:var(--gold)}.jytotal.over .jysumh b{color:#ff8a8a}.jytotal.open .jychev{transform:rotate(180deg)}
.jysumb{border-top:1px solid var(--line);margin-top:6px;padding-top:4px}
.jytotal .jycalc.kas{border-top:1.5px solid var(--line);margin-top:6px;padding-top:6px;font-size:14px;color:var(--ink)}.jytotal .jycalc.kas b{font-size:18px}
.jycash.over b{color:#ff8a8a}.jysumb .jycalc.sum b{font-size:18px}
.jycalc.plus b{color:#45d483}.jycalc.base{font-weight:700;border-bottom:1px dashed var(--line);padding-bottom:5px;margin-bottom:2px}
.jydc{font-size:10px;color:var(--mute);align-self:end;line-height:1.2}
.jyqh span{display:flex;flex-direction:column;line-height:1.15}.jyqh small{font-weight:400;font-size:10.5px;color:var(--mute)}
.jyneed{display:flex;gap:1px;margin-top:3px;background:rgba(255,255,255,.55);border-radius:8px;padding:2px 4px}.jyneed.no{opacity:.4}
.jydleg{display:flex;flex-wrap:wrap;gap:3px 12px;font-size:11.5px;color:var(--mute);margin-top:8px}.jydleg span{display:inline-flex;align-items:center;gap:3px}
.jymini{display:grid;gap:4px;margin-top:6px}
.jypips{display:flex;flex-wrap:wrap;justify-content:center;gap:2px;max-width:56px;min-height:7px}.jypips i{width:6px;height:6px;border-radius:50%;background:#1b1406;opacity:.55}
.jyqh{display:flex;align-items:center;gap:4px}
.jysel{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:10px;font-size:14px}
.jyks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin:8px 0}.jyks .btn{display:flex;flex-direction:column;align-items:center;font-size:13px}.jyks .btn small{font-size:11px;opacity:.8}.jyks .btn.on{outline:2px solid var(--gold)}
.jydraw{margin-top:12px;border:2px solid;border-radius:12px;padding:10px;text-align:center}
.jydh{font-size:13.5px;margin-bottom:8px}.jytoks{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
.jytok{position:relative;min-width:40px;padding:6px 8px;border-radius:99px;font-weight:700;background:var(--panel2);border:1.5px solid var(--line);font-size:14px}
.jytok.bad{color:#ff8a8a}.jytok.pasti{background:#45d483;color:#062512;border-color:#1f9d57}.jytok i{font-style:normal;font-size:10px;margin-left:2px}
.jytok.hit{background:var(--gold);color:#1b1406;border-color:var(--gold);transform:scale(1.15)}
.jydraw.anim .jytok{animation:jyshuf .18s ease-in-out calc(var(--i)*.09s) 5 alternate}
.jydraw.anim .jytok.hit{animation:jyhit .5s ease-out 1.15s both}
.jydraw.anim .jyres{animation:jyfade .4s ease-out 1.45s both}
@keyframes jyshuf{to{transform:translateY(-6px);background:rgba(230,184,76,.35)}}
@keyframes jyhit{from{transform:scale(1);background:var(--panel2);color:var(--ink)}60%{transform:scale(1.35)}to{transform:scale(1.15)}}
@keyframes jyfade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.jyres{margin-top:10px;font-size:18px;font-weight:700}.jyres.ok{color:#45d483}.jyres.no{color:#ff8a8a}.jyres small{font-size:12px;font-weight:400;color:var(--mute)}
.jytms{display:grid;gap:8px}.jytm{border:1px solid var(--line);border-left:4px solid var(--tc);border-radius:10px;padding:8px 10px;background:var(--panel2)}
.jytm.me{box-shadow:inset 0 0 0 1px var(--tc)}.jytm.turn{border-color:#ffd25e;box-shadow:0 0 0 2px #ffd25e;animation:turnGlow 1.6s ease-in-out infinite alternate}
.jytmh{display:flex;align-items:center;gap:4px}.jytms{margin-left:auto;font-size:12px;color:var(--mute)}
.jytmn{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:13px;margin-top:4px}
.jywts{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:8px 0}@media(max-width:520px){.jywts{grid-template-columns:1fr}}
.jywt{border:1px solid var(--line);border-top:4px solid var(--tc);border-radius:10px;padding:8px 10px;background:var(--panel2)}
.jychart{width:100%;max-width:420px;display:block;margin:10px auto 0;color:var(--ink)}
.logbox .lg{font-size:13px;padding:4px 0;border-bottom:1px solid var(--line)}
body.light .jyc{color:#1b1406}
body.light .rtag.o{"""
rep("body.light .rtag.o{",css)
open(p,'w').write(s)
print('jy ok')
