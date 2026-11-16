import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt} for: {old[:100]!r}')
    s=s.replace(old,new)
rep("/* ================= ONLINE PLUMBING ================= */",open('hub/wk_ui.js').read()+"\n/* ================= ONLINE PLUMBING ================= */")
rep("  if(isHubGame(cur.st))return cur.st.game==='pemukim'?renderPemukim():","  if(isHubGame(cur.st))return cur.st.game==='wwk'?renderWK():cur.st.game==='pemukim'?renderPemukim():")
rep('<option value="werewolf">🐺 Werewolf Satu Malam (3–10)</option>','<option value="werewolf">🐺 Werewolf Satu Malam (3–10)</option><option value="wwk">🐺 Werewolf Klasik (6–20)</option>')
rep("else if(e.target.value==='werewolf')t.value='300';","else if(e.target.value==='werewolf'||e.target.value==='wwk')t.value='300';")
rep("el.dataset.g==='werewolf'?'300':","el.dataset.g==='werewolf'||el.dataset.g==='wwk'?'300':")
rep("    const st=md==='pemukim'?{","    const st=md==='wwk'?{name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',game:'wwk',mode:'wwk',timer:tmr,roles:null,players:[{id:myId,nick:ui.nick||''}],v:1}\n      :md==='pemukim'?{")
rep("    case 'myrole':openRoleModal();break;","""    case 'myrole':openRoleModal();break;
    case 'wkroles':ui.wwDraft=null;wkRolesModal();break;
    case 'wkinc':ui.wwDraft.push(el.dataset.k);wkRolesModal();break;
    case 'wkdec':{const x=ui.wwDraft.lastIndexOf(el.dataset.k);if(x>=0)ui.wwDraft.splice(x,1);wkRolesModal();break;}
    case 'wkdraftauto':ui.wwDraft=wkPreset(Math.max(6,Math.min(20,st.players.length)));wkRolesModal();break;
    case 'wksel':ui.wkSel=+el.dataset.i;render();break;
    case 'wknight':if(ui.wkSel!=null){const t=ui.wkSel;ui.wkSel=null;hubMove({type:'night',t});}break;
    case 'wkskip':ui.wkSel=null;hubMove({type:'night',skip:true});break;
    case 'wkvote':if(ui.wkSel!=null){const t=ui.wkSel;ui.wkSel=null;hubMove({type:'vote',t});}break;
    case 'wkvskip':ui.wkSel=null;hubMove({type:'vote',t:-1});break;
    case 'wkshoot':if(ui.wkSel!=null){const t=ui.wkSel;ui.wkSel=null;hubMove({type:'shoot',t});}break;""")
rep("    case 'rforce':if(st.game==='werewolf'){","    case 'rforce':if(st.game==='wwk'){openModal(`<h3>⏩ Lanjutkan paksa?</h3><p class=\"mute\" style=\"font-size:14px\">${st.phase==='night'?'Malam diakhiri sekarang. Yang belum bertindak dianggap melewati.':st.phase==='day'?'Suara langsung dihitung. Yang belum memilih dianggap tidak memilih.':'Pemburu menembak secara acak.'}</p><div class=\"mbtns\"><button class=\"btn\" data-act=\"close\">Batal</button><button class=\"btn pri\" data-act=\"rforceok\">Lanjutkan</button></div>`);break;}\n      if(st.game==='werewolf'){")
rep("function tmrLeft(st){if(st&&st.game==='werewolf'&&st.phase!=='day')return null;","function tmrLeft(st){if(st&&(st.game==='werewolf'||st.game==='wwk')&&st.phase!=='day')return null;")
rep("rec:{online:{klasik:c(),duel:c(),rapat:c(),werewolf:c(),pemukim:c(),sandi:c()}","rec:{online:{klasik:c(),duel:c(),rapat:c(),werewolf:c(),wwk:c(),pemukim:c(),sandi:c()}")
rep("const T={online:{klasik:cell(),duel:cell(),rapat:cell(),werewolf:cell(),pemukim:cell(),sandi:cell()}","const T={online:{klasik:cell(),duel:cell(),rapat:cell(),werewolf:cell(),wwk:cell(),pemukim:cell(),sandi:cell()}")
rep("pmo=S.T.online.pemukim||Z, pmb=S.T.bot.pemukim||Z;\n  const tot=add(S.T.online.klasik,S.T.online.duel,rap,wwr,pmo,","pmo=S.T.online.pemukim||Z, pmb=S.T.bot.pemukim||Z, wkr=S.T.online.wwk||Z;\n  const tot=add(S.T.online.klasik,S.T.online.duel,rap,wwr,wkr,pmo,")
rep("${row('🌐 Online · 🐺 Werewolf',wwr)}","${row('🌐 Online · 🐺 Werewolf Satu Malam',wwr)}${row('🌐 Online · 🐺 Werewolf Klasik',wkr)}")
rep("${tab('v','werewolf','🐺 Werewolf')}","${tab('v','werewolf','🐺 Satu Malam')}${tab('v','wwk','🐺 Klasik')}")
rep("""<button class="btn sm ${which==='pemukim'?'on':''}" data-act="tutorial" data-w="pemukim">🏝️ Pemukim</button></div>`;
  if(which==='rapat'||which==='werewolf'||which==='pemukim'){""","""<button class="btn sm ${which==='wwk'?'on':''}" data-act="tutorial" data-w="wwk">🐺 WW Klasik</button><button class="btn sm ${which==='pemukim'?'on':''}" data-act="tutorial" data-w="pemukim">🏝️ Pemukim</button></div>`;
  if(which==='rapat'||which==='werewolf'||which==='pemukim'||which==='wwk'){""")
rep("${which==='pemukim'?pmRules():","${which==='wwk'?wkRules():which==='pemukim'?pmRules():")
rep("""data-act="tutorial" data-w="werewolf">🐺 Werewolf</button>""","""data-act="tutorial" data-w="werewolf">🐺 WW Satu Malam</button>""")
open(p,'w').write(s); print('wk ok',len(s))
