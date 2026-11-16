import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt} for: {old[:100]!r}')
    s=s.replace(old,new)
pm=open('hub/pemukim.js').read()+'\n'+open('hub/pemukim_bot.js').read()
rep("\nif(typeof module!=='undefined')module.exports={GAMES,","\n"+pm+"\nif(typeof module!=='undefined')module.exports={pmStart,pmAct,pmBotMove,pmVP,PM_G,GAMES,")
rep("/* ================= ONLINE PLUMBING ================= */",open('hub/pm_ui.js').read()+"\n/* ================= ONLINE PLUMBING ================= */")
rep("  if(isHubGame(cur.st))return cur.st.game==='werewolf'?renderWerewolf():renderRapat();","  if(isHubGame(cur.st))return cur.st.game==='pemukim'?renderPemukim():cur.st.game==='werewolf'?renderWerewolf():renderRapat();")
rep('<option value="werewolf">🐺 Werewolf Satu Malam (3–10)</option></select>','<option value="werewolf">🐺 Werewolf Satu Malam (3–10)</option><option value="pemukim">🏝️ Pemukim Nusantara (3–4)</option></select>')
rep("else if(e.target.value==='werewolf')t.value='300';","else if(e.target.value==='werewolf')t.value='300';else if(e.target.value==='pemukim')t.value='180';")
rep("    const st=md==='werewolf'?{","    const st=md==='pemukim'?{name,host:myId,createdAt:Date.now(),updatedAt:Date.now(),status:'lobby',game:'pemukim',mode:'pemukim',timer:tmr,players:[{id:myId,nick:ui.nick||''}],v:1}\n      :md==='werewolf'?{")
# clicks
rep("    case 'myrole':openRoleModal();break;","""    case 'myrole':openRoleModal();break;
    case 'pmlocal':pmLocalSetup();break;
    case 'pmlocalgo':pmLocalStart();break;
    case 'pmagain':closeModal();pmLocalSetup();break;
    case 'pmroll':pmMove({type:'roll'});break;
    case 'pmend':pmMove({type:'end'});break;
    case 'pmskipfree':pmMove({type:'skipfree'});break;
    case 'pmsteal':pmMove({type:'steal',v:+el.dataset.v});break;
    case 'pmmode':e.preventDefault();ui.pmMode=el.dataset.w&&ui.pmMode!==el.dataset.w?el.dataset.w:null;render();break;
    case 'pmbuydev':pmMove({type:'buydev'});break;
    case 'pmv':{const me=pmMe(st);if(st.phase==='setup')pmMove({type:'settle',v:+el.dataset.v});else pmMove({type:'build',what:ui.pmMode==='city'?'city':'settle',v:+el.dataset.v});break;}
    case 'pme':if(st.phase==='setup')pmMove({type:'road',e:+el.dataset.e});else pmMove({type:'build',what:'road',e:+el.dataset.e});break;
    case 'pmh':{const h=+el.dataset.h,me=pmMe(st),vic=pmVictims(st,me,h);if(vic.length>1){ui.pmRob=h;openModal(`<h3>🦹 Curi dari siapa?</h3><div class="row">${vic.map(j=>`<button class="btn" data-act="pmrobv" data-v="${j}"><span class="pmdot" style="background:${PM_COL[j]}"></span>${esc(nm(st,j))} (${pmTotal(st.players[j].res)} kartu)</button>`).join('')}</div><div class="mbtns"><button class="btn" data-act="close">Batal</button></div>`);}else pmMove({type:'robber',h});break;}
    case 'pmrobv':pmMove({type:'robber',h:ui.pmRob,v:+el.dataset.v});break;
    case 'pmdd':{const r=el.dataset.r;ui.pmDisc.g[r]=Math.max(0,ui.pmDisc.g[r]+(+el.dataset.d));pmDiscardModal();break;}
    case 'pmdiscok':{const g={...ui.pmDisc.g};ui.pmDisc=null;pmMove({type:'discard',res:g});break;}
    case 'pmtrade':pmTradeModal(el.dataset.t);break;
    case 'pmtg':ui.pmT.give=el.dataset.r;if(ui.pmT.get===ui.pmT.give)ui.pmT.get=null;pmTradeModal('bank');break;
    case 'pmtt':ui.pmT.get=el.dataset.r;pmTradeModal('bank');break;
    case 'pmbank':{const T=ui.pmT;pmMove({type:'bank',give:T.give,get:T.get});ui.pmT={give:null,get:null,og:{},ot:{}};break;}
    case 'pmo':{const o=ui.pmT[el.dataset.k],r=el.dataset.r;o[r]=Math.max(0,(o[r]||0)+(+el.dataset.d));pmTradeModal('pl');break;}
    case 'pmoffer':{const T=ui.pmT;pmMove({type:'offer',give:{...T.og},get:{...T.ot}});ui.pmT={give:null,get:null,og:{},ot:{}};break;}
    case 'pmresp':pmMove({type:'respond',yes:el.dataset.y==='1'});break;
    case 'pmaccept':pmMove({type:'accept',p:+el.dataset.p});break;
    case 'pmcancel':pmMove({type:'cancel'});break;
    case 'pmdev':pmDevModal(el.dataset.c);break;
    case 'pmy':ui.pmY=(ui.pmY||[]).concat(el.dataset.r).slice(0,2);pmDevModal('Y');break;
    case 'pmyclr':ui.pmY=[];pmDevModal('Y');break;
    case 'pmyok':{const r=ui.pmY;ui.pmY=[];pmMove({type:'dev',card:'Y',res:r});break;}
    case 'pmmono':pmMove({type:'dev',card:'M',res:el.dataset.r});break;""")
rep("const t=$('#timerIn');if(t)t.value=el.dataset.g==='rapat'?'0':el.dataset.g==='werewolf'?'300':","const t=$('#timerIn');if(t)t.value=el.dataset.g==='rapat'?'0':el.dataset.g==='werewolf'?'300':el.dataset.g==='pemukim'?'180':")
# timers
rep("  if(isHubGame(st)){const me=meIdx(st);if(cur.local||me<0||canWrite===false||l>-1200-me*700)return;",
"""  if(st.game==='pemukim'){const pend=pmPending(st);
    if(cur.local){if(!pend.includes(cur.human))return;const s=clone(st);pmTimeoutRun(s);cur.st=s;toast('⏱ Waktu habis — giliran diakhiri otomatis');if(s.status==='ended')onGameEnded(s);render();return;}
    const me=meIdx(st);if(me<0||canWrite===false)return;const mine=pend.includes(me);if(!mine&&l>-4000-me*700)return;if(pend.every(j=>st.players[j].bot))return;
    const v=st.v;ui.tmrBusy=true;commitOnline(s=>{if(s.v!==v||s.status!=='playing')throw NOOP;pmTimeoutRun(s);}).catch(()=>{}).finally(()=>{ui.tmrBusy=false;});return;}
  if(isHubGame(st)){const me=meIdx(st);if(cur.local||me<0||canWrite===false||l>-1200-me*700)return;""")
rep("const mine=isHubGame(st)?rapatPending(st).includes(meIdx(st)):","const mine=isHubGame(st)?(st.game==='pemukim'?pmPending(st).includes(pmMe(st)):rapatPending(st).includes(meIdx(st))):")
# end / stats
rep("  if(isHubGame(st))return onHubEnded(st);","  if(st.game==='pemukim')return pmOnEnded(st);\n  if(isHubGame(st))return onHubEnded(st);")
rep("rec:{online:{klasik:c(),duel:c(),rapat:c(),werewolf:c(),sandi:c()},bot:{klasik:c(),duel:c()}}","rec:{online:{klasik:c(),duel:c(),rapat:c(),werewolf:c(),pemukim:c(),sandi:c()},bot:{klasik:c(),duel:c(),pemukim:c()}}")
rep("const T={online:{klasik:cell(),duel:cell(),rapat:cell(),werewolf:cell(),sandi:cell()},bot:{klasik:cell(),duel:cell()}}","const T={online:{klasik:cell(),duel:cell(),rapat:cell(),werewolf:cell(),pemukim:cell(),sandi:cell()},bot:{klasik:cell(),duel:cell(),pemukim:cell()}}")
rep("  const Z={g:0,w:0}, rap=S.T.online.rapat||Z, wwr=S.T.online.werewolf||Z;\n  const tot=add(S.T.online.klasik,S.T.online.duel,rap,wwr,S.T.bot.klasik,S.T.bot.duel);",
    "  const Z={g:0,w:0}, rap=S.T.online.rapat||Z, wwr=S.T.online.werewolf||Z, pmo=S.T.online.pemukim||Z, pmb=S.T.bot.pemukim||Z;\n  const tot=add(S.T.online.klasik,S.T.online.duel,rap,wwr,pmo,S.T.bot.klasik,S.T.bot.duel,pmb);")
rep("${row('🌐 Online · 🐺 Werewolf',wwr)}","${row('🌐 Online · 🏝️ Pemukim',pmo)}${row('🌐 Online · 🐺 Werewolf',wwr)}")
rep("${row('🤖 Bot · ⚔️ Duel',S.T.bot.duel)}","${row('🤖 Bot · ⚔️ Duel',S.T.bot.duel)}${row('🤖 Bot · 🏝️ Pemukim',pmb)}")
rep("${tab('v','rapat','🏛️ Rapat')}","${tab('v','pemukim','🏝️ Pemukim')}${tab('v','rapat','🏛️ Rapat')}")
# bot loops guards
rep("function maybeBot(){\n  if(!cur||!cur.local||cur.botTimer)return;","function maybeBot(){\n  if(cur&&cur.st&&cur.st.game==='pemukim')return pmMaybeBot();\n  if(!cur||!cur.local||cur.botTimer)return;")
rep("function maybeOnlineBot(){\n  if(!cur||cur.local||!cur.st||canWrite===false||!myId)return;","function maybeOnlineBot(){\n  if(!cur||cur.local||!cur.st||canWrite===false||!myId||cur.st.game)return;")
# save system
rep("  const d={v:1,st:JSON.stringify(lite),human:cur.human,level:cur.level,lid:cur.lid,variant:st.mode==='duel'?'duel':'klasik',\n    n:st.players.length,round:st.round,pts:ptsOf(me),",
    "  const PMs=st.game==='pemukim';\n  const d={v:1,st:JSON.stringify(lite),human:cur.human,level:cur.level,lid:cur.lid,variant:PMs?'pemukim':st.mode==='duel'?'duel':'klasik',\n    n:st.players.length,round:st.round,pts:PMs?pmVP(st,cur.human,true):ptsOf(me),")
rep("Game lawan bot ini belum selesai (<b>${st.mode==='duel'?'⚔️ Duel':'Klasik'}</b> · ronde ${st.round} · skor kamu <b>${ptsOf(me)}</b>).",
    "Game lawan bot ini belum selesai (<b>${st.game==='pemukim'?'🏝️ Pemukim':st.mode==='duel'?'⚔️ Duel':'Klasik'}</b> · ronde ${st.round} · skor kamu <b>${st.game==='pemukim'?pmVP(st,cur.human,true):ptsOf(me)}</b>).")
rep("Simpanan lama (${old.variant==='duel'?'Duel':'Klasik'},","Simpanan lama (${old.variant==='pemukim'?'Pemukim':old.variant==='duel'?'Duel':'Klasik'},")
rep("<div class=\"bd\">${s.variant==='duel'?'⚔️ Duel':'Klasik'} · ${s.n} pemain","<div class=\"bd\">${s.variant==='pemukim'?'🏝️ Pemukim':s.variant==='duel'?'⚔️ Duel':'Klasik'} · ${s.n} pemain")
# tutorial tab
rep("""<button class="btn sm ${which==='werewolf'?'on':''}" data-act="tutorial" data-w="werewolf">🐺 Werewolf</button></div>`;
  if(which==='rapat'||which==='werewolf'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class="rules tutrules">${which==='werewolf'?wwRules():rapatRules()}</div>""",
"""<button class="btn sm ${which==='werewolf'?'on':''}" data-act="tutorial" data-w="werewolf">🐺 Werewolf</button><button class="btn sm ${which==='pemukim'?'on':''}" data-act="tutorial" data-w="pemukim">🏝️ Pemukim</button></div>`;
  if(which==='rapat'||which==='werewolf'||which==='pemukim'){openModal(`<h3>📖 Cara main & aturan</h3>${tabs}<div class="rules tutrules">${which==='pemukim'?pmRules():which==='werewolf'?wwRules():rapatRules()}</div>""")
css=""".pmwrap{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(300px,1fr);gap:14px;max-width:1240px;margin:0 auto;align-items:start}
@media(max-width:900px){.pmwrap{grid-template-columns:1fr}}
.pmbp{padding:12px}.pmboard{width:100%;height:auto;display:block;max-height:78vh;margin:0 auto;touch-action:manipulation}
.pmboard .pmhit{cursor:pointer}.pmboard .pmspot{pointer-events:none;animation:pmpulse 1.1s ease-in-out infinite}.pmwrap+* .rki .nm,.rki .nm{min-width:0}.rki .nm .bd{white-space:normal}
.pmboard .pmhl{cursor:pointer;stroke:#fff;stroke-width:4;animation:pmpulse 1.1s ease-in-out infinite}
@keyframes pmpulse{50%{opacity:.45}}
.pmside{display:grid;gap:12px;min-width:0}
.pmdot{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:-1px;border:1.5px solid rgba(0,0,0,.4)}.pmdot.sm{width:9px;height:9px;margin-right:4px}
.pmhand{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin:10px 0}
.pmres{display:flex;flex-direction:column;align-items:center;padding:7px 2px;border-radius:10px;background:var(--panel2);border:1px solid var(--line)}
.pmres span{font-size:22px;line-height:1.1}.pmres b{font-size:18px;font-family:Fraunces,serif}.pmres small{font-size:10.5px;color:var(--mute)}
.pmres.r-L{border-color:#2f7d4f}.pmres.r-B{border-color:#c0613a}.pmres.r-W{border-color:#8fc45a}.pmres.r-G{border-color:#e3bd3e}.pmres.r-O{border-color:#8b93a1}
.pmdevs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.pmdev{font:inherit;font-size:12.5px;font-weight:700;padding:6px 9px;border-radius:9px;background:var(--panel2);border:1px solid var(--line);color:var(--ink);opacity:.75}
.pmdev.ok{opacity:1;border-color:var(--gold);cursor:pointer;background:rgba(230,184,76,.15)}.pmdev small{font-weight:400;color:var(--mute)}
.pmact{display:grid;gap:8px;margin-top:6px}.pmbtns{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.pmbtns .btn{display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 6px}.pmbtns .btn.on{outline:2px solid var(--gold)}
.pmcost{font-size:12px;letter-spacing:1px}
.btn.big{padding:14px 22px;font-size:17px}
.pmdice{font-size:26px;line-height:1;display:inline-flex;align-items:center;gap:4px}.pmdice b{font-size:16px;font-family:Fraunces,serif;margin-left:4px}
.pmpls{display:grid;gap:6px}.pmpl{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:10px;background:var(--panel2);border:1px solid var(--line)}
.pmpl.turn{border-color:var(--gold);box-shadow:0 0 0 2px rgba(230,184,76,.25)}.pmpl.me{box-shadow:inset 3px 0 0 var(--gold)}
.pmpn{flex:1;min-width:0}.pmpn .bd{font-size:12px}.pmvp{font-family:Fraunces,serif;font-size:24px;font-weight:700;text-align:center;line-height:1}.pmvp small{display:block;font-size:10px;color:var(--mute);font-family:inherit}
.pmlast{margin-top:6px}
.pmoffer{border-color:var(--gold)}
.pmpick{display:flex;gap:6px;flex-wrap:wrap}.pmpick .btn.on{outline:2px solid var(--gold)}.pmpick small{font-weight:400;opacity:.8}
.pmstep{display:grid;gap:5px}.pmsrow{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:4px 8px;border-radius:8px;background:var(--panel2)}
.pmtwo{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:560px){.pmtwo{grid-template-columns:1fr}}
body.light .rtag.o{"""
rep("body.light .rtag.o{",css)
open(p,'w').write(s)
print('pm ok',len(s))
