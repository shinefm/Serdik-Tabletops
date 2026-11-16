import sys
p='saudagar-permata.html'; s=open(p).read()
def rep(a,b,c=1):
    global s
    if s.count(a)!=c: sys.exit('COUNT '+str(s.count(a))+' '+a[:80])
    s=s.replace(a,b)
rep("/* ================= ONLINE PLUMBING ================= */",open('hub/gate_ui.js').read()+"\n/* ================= ONLINE PLUMBING ================= */")
rep("      ${hubGridHTML()}","      <div id=\"gateSlot\">${accessGateHTML()}</div>${hubGridHTML()}")
rep("  $('#onlineNote').innerHTML=note;","  $('#onlineNote').innerHTML=note;\n  {const gs=$('#gateSlot');if(gs){const h=accessGateHTML();if(ui.gateH!==h){ui.gateH=h;gs.innerHTML=h;}}}")
rep("    case 'copylink':{","""    case 'gatecopy':{const t=pageLink();try{navigator.clipboard.writeText(t).then(()=>toast('Link disalin — tempel di Chrome/Safari setelah login'),()=>toast(t));}catch(err){toast(t);}break;}
    case 'gatemail':{const t=ui.email||'';try{navigator.clipboard.writeText(t).then(()=>toast('Email disalin — kirim ke tuan rumah'),()=>toast(t));}catch(err){toast(t);}break;}
    case 'copylink':{""")
rep("""      <button class="btn" data-act="copylink">🔗 Salin link</button>
    </div>""","""      <button class="btn" data-act="copylink">🔗 Salin link</button>
    </div>
    <div class="bd" style="margin-top:6px">ℹ️ Teman harus membuka link di Chrome/Safari, <b>login ke Claude</b>, dan emailnya <b>sudah kamu undang</b> lewat Share di claude.ai (akses jangan “Viewer”).</div>""")
rep("body.light .rtag.o{",""".gate a.btn{text-decoration:none}#gateSlot{grid-column:1/-1}#gateSlot:empty{display:none}.gate{border:2px solid var(--gold);background:linear-gradient(180deg,rgba(230,184,76,.14),var(--panel))}
.gate .gh{display:flex;gap:12px;align-items:flex-start;margin-bottom:10px}.gate .gi{font-size:34px;line-height:1}.gate h2{font-size:21px;margin:0}
.gsteps{margin:4px 0 12px;padding-left:22px;display:grid;gap:5px;font-size:14.5px;line-height:1.5}
.gwarn{padding:10px 12px;border-radius:10px;background:rgba(224,67,79,.16);border:1px solid #e0434f;font-size:14px;line-height:1.5;margin-bottom:10px}
.gmail{padding:8px 12px;border-radius:10px;background:var(--panel2);margin-bottom:10px;font-size:15px;word-break:break-all}
body.light .rtag.o{""")
rep('lalu ketuk "Duduk di meja ini": ${tableLink(gid)}`;}','lalu ketuk "Duduk di meja ini": ${tableLink(gid)} (buka di Chrome/Safari & login ke Claude dulu ya)`;}',2)
rep("  {const gs=$('#gateSlot');","  if(online==='off'&&EDITION!=='latihan'&&!ui.loginPopShown&&view==='lobby'&&!modalOpen()){ui.loginPopShown=true;setTimeout(()=>{if(online==='off'&&!modalOpen())openLoginPop();},400);}\n  {const gs=$('#gateSlot');")
rep('<html lang="id">','<html lang="id" translate="no">')
rep("<head>",'<head>\n<meta name="google" content="notranslate">')
rep("body.light .rtag.o{",""".mylane{display:grid;gap:12px;align-content:start}
.patrons{grid-template-columns:repeat(5,minmax(0,1fr))!important;max-width:470px;gap:8px;margin-bottom:10px}
@media(max-width:560px){.patrons{max-width:none;gap:5px}}
.mylane .players{margin-top:0}
.pl.mine-pl{background:#4a3d1c;border:1.5px solid #b98f2c;color:#fbecc4}
.pl.mine-pl .score{color:#f3d27a}
.pl.mine-pl.turn{border-color:#f3d27a;box-shadow:0 0 0 3px rgba(243,210,122,.55)}
.d-me{background:#4a3d1c!important;border:1.5px solid #b98f2c!important}
.pmpl.me{order:-1;background:#4a3d1c;border:1.5px solid #b98f2c;box-shadow:none}
.pmpl.me.turn{border-color:#f3d27a;box-shadow:0 0 0 3px rgba(243,210,122,.55)}
body.light .pl.mine-pl,body.light .d-me,body.light .pmpl.me{background:#fbefcf!important;border-color:#c99a2e!important;color:#3b2a20}
body.light .pl.mine-pl .score{color:#a8761a}
body.light .rtag.o{""")
rep("  rankPop(seat===0?'up':'last','🎲',seat===0?'Kamu pemain pertama — jalan duluan!':`Kamu pemain ${ord} dari ${n}`,`Urutan giliran: ${list}`,5000);",
    "  rankPop(seat===0?'up':'last','<span class=\"rpnum\">'+(seat+1)+'</span>',`Kamu urutan ${seat+1}`,seat===0?`dari ${n} pemain · kamu jalan duluan!`:`dari ${n} pemain`,4500);")
rep("toastT=setTimeout(()=>t.classList.remove('show'),2600);}","toastT=setTimeout(()=>t.classList.remove('show'),2800);}")
rep("body.light .rtag.o{","""body #toast{top:52%;bottom:auto!important;transform:translate(-50%,-50%) scale(.94);font-size:16px;padding:14px 22px;border-radius:16px;border-width:2px;max-width:min(520px,90vw);text-align:center;line-height:1.45;box-shadow:0 18px 50px rgba(0,0,0,.55);transition:opacity .2s,transform .2s}
body #toast.show{transform:translate(-50%,-50%) scale(1)}
body:has(#modal.open) #toast{top:auto;bottom:18px!important;transform:translate(-50%,0)}
@media (max-width:760px){body #toast{font-size:14.5px;padding:12px 16px}}
body #rankpop{top:15%}
#rankpop .rpnum{display:inline-block;font-family:'Fraunces',serif;font-size:64px;font-weight:800;color:var(--gold);line-height:1;text-shadow:3px 3px 0 #111}
body.light .rtag.o{""")
rep("  const players=st.players.map((p,i)=>{\n    const b=bonusOf(p);\n    const inv=ALL.map(c=>`<div class=\"slot ${c==='y'?'gold':''}\">${c!=='y'?`<div class=\"bon c-${c} ${b[c]?'':'zero'}\">${b[c]}</div>`:'<div class=\"jlab\">JOKER</div>'}<div class=\"tk c-${c} ${p.t[c]?'':'zero'}\">${p.t[c]}</div></div>`).join('');\n    const own=i===seat;",
    "  const plArr=st.players.map((p,i)=>{\n    const b=bonusOf(p);\n    const inv=ALL.map(c=>`<div class=\"slot ${c==='y'?'gold':''}\">${c!=='y'?`<div class=\"bon c-${c} ${b[c]?'':'zero'}\">${b[c]}</div>`:'<div class=\"jlab\">JOKER</div>'}<div class=\"tk c-${c} ${p.t[c]?'':'zero'}\">${p.t[c]}</div></div>`).join('');\n    const own=i===seat;")
rep("      ${resv}</div>`;\n  }).join('');\n  const logs=st.log.slice(-14)","      ${resv}</div>`;\n  });\n  const myPl=seat>=0?plArr[seat]:'', players=plArr.filter((x,i)=>i!==seat).join('');\n  const logs=st.log.slice(-14)")
rep("  $('#app').innerHTML=`${result}<div class=\"game\">\n    <section class=\"panel\">","  $('#app').innerHTML=`${result}<div class=\"game\">\n    <div class=\"mylane\"><section class=\"panel\">")
rep("      ${rows}\n    </section>\n    <aside>","      ${rows}\n    </section>${myPl?`<div class=\"players\">${myPl}</div>`:''}</div>\n    <aside>")
open(p,'w').write(s); print('gate ok')
