import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt} for: {old[:90]!r}')
    s=s.replace(old,new)
content=open('hub/content.js').read(); eng=open('hub/engines.js').read(); ui=open('hub/rapat_ui.js').read()+'\n'+open('hub/ww_ui.js').read()
# 1 engines into first script
rep("if(typeof module!=='undefined')module.exports={duelMaster,",
    content+"\n"+eng+"\nif(typeof module!=='undefined')module.exports={GAMES,gameOf,isHubGame,hubAct,hubStart,hubWinners,rapatStart,rapatAct,rapatRoles,rapatSide,sandiStart,sandiAct,MISSIONS,TERMS,MK_INFO,packTerms,termOf,RAPAT_SIZES,RAPAT_OKNUM,ROLE,obf,deobf,duelMaster,")
# 2 UI module before ONLINE PLUMBING
rep("/* ================= ONLINE PLUMBING ================= */", ui+"\n/* ================= ONLINE PLUMBING ================= */")
# 3 render branches
rep("function renderWaiting(){\n  const st=cur.st, mi=meIdx(st), isHost=st.host===myId;",
    "function renderWaiting(){\n  if(isHubGame(cur.st))return renderWaitingHub();\n  const st=cur.st, mi=meIdx(st), isHost=st.host===myId;")
rep("function renderGame(){\n  if(cur.st.mode==='duel')return renderDuel();",
    "function renderGame(){\n  if(isHubGame(cur.st))return cur.st.game==='werewolf'?renderWerewolf():renderRapat();\n  if(cur.st.mode==='duel')return renderDuel();")
# 4 lobby hub grid + game select
rep('$(\'#app\').innerHTML=`<div id="lobbyShell" class="lobby">\n',
    '$(\'#app\').innerHTML=`<div id="lobbyShell" class="lobby">\n      ${hubGridHTML()}\n')
rep('''>Mode<select id="modeIn"><option value="klasik">💎 Klasik (2–4 pemain)</option><option value="duel">⚔️ Duel (2 pemain)</option></select>''',
    '''>Permainan<select id="modeIn"><option value="klasik">💎 Permata Klasik (2–4)</option><option value="duel">⚔️ Permata Duel (2)</option><option value="rapat">🏛️ Rapat Rahasia (5–10)</option><option value="werewolf">🐺 Werewolf Satu Malam (3–10)</option></select>''')
rep("""<b>${esc(g.name||'Meja')}</b>${g.mode==='duel'?""",
    """<b>${esc(g.name||'Meja')}</b>${isHubGame(g)?`<span class="pill playing" style="background:#1d3b66;color:#dbe8ff">${GAMES[g.game].icon} ${GAMES[g.game].name}</span>`:''}${g.mode==='duel'?""")
rep("${(g.players||[]).length}/${g.mode==='duel'?2:4}","${(g.players||[]).length}/${(GAMES[gameOf(g)]||{max:4}).max}")
rep("""function inviteText(st,gid){return `Ayo main Saudagar Permata""",
    """function inviteText(st,gid){if(st&&isHubGame(st)){const G=GAMES[st.game];return `Ayo main ${G.name} ${G.icon} (${G.min}–${G.max} pemain)! Masuk ke meja "${st.name||'Meja'}" di sini, lalu ketuk "Duduk di meja ini": ${tableLink(gid)}`;}return `Ayo main Saudagar Permata""")
# 5 createTable
rep("""    const st={name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',mode:md==='duel'?'duel':'klasik',timer:tmr,players:[newPlayer(myId,ui.nick)],v:1};""",
    """    const st=md==='werewolf'?{name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',game:'werewolf',mode:'werewolf',timer:tmr,roles:null,players:[{id:myId,nick:ui.nick||''}],v:1}
      :md==='rapat'?{name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',game:'rapat',mode:'rapat',timer:tmr,special:true,players:[{id:myId,nick:ui.nick||''}],v:1}
      :{name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',mode:md==='duel'?'duel':'klasik',timer:tmr,players:[newPlayer(myId,ui.nick)],v:1};""")
# 6 tableAction
rep("      const maxP=st.mode==='duel'?2:4;\n      if(kind==='join'){ if(i>=0)return; if(st.players.length>=maxP){const b=st.players.map(p=>p.bot).lastIndexOf(true);if(b<0)fail('Meja sudah penuh');st.players.splice(b,1);} st.players.push(newPlayer(myId,ui.nick)); }",
    "      const hub=isHubGame(st), maxP=hub?GAMES[st.game].max:(st.mode==='duel'?2:4);\n      if(kind==='join'){ if(i>=0)return; if(st.players.length>=maxP){const b=st.players.map(p=>p.bot).lastIndexOf(true);if(b<0)fail('Meja sudah penuh');st.players.splice(b,1);} st.players.push(hub?{id:myId,nick:ui.nick||''}:newPlayer(myId,ui.nick)); }\n      else if(kind==='special'){ if(st.host!==myId)fail('Hanya tuan rumah'); st.special=!!ui.spVal; }\n      else if(kind==='wwroles'){ if(st.host!==myId)fail('Hanya tuan rumah'); st.roles=(ui.wwDraft||[]).slice(); }\n      else if(kind==='wwauto'){ if(st.host!==myId)fail('Hanya tuan rumah'); st.roles=null; }\n      else if(kind==='start'&&hub){ if(st.host!==myId)fail('Hanya tuan rumah yang bisa memulai'); if(st.players.length<GAMES[st.game].min)fail('Butuh minimal '+GAMES[st.game].min+' pemain'); shuffle(st.players); st.players.forEach(p=>{if(!p.nick&&NAMES[p.id])p.nick=NAMES[p.id];}); hubStart(st); }")
# 7 change listeners
rep("  if(e.target.id==='obLv'){ui.obLevel=e.target.value;}});",
    "  if(e.target.id==='obLv'){ui.obLevel=e.target.value;}\n  if(e.target.id==='spSel'){ui.spVal=e.target.checked;tableAction('special');}\n  if(e.target.id==='modeIn'){const t=$('#timerIn');if(t){if(e.target.value==='rapat')t.value='0';else if(e.target.value==='werewolf')t.value='300';else if(t.value==='0')t.value='180';}}});")
# 8 click acts
rep("    case 'create':createTable();break;",
    """    case 'create':createTable();break;
    case 'hubnew':{const m=$('#modeIn');if(m)m.value=el.dataset.g;const t=$('#timerIn');if(t)t.value=el.dataset.g==='rapat'?'0':el.dataset.g==='werewolf'?'300':(t.value==='0'?'180':t.value);createTable();break;}
    case 'myrole':openRoleModal();break;
    case 'wwroles':ui.wwDraft=null;wwRolesModal();break;
    case 'wwinc':case 'wwdec':{const k=el.dataset.k,step=k==='K'?2:1;ui.wwDraft=ui.wwDraft||[];if(a==='wwinc'){for(let j=0;j<step;j++)ui.wwDraft.push(k);}else{for(let j=0;j<step;j++){const x=ui.wwDraft.lastIndexOf(k);if(x>=0)ui.wwDraft.splice(x,1);}}wwRolesModal();break;}
    case 'wwdraftauto':ui.wwDraft=wwPreset(Math.max(3,Math.min(10,st.players.length)));wwRolesModal();break;
    case 'wwsave':closeModal();tableAction('wwroles');break;
    case 'wwauto':tableAction('wwauto');break;
    case 'wpick':{const i=+el.dataset.i,need=wwNeeds(st,meIdx(st));if(!need||!need.p)return;ui.wsel.c=[];if(ui.wsel.p.includes(i))ui.wsel.p=ui.wsel.p.filter(x=>x!==i);else{ui.wsel.p=[...ui.wsel.p,i].slice(-need.p);}render();break;}
    case 'wcen':{const c=+el.dataset.c,need=wwNeeds(st,meIdx(st));if(!need||!need.c)return;ui.wsel.p=[];if(ui.wsel.c.includes(c))ui.wsel.c=ui.wsel.c.filter(x=>x!==c);else{ui.wsel.c=[...ui.wsel.c,c].slice(-need.c);}render();break;}
    case 'wclr':ui.wsel={p:[],c:[]};render();break;
    case 'wskip':hubMove({type:'night',skip:true});break;
    case 'wnight':{const r=wwDeal(st)[meIdx(st)],S=ui.wsel,mv={type:'night'};
      if(r==='W'||r==='D')mv.c=S.c[0];else if(r==='S'){if(S.p.length)mv.p=S.p[0];else mv.c=S.c;}else if(r==='R')mv.p=S.p[0];else if(r==='T')mv.ps=S.p;
      hubMove(mv);break;}
    case 'wvote':ui.wvote=+el.dataset.i;render();break;
    case 'wvoteok':if(ui.wvote!=null){const t=ui.wvote;ui.wvote=null;hubMove({type:'vote',target:t});}break;
    case 'rmis':missionModal(+el.dataset.j);break;
    case 'rvhist':voteHistModal();break;
    case 'rpick':{const i=+el.dataset.i,mis=st.missions[st.mi];ui.rpick=ui.rpick||[];if(ui.rpick.includes(i))ui.rpick=ui.rpick.filter(x=>x!==i);else{if(ui.rpick.length>=mis.size)return toast('Tim proyek ini '+mis.size+' orang');ui.rpick=[...ui.rpick,i];}render();break;}
    case 'rpickclr':ui.rpick=[];render();break;
    case 'rpropose':hubMove({type:'propose',team:[...(ui.rpick||[])]});break;
    case 'rvote':hubMove({type:'vote',yes:el.dataset.y==='1'});break;
    case 'rplay':{const f=el.dataset.c==='f';openModal(`<h3>${f?'💣 Kirim kartu Sabotase?':'✅ Kirim kartu Dukung?'}</h3><p class="mute" style="font-size:14px">Pilihan tidak bisa diubah. Yang diumumkan hanya jumlah sabotase, bukan siapa pengirimnya.</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn ${f?'danger':'ok'}" data-act="rplayok" data-c="${f?'f':'s'}">${f?'Sabotase':'Dukung'}</button></div>`);break;}
    case 'rplayok':hubMove({type:'play',card:el.dataset.c});break;
    case 'rtgt':ui.rtarget=+el.dataset.i;render();break;
    case 'rshootok':if(ui.rtarget==null)return;openModal(`<h3>🎯 Tuduh ${esc(nm(st,ui.rtarget))}?</h3><p class="mute" style="font-size:14px">Kalau dia Auditor Internal, Oknum menang. Kalau salah, Integritas menang. Hanya satu kesempatan.</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn danger" data-act="rshootgo">Tuduh</button></div>`);break;
    case 'rshootgo':hubMove({type:'shoot',target:ui.rtarget});break;
    case 'rforce':if(st.game==='werewolf'){openModal(st.phase==='night'?`<h3>⏩ Akhiri malam sekarang?</h3><p class="mute" style="font-size:14px">Untuk pemain yang terputus atau terlalu lama. Pemain yang belum bertindak dianggap melewati kemampuannya (Pemabuk menukar dengan kartu tengah acak).</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="rforceok">Akhiri malam</button></div>`:`<h3>⏩ Akhiri diskusi sekarang?</h3><p class="mute" style="font-size:14px">Suara langsung dihitung. ${st.players.length-st.voted.length} pemain yang belum memilih dianggap tidak memilih siapa pun.</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="rforceok">Hitung suara</button></div>`);break;}
      openModal(`<h3>⏩ Lanjutkan paksa?</h3><p class="mute" style="font-size:14px">Untuk pemain yang terputus atau tidak merespons. Yang belum masuk dihitung otomatis: usulan tim diisi berurutan, suara dihitung Setuju, kartu proyek dihitung Dukung, tebakan Dalang diacak.</p><div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="rforceok">Lanjutkan</button></div>`);break;
    case 'rforceok':{closeModal();if(ui.busy)return;ui.busy=true;const ph=st.phase,ta=st.turnAt;commitOnline(s=>{if(s.status!=='playing'||s.phase!==ph||s.turnAt!==ta)throw NOOP;hubAct(s,meIdx(s),{type:'timeout',forced:true});}).catch(e=>{if(!e.noop)toast(e.message||'Gagal');}).finally(()=>{ui.busy=false;});break;}""")
# 9 timer
rep("  if(l==null||l>0||cur.guided||ui.tmrBusy)return;\n  const p=st.players[st.turn]; if(!p||p.bot)return;",
    """  if(l==null||l>0||cur.guided||ui.tmrBusy)return;
  if(isHubGame(st)){const me=meIdx(st);if(cur.local||me<0||canWrite===false||l>-1200-me*700)return;
    const ph=st.phase,ta=st.turnAt;ui.tmrBusy=true;
    commitOnline(s=>{if(s.status!=='playing'||s.phase!==ph||s.turnAt!==ta)throw NOOP;hubAct(s,meIdx(s),{type:'timeout'});}).catch(()=>{}).finally(()=>{ui.tmrBusy=false;});return;}
  const p=st.players[st.turn]; if(!p||p.bot)return;""")
rep("function timerHTML(st){const l=tmrLeft(st);if(l==null)return '';const mine=st.turn===actor(st);",
    "function timerHTML(st){const l=tmrLeft(st);if(l==null)return '';const mine=isHubGame(st)?rapatPending(st).includes(meIdx(st)):st.turn===actor(st);")
rep("function tmrLeft(st){return st&&st.timer","function tmrLeft(st){if(st&&st.game==='werewolf'&&st.phase!=='day')return null;return st&&st.timer")
# 10 applyState notify + end
rep("  if(prev&&prev.status==='playing'&&data.status==='ended')toast('Permainan selesai!');\n  render();",
    "  if(isHubGame(data))hubNotify(prev,data);\n  if(prev&&prev.status==='playing'&&data.status==='ended')toast('Permainan selesai!');\n  render();")
rep("  if(!db||!myId||isGuest())return;\n  const rid=cur.local?cur.lid:'g_'+cur.gid;",
    "  if(!db||!myId||isGuest())return;\n  if(isHubGame(st))return onHubEnded(st);\n  const rid=cur.local?cur.lid:'g_'+cur.gid;")
rep("function openEndModal(){\n  const st=cur.st; if(!st||st.status!=='ended')return;",
    "function openEndModal(){\n  const st=cur.st; if(!st||st.status!=='ended')return;\n  if(isHubGame(st))return openHubEnd();")
# 11 stats
rep("rec:{online:{klasik:c(),duel:c()},bot:{klasik:c(),duel:c()}}","rec:{online:{klasik:c(),duel:c(),rapat:c(),werewolf:c(),sandi:c()},bot:{klasik:c(),duel:c()}}")
rep("  const won=me.rank===1, m=r.mode==='online'?'online':'bot', v=r.variant==='duel'?'duel':'klasik';\n  s.rec[m][v].g++; if(won)s.rec[m][v].w++;",
    "  const won=me.rank===1, m=r.mode==='online'?'online':'bot', v=vOf(r), perm=v==='klasik'||v==='duel';\n  if(!s.rec[m][v])s.rec[m][v]={g:0,w:0}; s.rec[m][v].g++; if(won)s.rec[m][v].w++;")
rep("s.streak=won?s.streak+1:0; s.best=Math.max(s.best,s.streak); s.top=Math.max(s.top,me.pts||0);\n  if(m==='online'){",
    "s.streak=won?s.streak+1:0; s.best=Math.max(s.best,s.streak); if(perm)s.top=Math.max(s.top,me.pts||0);\n  if(m==='online'&&perm){")
rep("const T={online:{klasik:cell(),duel:cell()},bot:{klasik:cell(),duel:cell()}}","const T={online:{klasik:cell(),duel:cell(),rapat:cell(),werewolf:cell(),sandi:cell()},bot:{klasik:cell(),duel:cell()}}")
rep("  rows.forEach(r=>{const m=r.mode==='online'?'online':'bot',v=r.variant==='duel'?'duel':'klasik',won=meOf(r).rank===1;\n    T[m][v].g++;",
    "  rows.forEach(r=>{const m=r.mode==='online'?'online':'bot',v=vOf(r),won=meOf(r).rank===1;\n    if(!T[m][v])T[m][v]=cell(); T[m][v].g++;")
rep("  const tot=add(S.T.online.klasik,S.T.online.duel,S.T.bot.klasik,S.T.bot.duel);",
    "  const Z={g:0,w:0}, rap=S.T.online.rapat||Z, wwr=S.T.online.werewolf||Z;\n  const tot=add(S.T.online.klasik,S.T.online.duel,rap,wwr,S.T.bot.klasik,S.T.bot.duel);")
rep("${row('🌐 Online · Klasik',S.T.online.klasik)}${row('🌐 Online · ⚔️ Duel',S.T.online.duel)}",
    "${row('🌐 Online · Klasik',S.T.online.klasik)}${row('🌐 Online · ⚔️ Duel',S.T.online.duel)}${row('🌐 Online · 🏛️ Rapat Rahasia',rap)}${row('🌐 Online · 🐺 Werewolf',wwr)}")
# 12 history
rep("const rows=all.filter(r=>(f.m==='all'||(f.m==='online'?r.mode==='online':r.mode!=='online'))&&(f.v==='all'||(r.variant==='duel'?'duel':'klasik')===f.v));",
    "const rows=all.filter(r=>(f.m==='all'||(f.m==='online'?r.mode==='online':r.mode!=='online'))&&(f.v==='all'||vOf(r)===f.v));")
rep("${tab('v','all','Semua mode')}${tab('v','klasik','💎 Klasik')}${tab('v','duel','⚔️ Duel')}",
    "${tab('v','all','Semua game')}${tab('v','klasik','💎 Klasik')}${tab('v','duel','⚔️ Duel')}${tab('v','rapat','🏛️ Rapat')}${tab('v','werewolf','🐺 Werewolf')}")
rep("""      return `<div class="hrow" data-act="hdetail" data-id="${esc(r._id)}"><div style="min-width:0"><b>${me.rank===1?'🏆 Menang':'Peringkat '+me.rank}</b> <span class="bd">· ${r.variant==='duel'?'⚔️ Duel':'💎 Klasik'} · ${r.mode==='online'?r.players.length+' pemain online':'lawan bot ('+(LVNAME[r.level]||'')+')'} · ${r.rounds} ronde · ${fmtDate(r.endedAt)}</span>""",
    """      const hub=hubV(r);
      return `<div class="hrow" data-act="hdetail" data-id="${esc(r._id)}"><div style="min-width:0"><b>${me.rank===1?'🏆 Menang':hub?'Kalah':'Peringkat '+me.rank}</b> <span class="bd">· ${VLAB[vOf(r)]} · ${r.mode==='online'?r.players.length+' pemain online':'lawan bot ('+(LVNAME[r.level]||'')+')'} · ${vOf(r)==='werewolf'?'1 malam':r.rounds+' '+(hub?'proyek':'ronde')} · ${fmtDate(r.endedAt)}</span>""")
rep("""<div style="text-align:right;flex:none"><div class="bigpts">${aw?'+'+aw.total:'—'}</div><div class="bd">${me.pts} poin game</div></div></div>`;}).join('')""",
    """<div style="text-align:right;flex:none"><div class="bigpts">${aw?'+'+aw.total:'—'}</div><div class="bd">${hub?roleName(vOf(r),me.role):me.pts+' poin game'}</div></div></div>`;}).join('')""")
rep("""function openResultDetail(id){
  const r=ui.hist&&ui.hist[id]; if(!r)return;""",
    """function openResultDetail(id){
  const r=ui.hist&&ui.hist[id]; if(!r)return;
  if(hubV(r)){const ps=[...r.players].sort((a,b)=>a.rank-b.rank), WWv=vOf(r)==='werewolf';
    openModal(`<h3>${WWv?'🐺 Werewolf Satu Malam':'🏛️ Rapat Rahasia · '+(r.winner==='I'?'Integritas menang':'Oknum menang')}</h3><p class="bd" style="margin:0 0 10px">${fmtDate(r.endedAt)}${r.name?' · '+esc(r.name):''} · ${esc(r.winBy||'')}</p>
      <table class="lb"><tr><th>Pemain</th><th>Peran</th><th>Hasil</th></tr>${ps.map(p=>`<tr class="${p.id===myId?'me':''}"><td>${esc(pname(p))}</td><td>${roleName(vOf(r),p.role)||'—'}${WWv&&p.orig&&p.orig!==p.role?' <span class="bd">(awal: '+roleName('werewolf',p.orig)+')</span>':''}${p.dead?' ☠️':''}</td><td>${p.rank===1?'🏆 Menang':'Kalah'}</td></tr>`).join('')}</table>
      <h3 style="font-size:15px;margin:14px 0 6px">Jalannya permainan</h3><div class="log" style="max-height:240px;margin-top:0">${(r.log||[]).map(l=>`<div>${l.p>=0&&r.players[l.p]?`<b>${esc(pname(r.players[l.p]))}</b> `:''}${esc(l.m)}</div>`).join('')}</div>
      <div class="mbtns"><button class="btn" data-act="history">← Riwayat</button><button class="btn pri" data-act="close">Tutup</button></div>`);return;}""")
rep("""<b>${me.rank===1?'🏆 Menang':'Peringkat '+me.rank}</b> <span class="bd">· ${r.variant==='duel'?'⚔️':'💎'} ${r.mode==='online'?r.players.length+' pemain':'lawan bot'} · ${r.rounds} ronde · ${fmtDate(r.endedAt)}</span></div><div class="bigpts" style="font-size:17px;flex:none">${aw?'+'+aw.total:me.pts+' p'}</div>""",
    """<b>${me.rank===1?'🏆 Menang':hubV(r)?'Kalah':'Peringkat '+me.rank}</b> <span class="bd">· ${VLAB[vOf(r)].split(' ')[0]} ${r.mode==='online'?r.players.length+' pemain':'lawan bot'} · ${vOf(r)==='werewolf'?'1 malam':r.rounds+' '+(vOf(r)==='rapat'?'proyek':'ronde')} · ${fmtDate(r.endedAt)}</span></div><div class="bigpts" style="font-size:17px;flex:none">${aw?'+'+aw.total:hubV(r)?'—':me.pts+' p'}</div>""")
# 13 tutorial tabs
rep("""function openTutorial(which){
  which=which||(cur&&cur.st&&cur.st.mode==='duel'?'duel':'klasik');
  const T=TUTORIALS[which];
  openModal(`<h3>🎬 Tutorial & aturan</h3>
    <div class="tabs"><button class="btn sm ${which==='klasik'?'on':''}" data-act="tutorial" data-w="klasik">💎 Klasik</button><button class="btn sm ${which==='duel'?'on':''}" data-act="tutorial" data-w="duel">⚔️ Duel</button></div>""",
    """function openTutorial(which){
  which=which||(cur&&cur.st&&isHubGame(cur.st)?cur.st.game:cur&&cur.st&&cur.st.mode==='duel'?'duel':'klasik');
  const tabs=`<div class="tabs"><button class="btn sm ${which==='klasik'?'on':''}" data-act="tutorial" data-w="klasik">💎 Klasik</button><button class="btn sm ${which==='duel'?'on':''}" data-act="tutorial" data-w="duel">⚔️ Duel</button><button class="btn sm ${which==='rapat'?'on':''}" data-act="tutorial" data-w="rapat">🏛️ Rapat Rahasia</button><button class="btn sm ${which==='werewolf'?'on':''}" data-act="tutorial" data-w="werewolf">🐺 Werewolf</button></div>`;
  if(which==='rapat'||which==='werewolf'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class="rules tutrules">${which==='werewolf'?wwRules():rapatRules()}</div><div class="mbtns"><button class="btn pri" data-act="close">Siap main!</button></div>`);return;}
  const T=TUTORIALS[which];
  openModal(`<h3>🎬 Tutorial & aturan</h3>
    ${tabs}""")
# 14 CSS
css=""".hubp{grid-column:1/-1}
.hubgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:12px}
.hubcard{display:flex;flex-direction:column;gap:8px;padding:14px;border-radius:14px;background:var(--panel2);border:1px solid var(--line)}
.hubcard.soon{opacity:.72}.hubcard .hh{display:flex;gap:10px;align-items:center}.hubcard .hi{font-size:32px;line-height:1}
.hubcard .hmeta{display:flex;gap:12px;flex-wrap:wrap;font-size:12.5px;color:var(--mute)}
.hubcard .hd{margin:0;font-size:13.5px;line-height:1.5}.hubcard .hbt{gap:6px;margin-top:auto}
.hmk{display:flex;gap:6px;flex-wrap:wrap}
.mkchip{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:99px;background:color-mix(in srgb,var(--mk) 24%,transparent);border:1px solid var(--mk);color:var(--ink);white-space:nowrap}
.soonpill{margin:0;background:#3a3466;color:#cfc8ea}
.chk{display:inline-flex;gap:6px;align-items:center;font-size:14px;cursor:pointer}
.rp-wrap{max-width:1000px;margin:0 auto;display:grid;gap:12px}
.rmis-row{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}
.rmis{padding:10px;border-radius:12px;background:var(--panel2);border:1px solid var(--line);display:flex;flex-direction:column;gap:5px;cursor:pointer;min-width:0;align-items:flex-start}
.rmis .rn{font-family:Fraunces,serif;font-weight:700;font-size:20px;line-height:1}
.rmis .rt{font-size:12.5px;font-weight:700;line-height:1.3}.rmis .rsz{font-size:12px;color:var(--mute)}
.rmis .mkchip{max-width:100%;overflow:hidden;text-overflow:ellipsis}
.rmis.cur{border-color:var(--gold);box-shadow:0 0 0 2px rgba(230,184,76,.35)}
.rmis.ok{background:rgba(67,211,145,.14);border-color:#35b07a}.rmis.bad{background:rgba(224,67,79,.16);border-color:#e0434f}
.rrej{display:flex;gap:5px;align-items:center}.rrej i{width:14px;height:14px;border-radius:50%;border:2px solid var(--bad);display:inline-block}.rrej i.on{background:var(--bad)}
.rpl{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px}
.rpchip{padding:10px;border-radius:12px;background:var(--panel2);border:1px solid var(--line);display:flex;flex-direction:column;gap:5px;min-width:0}
.rpchip .rh{display:flex;align-items:center;gap:6px;min-width:0}.rpchip .rh b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rpchip .rno{font-size:11px;font-weight:700;color:var(--mute)}
.rpchip .rbadges{display:flex;gap:4px;flex-wrap:wrap;min-height:4px}
.rpchip.lead{border-color:var(--gold)}.rpchip.team{background:rgba(59,123,224,.22);border-color:#3b7be0}
.rpchip.pick{cursor:pointer}.rpchip.pick:hover{border-color:rgba(255,255,255,.4)}
.rpchip.tgt{outline:3px solid var(--bad)}.rpchip.me{box-shadow:inset 3px 0 0 var(--gold)}
.rpchip.pend .rbd{color:var(--gold)}
.rtag{font-size:11px;font-weight:700;padding:2px 7px;border-radius:99px;display:inline-block;white-space:nowrap}
.rtag.o{background:#5a2330;color:#ffd6db}.rtag.i{background:#1d3b66;color:#dbe8ff}.rtag.ld{background:rgba(230,184,76,.22);color:var(--gold)}.rtag.tm{background:#1d3b66;color:#dbe8ff}
.rbd{font-size:12.5px;color:var(--mute);line-height:1.45}
.ract{display:flex;flex-direction:column;gap:10px;align-items:flex-start;font-size:15px;line-height:1.5}
.rbig{display:flex;gap:10px;flex-wrap:wrap}.rbig .btn{padding:13px 22px;font-size:16px}
.rolecard{text-align:center;padding:18px;border-radius:16px;border:2px solid}
.rolecard.i{border-color:#3b7be0;background:rgba(59,123,224,.12)}.rolecard.o{border-color:#e0434f;background:rgba(224,67,79,.12)}
.rolecard .ri{font-size:54px;line-height:1.1}.rknow{font-size:14.5px;margin:10px 0 0}
table.vh td,table.vh th{text-align:center;padding:4px 6px;font-size:12.5px}
@media(max-width:700px){.rmis-row{gap:4px}.rmis{padding:6px;align-items:center}.rmis .rt,.rmis .mkchip{display:none}.rmis .rsz{font-size:11px}.rpl{grid-template-columns:repeat(2,minmax(0,1fr))}.rbig .btn{flex:1}}
.wwchips{display:flex;gap:5px;flex-wrap:wrap}
.wwr{display:inline-block;font-size:12px;font-weight:700;padding:3px 8px;border-radius:99px;white-space:nowrap;border:1px solid}
.wwr.t-v{background:rgba(59,123,224,.18);border-color:#3b7be0;color:#dbe8ff}.wwr.t-w{background:rgba(224,67,79,.2);border-color:#e0434f;color:#ffd6db}.wwr.t-n{background:rgba(201,140,60,.22);border-color:#c98c3c;color:#ffe6c2}
body.light .wwr.t-v{color:#1d3b66}body.light .wwr.t-w{color:#7a1d2a}body.light .wwr.t-n{color:#6b4314}
.wwlist{display:grid;gap:6px;margin:6px 0}.wwrow{display:grid;grid-template-columns:150px 1fr auto;gap:10px;align-items:center;padding:6px 8px;border-radius:10px;background:var(--panel2)}
.wwrow .wwd{font-size:12.5px;line-height:1.4}.wwct{display:flex;gap:6px;align-items:center}.wwct b{min-width:16px;text-align:center}
@media(max-width:560px){.wwrow{grid-template-columns:1fr auto}.wwrow .wwd{grid-column:1/-1;grid-row:2}}
.wwme{display:flex;gap:14px;align-items:center;padding:12px 14px;border-radius:14px;border:2px solid;width:100%}
.wwme .wi{font-size:46px;line-height:1}.wwme.t-v{border-color:#3b7be0;background:rgba(59,123,224,.12)}.wwme.t-w{border-color:#e0434f;background:rgba(224,67,79,.12)}.wwme.t-n{border-color:#c98c3c;background:rgba(201,140,60,.12)}
.wwinfo{display:grid;gap:4px;padding:10px 12px;border-radius:12px;background:var(--panel2);border:1px dashed var(--line);width:100%;font-size:14.5px}
.wwcen{display:flex;gap:8px;flex-wrap:wrap}
.wwcard{width:110px;min-height:80px;border-radius:12px;background:var(--panel2);border:1px solid var(--line);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:12.5px;font-weight:700;text-align:center;padding:6px}
.wwcard .wi{font-size:26px}.wwcard.pick{cursor:pointer;border-style:dashed;border-color:var(--gold)}.wwcard.sel{background:rgba(230,184,76,.22);border:2px solid var(--gold)}
.wwcard.open.t-w{border-color:#e0434f}.wwcard.open.t-v{border-color:#3b7be0}.wwcard.open.t-n{border-color:#c98c3c}
.rpchip.dead{opacity:.6;background:rgba(224,67,79,.12)}
.wwcomp{margin:2px 0 12px}
.ww.night .ract{background:linear-gradient(180deg,rgba(40,40,110,.55),var(--panel))}
body.light .rtag.o{background:#f6d5d9;color:#7a1d2a}body.light .rtag.i,body.light .rtag.tm{background:#d9e6fb;color:#1d3b66}
</style>"""
rep("</style>",css)
open(p,'w').write(s)
print('ok',len(s))
