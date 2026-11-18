# Sandi Syndicate (mirip Codenames): ruang tunggu tim, papan 5x5, petunjuk, tebakan, aturan, layar akhir
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b):
    global s
    n=s.count(a); assert n==1,(n,a[:90]); s=s.replace(a,b)

ui_js=open('hub/sandi_ui.js').read()
rep("function openHubEnd(){",ui_js+"\nfunction openHubEnd(){")

# kartu hub: tidak lagi "Segera hadir"
rep("mk:[['MK01–06','istilah materi']],soon:true}","mk:[['MK01–06','istilah materi']]}")
rep("    else if(k==='rapat'||k==='werewolf')b=EDITION==='latihan'?","    else if(k==='rapat'||k==='werewolf'||k==='sandi')b=EDITION==='latihan'?")
rep("Ketua tim memberi petunjuk satu kata untuk menebak istilah materi MK di papan 5×5.",
    "Ketua tim memberi petunjuk satu kata, anggotanya menebak istilah materi MK di papan 5×5. Hindari Kartu Audit!")

# buat meja
rep('<option value="jualan">🛍️ Jualan Yuk (2–4 tim)</option></select>',
    '<option value="jualan">🛍️ Jualan Yuk (2–4 tim)</option><option value="sandi">🕵️ Sandi Syndicate (4–8)</option></select>')
rep("el.dataset.g==='jualan'?'0':(t.value==='0'?'180':t.value);createTable();break;}",
    "el.dataset.g==='jualan'?'0':el.dataset.g==='sandi'?'180':(t.value==='0'?'180':t.value);createTable();break;}")
rep("      :md==='wwk'?{name,host:myId,",
    "      :md==='sandi'?{name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',game:'sandi',mode:'sandi',timer:tmr,pack:'mix',players:[{id:myId,nick:ui.nick||'',team:'r',ketua:true}],v:1}\n      :md==='wwk'?{name,host:myId,")
rep("st.players.push(hub?(st.game==='jualan'?{id:myId,nick:ui.nick||'',team:jySmallTeam(st)}:",
    "st.players.push(hub?(st.game==='jualan'?{id:myId,nick:ui.nick||'',team:jySmallTeam(st)}:st.game==='sandi'?{id:myId,nick:ui.nick||'',team:st.players.filter(q=>q.team==='r').length<=st.players.filter(q=>q.team==='b').length?'r':'b'}:")
rep("      else if(kind==='jyteam'){",
    """      else if(kind==='sdteam'){ if(i<0)fail('Duduk dulu di meja'); const t=ui.sdTeamVal; if(t!=='r'&&t!=='b')fail('Tim tidak dikenal'); st.players[i].team=t; st.players[i].ketua=false; }
      else if(kind==='sdketua'){ const k=ui.sdKVal|0, P=st.players[k]; if(!P)fail('Pemain tidak ditemukan'); if(st.host!==myId&&k!==i)fail('Hanya tuan rumah yang bisa memilih ketua orang lain'); st.players.forEach(q=>{if(q.team===P.team)q.ketua=false;}); P.ketua=true; }
      else if(kind==='sdpack'){ if(st.host!==myId)fail('Hanya tuan rumah'); if(!PACKS.some(x=>x[0]===ui.sdPackVal))fail('Paket kata tidak dikenal'); st.pack=ui.sdPackVal; }
      else if(kind==='jyteam'){""")
rep("  if(e.target.id==='tmrSel'){ui.tmrVal=e.target.value;tableAction('timer');}",
    "  if(e.target.id==='tmrSel'){ui.tmrVal=e.target.value;tableAction('timer');}\n  if(e.target.id==='sdPack'){ui.sdPackVal=e.target.value;tableAction('sdpack');}")

# tampilan
rep("  if(isHubGame(cur.st))return cur.st.game==='jualan'?renderWaitingJY():renderWaitingHub();",
    "  if(isHubGame(cur.st))return cur.st.game==='jualan'?renderWaitingJY():cur.st.game==='sandi'?renderWaitingSD():renderWaitingHub();")
rep("  if(isHubGame(cur.st))return cur.st.game==='wwk'?renderWK():",
    "  if(cur.st.game==='sandi')return renderSandi();\n  if(isHubGame(cur.st))return cur.st.game==='wwk'?renderWK():")
rep("  if(st.game==='wwk')return openWKEnd();","  if(st.game==='wwk')return openWKEnd();\n  if(st.game==='sandi')return openSDEnd();")
# yang ditunggu (timer milikku, menu tuan rumah)
rep("function rapatPending(st){\n  if(st.status!=='playing')return [];",
    "function rapatPending(st){\n  if(st.status!=='playing')return [];\n  if(st.game==='sandi')return st.players.map((p,i)=>i).filter(i=>st.players[i].team===st.turnTeam&&(st.phase==='clue'?!!st.players[i].ketua:!st.players[i].ketua));")
# lewati oleh tuan rumah
rep("    st.log.push({p:-1,m:`⏱ Tim ${TEAMNAME[st.turnTeam]} kehabisan waktu ${st.phase==='clue'?'memberi petunjuk':'menebak'} — giliran pindah.`});",
    "    st.log.push({p:-1,m:mv.forced?`⏭ Giliran Tim ${TEAMNAME[st.turnTeam]} dilewati tuan rumah.`:`⏱ Tim ${TEAMNAME[st.turnTeam]} kehabisan waktu ${st.phase==='clue'?'memberi petunjuk':'menebak'} — giliran pindah.`});")

# klik
rep("    case 'jyjoin':",
    """    case 'sdteam':ui.sdTeamVal=el.dataset.t;tableAction('sdteam');break;
    case 'sdketua':ui.sdKVal=+el.dataset.i;tableAction('sdketua');break;
    case 'sdcard':sdClick(+el.dataset.i);break;
    case 'sdguess':sdGuess();break;
    case 'sdcancel':ui.sdSel=null;render();break;
    case 'sdinfo':sdInfo(+el.dataset.i);break;
    case 'sdclue':sdSendClue();break;
    case 'sdend':hubMove({type:'endturn'});break;
    case 'sdkey':ui.sdKey=ui.sdKey===false;render();break;
    case 'sdhk':hostDo('ketua',+el.dataset.i,'🎖️ Ketua tim diganti');break;
    case 'jyjoin':""")
# Enter di kolom petunjuk
rep("  if(e.target.id==='sdPack'){","  if(e.target.id==='sdN'){ui.sdN=+e.target.value;}\n  if(e.target.id==='sdPack'){")

# tutorial & aturan
rep('<button class="btn sm ${which===\'jualan\'?\'on\':\'\'}" data-act="tutorial" data-w="jualan">🛍️ Jualan Yuk</button></div>`;',
    '<button class="btn sm ${which===\'jualan\'?\'on\':\'\'}" data-act="tutorial" data-w="jualan">🛍️ Jualan Yuk</button><button class="btn sm ${which===\'sandi\'?\'on\':\'\'}" data-act="tutorial" data-w="sandi">🕵️ Sandi</button></div>`;')
rep("  if(which==='rapat'||which==='werewolf'||which==='pemukim'||which==='wwk'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class=\"rules tutrules\">${which==='wwk'?wkRules():",
    "  if(which==='rapat'||which==='werewolf'||which==='pemukim'||which==='wwk'||which==='sandi'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class=\"rules tutrules\">${which==='sandi'?sandiRules():which==='wwk'?wkRules():")

# notifikasi
rep("function hubNotify(prev,d){\n  if(!prev||prev.status!=='playing'||!isHubGame(d))return;",
    """function hubNotify(prev,d){
  if(!prev||prev.status!=='playing'||!isHubGame(d))return;
  if(d.game==='sandi'){const mi=meIdx(d),me=mi>=0?d.players[mi]:null;
    if(d.status!=='playing')return;
    if(d.phase==='guess'&&prev.phase!=='guess'&&d.clue){if(me&&me.team===d.turnTeam&&!me.ketua)rankPop('up','🔍',`“${d.clue.w}” · ${d.clue.n}`,'Petunjuk dari ketua · giliran timmu menebak',2800);else toast(`🕵️ Tim ${TEAMNAME[d.turnTeam]}: “${d.clue.w}” · ${d.clue.n}`);}
    else if(d.turnTeam!==prev.turnTeam&&me&&me.team===d.turnTeam&&me.ketua)rankPop('up','🎖️','Giliranmu memberi petunjuk','Lihat kunci, lalu kirim satu kata + angka',2600);
    const L=d.log[d.log.length-1];if(L&&d.log.length>prev.log.length&&L.p>=0&&L.p!==mi&&/membuka/.test(L.m))toast(nm(d,L.p)+' '+L.m);
    return;}""")

# menu tuan rumah
rep("const HOST_GAMES=['pemukim','jualan','rapat','werewolf','wwk'];","const HOST_GAMES=['pemukim','jualan','rapat','werewolf','wwk','sandi'];")
rep("    if(!JY_)btns+=p.auto?",
    "    if(st.game==='sandi'){if(!p.ketua)btns+=`<button class=\"btn sm\" data-act=\"sdhk\" data-i=\"${i}\">🎖️ Jadikan ketua</button>`;}\n    else if(!JY_)btns+=p.auto?")
rep("    const tag=p.auto?'<span class=\"htag auto\">🤖 Otomatis</span>':'', crown=",
    "    const tag=st.game==='sandi'?`<span class=\"htag\">${p.team==='r'?'🔴':'🔵'} ${p.ketua?'🎖️ Ketua':'Penebak'}</span>`:p.auto?'<span class=\"htag auto\">🤖 Otomatis</span>':'', crown=")
rep("  const help=JY_?","  const help=st.game==='sandi'?'🎖️ <b>Jadikan ketua</b>: memindahkan peran ketua di tim pemain itu, misalnya kalau ketuanya terputus. ⏭ <b>Lewati</b>: giliran pindah ke tim lawan.':JY_?")
rep("  if(kind==='host'){","  if(kind==='ketua'){if(s.game!=='sandi')fail('Hanya untuk Sandi Syndicate');s.players.forEach(q=>{if(q.team===P.team)q.ketua=false;});P.ketua=true;note('🎖️ '+nm(s,i)+' kini ketua Tim '+TEAMNAME[P.team]);return;}\n  if(kind==='host'){")

rep("</style>","""/* --- Sandi Syndicate --- */
.sdcols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
@media(max-width:560px){.sdcols{grid-template-columns:1fr}}
.sdcol{border:2px solid var(--line);border-radius:14px;padding:10px;background:var(--panel2)}
.sdcol.sd-r{border-color:#d9534f88}.sdcol.sd-b{border-color:#3d7be088}
.sdcol h3{margin:0 0 8px;font-size:17px}.sdcol .seat{margin:4px 0}
.sdk{font-size:12px;font-weight:700;color:#b98f2c;margin-left:6px}
.sd-wrap{display:grid;gap:12px;max-width:900px;margin:0 auto}
.sdteams{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.sdteam{border:2px solid var(--line);border-radius:12px;padding:8px 10px;background:var(--panel2);opacity:.85}
.sdteam.on{opacity:1;box-shadow:0 0 0 2px var(--sdc),0 0 14px color-mix(in srgb,var(--sdc) 45%,transparent)}
.sdteam.sd-r{--sdc:#d9534f;border-color:#d9534f88}.sdteam.sd-b{--sdc:#3d7be0;border-color:#3d7be088}
.sdth{display:flex;justify-content:space-between;align-items:baseline;gap:6px}
.sdleft{font:800 22px/1 system-ui,sans-serif;color:var(--sdc)}.sdleft small{font-size:11px;font-weight:600;opacity:.8}
.sdmem{display:flex;flex-wrap:wrap;gap:4px 10px;font-size:13px;margin:4px 0}.sdmem .me{font-weight:800}
.sdcl{display:flex;flex-wrap:wrap;gap:4px;font-size:12px}.sdcl span{padding:1px 7px;border-radius:999px;border:1px solid var(--line);background:var(--panel)}
.sdbig{font:800 26px/1.2 Fraunces,serif;margin:2px 0 6px}.sdbig span{display:inline-grid;place-items:center;min-width:34px;height:34px;border-radius:10px;color:#fff;font:800 20px/1 system-ui,sans-serif;margin-left:6px;vertical-align:4px}
.sdbig.sd-r span{background:#d9534f}.sdbig.sd-b span{background:#3d7be0}
.sdclue-in{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}.sdclue-in input{flex:1 1 180px;min-width:0;padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--ink);font-size:16px}
.sdconfirm{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:8px 0;padding:8px 10px;border-radius:12px;border:1.5px dashed #b98f2c;background:var(--panel2)}
.sdboard{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
.sdcard{position:relative;min-height:66px;padding:16px 4px 6px;border-radius:10px;border:1.5px solid var(--line);background:var(--panel2);color:var(--ink);font:700 13px/1.15 system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;cursor:pointer;word-break:break-word;hyphens:auto}
@media(max-width:560px){.sdboard{gap:4px}.sdcard{min-height:58px;font-size:10.5px;padding:14px 2px 4px;border-radius:8px}.sdboard .sdcard.long{font-size:8.6px;letter-spacing:-.3px}}
.sdmk{position:absolute;top:3px;left:4px;font-size:8.5px;font-weight:800;color:var(--mk);opacity:.9;letter-spacing:.2px}
.sdw{display:block;overflow-wrap:anywhere}.sdcard.long{font-size:11.5px;letter-spacing:-.2px}
.sdcard.pick:hover{border-color:#b98f2c}.sdcard.sel{border-color:#ffd25e;box-shadow:0 0 0 3px #ffd25e;transform:translateY(-1px)}
.sdcard.spy.c-r{box-shadow:inset 0 0 0 3px #d9534f;background:color-mix(in srgb,#d9534f 12%,var(--panel2))}
.sdcard.spy.c-b{box-shadow:inset 0 0 0 3px #3d7be0;background:color-mix(in srgb,#3d7be0 12%,var(--panel2))}
.sdcard.spy.c-x{box-shadow:inset 0 0 0 3px #222;background:color-mix(in srgb,#000 22%,var(--panel2))}
.sdcard.spy.c-n{box-shadow:inset 0 0 0 2px #b9aa86}
.sdx{position:absolute;top:2px;right:4px;font-size:12px}
.sdcard.rev{color:#fff;border-color:transparent}.sdcard.rev .sdmk{color:#fff;opacity:.75}
.sdcard.rev.c-r{background:#d9534f}.sdcard.rev.c-b{background:#3d7be0}.sdcard.rev.c-n{background:#cdbd96;color:#3b3220}.sdcard.rev.c-n .sdmk{color:#3b3220}.sdcard.rev.c-x{background:#1d1a24}
.sdby{font-size:9px;font-weight:600;opacity:.85;margin-top:3px}
.sdlegend{margin-top:8px}
.sdpill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:700;color:#fff;background:#888}
.sdpill.c-r{background:#d9534f}.sdpill.c-b{background:#3d7be0}.sdpill.c-n{background:#cdbd96;color:#3b3220}.sdpill.c-x{background:#1d1a24}
.sdclues{display:flex;flex-wrap:wrap;gap:4px}
</style>""")
open(F,'w').write(s)
print('ok sandi')
