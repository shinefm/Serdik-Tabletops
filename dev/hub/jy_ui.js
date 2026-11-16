/* ================= JUALAN YUK (tampilan) ================= */
function jyMe(st){return cur&&cur.local?cur.human:meIdx(st);}
function jyMyTeam(st){const me=jyMe(st);return me>=0?jyTeamOf(st,me):-1;}
function jyDot(T){return `<span class="jydot" style="background:${T.col}"></span>`;}
function jyNames(st,t){const T=st.teams[t];if(T.bot)return '🤖 Tim bot';return T.members.map(i=>esc(nm(st,i))).join(', ');}
function jyRoleOf(st,t,div){const T=st.teams[t];if(T.bot)return '🤖';if(!st.split)return 'semua';const i=T.roles[div];return i!=null?esc(nm(st,i)):'–';}
function jyForm(st){
  const t=jyMyTeam(st), r=(cur.lid||cur.gid)+':'+st.round+':'+t;
  if(!ui.jy||ui.jy.key!==r)ui.jy={key:r,d:{},cell:null,k:0};
  return ui.jy;
}
function jyDraft(st,t){const T=st.teams[t];return Object.assign({},T.draft,t===jyMyTeam(st)&&ui.jy?ui.jy.d:{});}
/* ---------- totem ---------- */
function jyRepeat(n,html,cap){cap=cap||14;n=Math.max(0,n);return html.repeat(Math.min(n,cap))+(n>cap?`<span class="jymore">+${n-cap}</span>`:'');}
function jyPerson(l,cls){return `<span class="jyp l${l} ${cls||''}" title="Karyawan level ${l}"><i>L${l}</i></span>`;}
function jyCube(q,cls){return `<span class="jycube q${q} ${cls||''}" title="${JY.QN[q]}"></span>`;}
function jyHeart(cls){return `<span class="jyheart ${cls||''}">♥</span>`;}
function jyCoin(cls){return `<span class="jycoin ${cls||''}">Rp</span>`;}
function jyEmpTot(emp,d,sm){
  const cur_=[emp[0]-(d?d.u12:0),emp[1]-(d?d.u23:0),emp[2]], add=d?[d.h0,d.h1+d.u12,d.h2+d.u23]:[0,0,0], c=sm?'sm':'';
  const out=[1,2,3].map(l=>jyRepeat(Math.max(0,cur_[l-1]),jyPerson(l,c),sm?6:10)+jyRepeat(add[l-1],jyPerson(l,c+' new'),sm?6:10)).join('');
  return out||'<span class="jynone">belum ada</span>';
}
function jyInvTot(inv,d,sm){const c=sm?'sm':'';
  const out=['L','M','H'].map(q=>jyRepeat(inv[q],jyCube(q,c),sm?6:10)+jyRepeat(d?d[q]:0,jyCube(q,c+' new'),sm?6:10)).join('');
  return out||'<span class="jynone">kosong</span>';
}
function jyRows(T,d){
  const e=[T.emp[0]+(d?d.h0-d.u12:0),T.emp[1]+(d?d.h1+d.u12-d.u23:0),T.emp[2]+(d?d.h2+d.u23:0)], v={H:T.inv.H+(d?d.H:0),M:T.inv.M+(d?d.M:0),L:T.inv.L+(d?d.L:0)};
  const cnt=(n,unit,parts)=>`<span class="jycnt"><b>${n}</b> ${unit}${n?` <small>${parts}</small>`:''}</span>`;
  return {hr:['👥 SDM',jyEmpTot(T.emp,d),'',cnt(e[0]+e[1]+e[2],'orang',`L1 ${e[0]} · L2 ${e[1]} · L3 ${e[2]}`)],
    op:['📦 Produksi',jyInvTot(T.inv,d),'',cnt(v.H+v.M+v.L,'barang',`E ${v.L} · S ${v.M} · P ${v.H}`)],
    mk:['❤️ CR',jyRepeat(T.cr,jyHeart(),12)+jyRepeat(d?d.cr:0,jyHeart('new'),12)||'<span class="jynone">0</span>',`<b class="jynum">${T.cr+(d?d.cr:0)}</b>`],
    sl:['🪙 Dana jualan',jyRepeat(T.bud.sl/50,jyCoin(),12)+jyRepeat(d?d.sl/50:0,jyCoin('new'),12)||'<span class="jynone">0</span>',`<b class="jynum">${jyRp(T.bud.sl+(d?d.sl:0))}</b>`]};
}
function jyCashHTML(T,d){
  if(!d)return `<div class="jycash"><small>Kas keuangan</small><b>${jyRp(T.cash)}</b></div>`;
  const C=jyDraftCost(d), room=Math.min(JY.CAP,T.cash)-C.tot;
  return `<div class="jycash ${room<0?'over':''}"><small>Sisa jatah belanja ronde ini</small><b>${jyRp(room)}</b>${C.tot?`<span class="jyminus">−${jyRp(C.tot)} belanja ronde ini</span>`:''}</div>`;}
function jyBoardHTML(T,d,cashOnly){
  if(cashOnly)return jyCashHTML(T,d);
  const R=jyRows(T,d);
  return `<div class="jyboard">${jyCashHTML(T,d)}${['hr','op','mk','sl'].map(k=>`<div class="jyrow"><span class="jyrl">${R[k][0]}${R[k][3]?'<br>'+R[k][3]:''}</span><div class="jytot">${R[k][1]}${R[k][2]}</div></div>`).join('')}</div>`;
}
function jyItem(k,icon,name,price,v,dis,maxed,sub,unit){
  return `<div class="jyit ${v?'has':''}"><div class="jyii">${icon}</div><b>${name}</b><small>${price}${sub?' · '+sub:''}</small>
    <div class="jysb"><button class="btn sm" data-act="jyinc" data-k="${k}" data-d="-1" ${dis||v<=0?'disabled':''} aria-label="Kurangi ${name}">−</button><span>${k==='sl'?jyRp(v):v}</span><button class="btn sm" data-act="jyinc" data-k="${k}" data-d="1" ${dis||maxed?'disabled':''} aria-label="Tambah ${name}">+</button></div>${unit&&k!=='sl'?`<em class="jysub ${v?'on':''}">${v?v+' × '+unit+' = <b>'+jyRp(v*unit)+'</b>':'&nbsp;'}</em>`:''}</div>`;
}
function jyDemandHTML(st,clickable,F,T){
  const I=null;
  const cells=JY.Q.map(q=>`<div class="jyqh">${jyCube(q)}<span><b>${JY.QN[q]}</b></span></div>`+JY.P.map(p=>{const d=st.demand[q][p];
    const ok=clickable&&d>0&&T&&T.inv[q]>0&&jyElig(T,q,p)>0, sel=F&&F.cell&&F.cell.q===q&&F.cell.p===p, have=T&&jyElig(T,q,p)>0;
    return `<button class="jyc q${q} ${d?'':'zero'} ${sel?'sel':''} ${clickable&&!ok?'na':''} ${I&&I.q===q&&I.p===p?'info':''}" ${ok?`data-act="jycell"`:`data-act="jyinfo"`} data-q="${q}" data-p="${p}" aria-label="${JY.QN[q]} ${JY.PN[p]}: ${d} pembeli, peluang laku ${Math.round(jyChance(q,p,0)*100)} persen, laku ${jyRp(JY.REV[q][p])} per barang, butuh karyawan level ${JY.ABL[q][p].join(' atau ')}"><b>${d}</b><span class="jyprob">${[1,2,3,4,5].map(n=>JY.FAIL[q][p].includes(n)?'<i class="x">✕</i>':'<i>'+n+'</i>').join('')}</span><small class="jydt">laku ${jyRp(JY.REV[q][p])}</small><span class="jydt jyneed ${T?(have?'ok':'no'):''}">${JY.ABL[q][p].map(l=>jyPerson(l,'sm')).join('')}</span></button>`;}).join('')).join('');
  return `<div class="jydem"><div class="jydc">kualitas ↓ harga →</div>${JY.P.map(p=>`<div class="jyph">${JY.PN[p]}<small>biaya ${jyRp(JY.FEE[p])}</small></div>`).join('')}${cells}</div><p class="bd jytap">👆 Ketuk kotak untuk melihat detail dan arti ikonnya.</p>`;
}
function jyInfoModal(q,p){
  const st=cur.st, mt=jyMyTeam(st), T=mt>=0?st.teams[mt]:null, d=st.demand[q][p], el=T?jyElig(T,q,p):0, F=JY.FAIL[q][p];
  let note='';
  if(T){note=d<=0?'Pembelinya sudah habis.':el<=0?`Timmu belum punya karyawan level ${JY.ABL[q][p].join(' atau ')}.`:T.inv[q]<=0?`Timmu belum punya stok ${JY.QN[q].toLowerCase()}.`:`Timmu bisa menjual ${Math.min(d,T.inv[q],el)} barang di sini (stok ${T.inv[q]}, karyawan mampu ${el}).`;}
  const toks=[1,2,3,4,5].map(n=>F.includes(n)?'<i class="x">✕</i>':'<i>'+n+'</i>').join('');
  openModal(`<h3>${jyCube(q)} ${JY.QN[q]} · ${JY.PN[p]}</h3>
    <div class="jyml">
      <div class="jymr"><span class="jymi"><b class="jybig">${d}</b></span><div><b>${d} pembeli</b><small>Angka besar = jumlah pembeli di kotak ini. Dipakai bersama semua tim, siapa jualan duluan dapat duluan.</small></div></div>
      <div class="jymr"><span class="jymi"><span class="jyprob lg">${toks}</span></span><div><b>Peluang laku ${Math.round(jyChance(q,p,0)*100)}%</b><small>Isi kantong token 1–5. ${F.length?`Kalau terambil ✕ (angka ${F.join(', ')}), penjualan gagal.`:'Tidak ada ✕, jadi selalu laku.'} Dengan 2 token Pasti jadi ${Math.round(jyChance(q,p,2)*100)}%, dengan 4 jadi ${Math.round(jyChance(q,p,4)*100)}%.</small></div></div>
      <div class="jymr"><span class="jymi">${JY.ABL[q][p].map(l=>jyPerson(l,'sm')).join('')}</span><div><b>Butuh karyawan level ${JY.ABL[q][p].join(' atau ')}</b><small>Ikon orang = level karyawan yang bisa menjual di kotak ini. Tiap karyawan yang mampu menjual 1 barang per percobaan.</small></div></div>
      <div class="jymr"><span class="jymi">${jyCoin()}</span><div><b>Laku ${jyRp(JY.REV[q][p])} per barang</b><small>Pendapatan masuk ke kas. Biaya tiap percobaan jual di harga ${JY.PN[p].toLowerCase()}: ${jyRp(JY.FEE[p])}, dibayar dari dana jualan, laku atau tidak.</small></div></div>
    </div>
    ${note?`<p class="jyin">${note}</p>`:''}
    <div class="mbtns"><button class="btn pri" data-act="close">Mengerti</button></div>`);
}
function jyPlanPanel(st,t,me){
  const T=st.teams[t];
  if(T.step==='ready')return `<p class="mute jywait">✔ Rencana timmu sudah dikirim. Menunggu tim lain…</p>`;
  const d=jyDraft(st,t), C=jyDraftCost(d), cap=Math.min(JY.CAP,T.cash), room=cap-C.tot;
  const can=dv=>me>=0&&jyCan(st,me,t,dv), who=dv=>st.split?` <small class="jywho ${can(dv)?'me':''}">${can(dv)?'bagianmu':'dipegang '+jyRoleOf(st,t,dv)}</small>`:'';
  const it=(k,icon,name,price,unit,sub,extraMax)=>jyItem(k,icon,name,price,d[k],!can(JY_KEYS[k]),room<unit||extraMax,sub,unit);
  const bub=(v)=>`<span class="jybub ${v?'on':''}">${jyRp(v)}</span>`;
  const R=jyRows(T,d), O=ui.jyOpen=ui.jyOpen||{hr:true};
  const acc=(k,cost,body)=>`<div class="jyacc ${O[k]?'open':''}"><button class="jyah" data-act="jyacc" data-d="${k}" aria-expanded="${!!O[k]}"><span class="jyat"><b>${R[k][0]}</b>${R[k][3]||''}${who(k)}</span>${bub(cost)}<span class="jychev">▾</span><div class="jytot">${R[k][1]}${R[k][2]}</div></button>${O[k]?`<div class="jyab">${body}</div>`:''}</div>`;
  const over=room<0;
  return `<div class="jyplan">
    ${(()=>{let seen=false;try{seen=localStorage.getItem('jyHelp')==='1';}catch(e){}
      const open=ui.jyHelpOpen!=null?ui.jyHelpOpen:(!seen&&st.round===1); if(!seen){try{localStorage.setItem('jyHelp','1');}catch(e){} ui.jyHelpFirst=1;}
      const op=ui.jyHelpOpen!=null?ui.jyHelpOpen:(ui.jyHelpFirst&&st.round===1);
      return `<div class="jyq"><button class="jyqb ${op?'on':''}" data-act="jyhelp" aria-expanded="${!!op}" aria-label="Cara belanja">?</button>${op?`<p class="jyqt">Ketuk tiap kotak untuk membuka pilihannya. Harga langsung dihitung dan dipotong dari kas. Belanja maksimal <b>${jyRp(JY.CAP)}</b> per ronde. Selama belum menekan <b>Siap jualan</b>, semuanya masih bisa diubah.</p>`:'<span class="jyqh2">Cara belanja</span>'}</div>`;})()}
    ${acc('hr',C.hr,`<div class="jyits">${it('h0',jyPerson(1),'Level 1','Rp50 rb',50)}${it('h1',jyPerson(2),'Level 2','Rp100 rb',100)}${it('h2',jyPerson(3),'Level 3','Rp150 rb',150)}</div>
      ${T.emp[0]+T.emp[1]>0?`<div class="jyits two">${T.emp[0]?it('u12',jyPerson(1,'sm')+'→'+jyPerson(2,'sm'),'Latih L1 → L2','Rp50 rb',50,'punya '+T.emp[0],d.u12>=T.emp[0]):''}${T.emp[1]?it('u23',jyPerson(2,'sm')+'→'+jyPerson(3,'sm'),'Latih L2 → L3','Rp50 rb',50,'punya '+T.emp[1],d.u23>=T.emp[1]):''}</div>`:''}
      ${jyAblHTML()}`)}
    ${acc('op',C.op,`<div class="jyits">${it('L',jyCube('L'),'Ekonomi','Rp50 rb',50)}${it('M',jyCube('M'),'Standar','Rp100 rb',100)}${it('H',jyCube('H'),'Premium','Rp150 rb',150)}</div>`)}
    ${acc('mk',C.mk,`<div class="jyits one">${it('cr',jyHeart(),'Tambah CR','Rp50 rb/level',50,'CR tertinggi jualan duluan')}</div>`)}
    ${acc('sl',C.sl,`<div class="jyits one">${jyItem('sl',jyCoin(),'Dana jualan','per Rp50 rb',d.sl,!can('sl'),room<50,'untuk bayar biaya tiap percobaan jual')}</div>
      ${(()=>{const op=ui.jySlHelp!=null?ui.jySlHelp:st.round===1;
        return `<div class="jyq" style="margin:8px 0 0"><button class="jyqb ${op?'on':''}" data-act="jyslhelp" aria-expanded="${!!op}" aria-label="Cara pakai dana jualan">?</button>${op?`<div class="jyslx"><b>Cara pakainya saat jualan</b><ul><li>Tiap percobaan menjual bayar biaya sesuai harga yang diincar: <b>Murah Rp50 rb</b>, <b>Normal Rp100 rb</b>, <b>Mahal Rp150 rb</b>. Dibayar walau gagal.</li><li><b>Token Pasti</b>: <b>Rp50 rb untuk 2 token</b>, maksimal 4 token (Rp100 rb) per percobaan.<div class="jytokv"><span class="jyprob lg"><i class="x">✕</i><i class="x">✕</i><i>3</i><i>4</i><i>5</i></span><span>+</span><span class="jypasti">Pasti</span><span class="jypasti">Pasti</span></div></li><li>Sisa dana jualan tersimpan untuk ronde berikutnya.</li></ul></div>`:'<span class="jyqh2">Cara pakai dana jualan dan token Pasti</span>'}</div>`;})()}`)}
    <div class="jytotal ${ui.jySum?'open':''}">
      <button class="jysumh" data-act="jysum" aria-expanded="${!!ui.jySum}"><span>Sisa kas</span><b>${jyRp(T.cash-C.tot)}</b><span class="jychev">▾</span></button>
      ${ui.jySum?`<div class="jysumb">${(()=>{const R=st.recap,pv=R&&R.round===st.round-1?(R.rev[t]||0):null;return pv==null?'':`<div class="jycalc"><span>Sisa kas ronde ${st.round-1}</span><b>${jyRp(T.cash-pv)}</b></div><div class="jycalc plus ${pv?'':'zero'}"><span>💰 Hasil jualan ronde ${st.round-1}</span><b>+ ${jyRp(pv)}</b></div>`;})()}<div class="jycalc base"><span>${st.round===1?'Modal awal':'Kas awal ronde ini'}</span><b>${jyRp(T.cash)}</b></div>
        ${[['👥 SDM',C.hr],['📦 Produksi',C.op],['❤️ Pemasaran',C.mk],['🪙 Dana jualan',C.sl]].map(x=>`<div class="jycalc ${x[1]?'':'zero'}"><span>${x[0]}</span><b>− ${jyRp(x[1])}</b></div>`).join('')}</div>`:''}
    </div>
    ${over?`<p class="bad" style="margin:6px 0">Belanja melebihi batas ${jyRp(cap)}. Kurangi dulu ${jyRp(-room)}.</p>`:''}
    ${T.bud.sl+d.sl<50&&!over?'<p class="bd" style="margin:6px 0">⚠️ Dana jualan masih Rp0. Tanpa dana jualan timmu tidak bisa menjual di ronde ini.</p>':''}
    ${can('fin')?`<button class="btn pri big jygo" data-act="jyready" ${over?'disabled':''}>✅ Siap jualan</button>`:`<p class="mute jywait">⏳ <b>${jyRoleOf(st,t,'fin')}</b> (Keuangan) yang menekan “Siap jualan” setelah semua bagian terisi.</p>`}
  </div>`;
}
function jyAblHTML(){
  return `<details class="jyabl"><summary>Tabel kemampuan karyawan</summary><table><tr><th></th>${JY.P.map(p=>`<th>${JY.PN[p]}</th>`).join('')}</tr>${JY.Q.map(q=>`<tr><th>${JY.QN[q]}</th>${JY.P.map(p=>`<td>L${JY.ABL[q][p].join('/')}</td>`).join('')}</tr>`).join('')}</table><small>Setiap karyawan yang mampu bisa menjual 1 barang per percobaan.</small></details>`;
}
function jyDrawHTML(st){
  const D=st.draw; if(!D)return '';
  const T=st.teams[D.t], anim=ui.jyAnim!==D.n; if(anim)setTimeout(()=>{ui.jyAnim=D.n;},1800);
  const toks=D.pouch.map((x,k)=>{const bad=x!=='S'&&JY.FAIL[D.q][D.p].includes(x), hit=x===D.drawn&&k===D.pouch.indexOf(D.drawn);
    return `<span class="jytok ${bad?'bad':'good'} ${x==='S'?'pasti':''} ${hit?'hit':''}" style="--i:${k}">${x==='S'?'Pasti':x}${bad?'<i>✕</i>':''}</span>`;}).join('');
  return `<div class="jydraw ${anim?'anim':''}" style="border-color:${T.col}"><div class="jydh">${jyDot(T)}<b>${esc(T.name)}</b> · ${JY.QN[D.q]} · ${JY.PN[D.p]}${D.k?` · +${D.k} pasti`:''}</div>
    <div class="jytoks">${toks}</div>
    <div class="jyres ${D.ok?'ok':'no'}">${D.ok?`✅ Laku ${D.units} · +${jyRp(D.rev)}`:'❌ Gagal terjual'} <small>(biaya ${jyRp(D.cost)})</small></div></div>`;
}
function jySellPanel(st,t,me){
  const cur_t=st.order[st.si], T=st.teams[t], myTurn=t===cur_t, can=me>=0&&myTurn&&jyCan(st,me,t,'sl'), F=jyForm(st);
  const ord=st.order.map((i,k)=>`<span class="jyord ${k<st.si?'done':''} ${k===st.si?'now':''}" style="border-color:${st.teams[i].col}">${k+1}. ${esc(st.teams[i].name)} · CR ${st.teams[i].cr}</span>`).join('');
  let form='';
  if(can){const c=F.cell;
    if(c&&(st.demand[c.q][c.p]<=0||T.inv[c.q]<=0||jyElig(T,c.q,c.p)<=0))F.cell=null;
    if(!F.cell)form=`<p class="jyhelp">👆 Ketuk kotak demand di atas yang mau kamu incar. Kotak redup = stok, karyawan, atau demand tidak cukup.</p>`;
    else{const {q,p}=F.cell, el=jyElig(T,q,p), units=Math.min(st.demand[q][p],T.inv[q],el);
      while(F.k>0&&JY.FEE[p]+F.k/2*JY.SOLD2>T.bud.sl)F.k-=2;
      const opts=[0,2,4].map(k=>{const cost=JY.FEE[p]+k/2*JY.SOLD2;return `<button class="btn sm ${F.k===k?'on':''}" data-act="jyk" data-k="${k}" ${cost>T.bud.sl?'disabled':''}>${k?`+${k} pasti`:'Tanpa'}<small>${Math.round(jyChance(q,p,k)*100)}% · ${jyRp(cost)}</small></button>`;}).join('');
      const cost=JY.FEE[p]+F.k/2*JY.SOLD2;
      form=`<div class="jysel"><div><b>${JY.QN[q]} · ${JY.PN[p]}</b> — kalau laku: <b>${units}</b> barang × ${jyRp(JY.REV[q][p])} = <b>${jyRp(units*JY.REV[q][p])}</b></div>
        <small class="mute">demand ${st.demand[q][p]} · stok ${T.inv[q]} · karyawan mampu ${el} (L${JY.ABL[q][p].join('/')})</small> <button class="btn sm" data-act="jyinfo" data-q="${q}" data-p="${p}" style="padding:2px 8px">ℹ️ arti ikon</button>
        <div class="jyks">${opts}</div>
        <button class="btn pri big jygo" data-act="jysell" ${cost>T.bud.sl?'disabled':''}>🎯 Jual · bayar ${jyRp(cost)}</button></div>`;}
    form+=`<button class="btn sm" data-act="jystop" style="margin-top:8px">Berhenti jualan ronde ini</button>`;
  }else if(myTurn)form=`<p class="mute jywait">⏳ <b>${jyRoleOf(st,t,'sl')}</b> (Penjualan) sedang memilih…</p>`;
  else form=`<p class="mute jywait">${st.si<st.order.indexOf(t)?'⏳ Tunggu giliran jualan timmu.':'✔ Timmu sudah selesai jualan ronde ini.'}</p>`;
  return `<div class="jyords">${ord}</div><div class="jybud" style="margin:0 0 8px">🪙 Dana jualan <b>${jyRp(T.bud.sl)}</b></div>${form}`;
}
function jyTeamsHTML(st,mt){
  const sell=st.phase==='sell'||st.status==='ended';
  return st.teams.map((T,t)=>{let stt='';
    if(st.status==='ended')stt='⭐'.repeat(T.stars||0)||'—';
    else if(st.phase==='plan')stt=T.step==='ready'?'✔ siap jualan':'🛠️ menyusun rencana…';
    else{const k=st.order.indexOf(t);stt=k<st.si?'✔ selesai':k===st.si?'🛒 jualan':'⏳ antre';}
    const show=t===mt||sell;
    return `<div class="jytm ${t===mt?'me':''} ${st.phase==='sell'&&st.order[st.si]===t?'turn':''}" style="--tc:${T.col}">
      <div class="jytmh">${jyDot(T)}<b>${esc(T.name)}</b>${t===mt?' <span class="mine">(timmu)</span>':''}<span class="jytms">${stt}</span></div>
      <div class="bd">${jyNames(st,t)}</div>
      <div class="jytmn"><span>Kas <b>${jyRp(T.cash)}</b></span><span>CR <b>${sell||t===mt?T.cr:'?'}</b></span></div>${show?`<div class="jymini"><div class="jytot">${jyEmpTot(T.emp,null,true)}</div><div class="jytot">${jyInvTot(T.inv,null,true)}</div></div>`:'<div class="bd">Karyawan dan gudang tim lain terlihat saat fase jualan.</div>'}</div>`;}).join('');
}
function renderJualan(){
  const st=cur.st, me=jyMe(st), mt=jyMyTeam(st), T=mt>=0?st.teams[mt]:null, ended=st.status==='ended';
  if(!cur.local)refreshNames(st.players.map(p=>p.id));
  const phase=ended?'Selesai':st.phase==='plan'?'Fase rencana':'Fase jualan';
  const F=mt>=0?jyForm(st):null;
  const clickable=!ended&&st.phase==='sell'&&mt>=0&&st.order[st.si]===mt&&me>=0&&jyCan(st,me,mt,'sl');
  const log=st.log.filter(l=>!l.priv||l.t===mt||ended).slice(-14).reverse().map(l=>`<div class="lg" ${l.t!=null?`style="border-left:3px solid ${st.teams[l.t].col};padding-left:8px"`:''}>${esc(l.m)}</div>`).join('');
  const jyDemHTML=`<section class="panel jydemp"><h2 class="jyh2">📊 Demand ronde ${st.round}</h2>${jyDemandHTML(st,clickable,F,T)}
      ${!ended&&st.phase==='sell'&&T?'<div class="jysp">'+jySellPanel(st,mt,me)+'</div>':''}
      ${st.draw&&st.phase==='sell'||st.draw&&ended?jyDrawHTML(st):''}</section>`;
  const jyDemSec=st.phase==='plan'&&!ended?'':jyDemHTML, jyDemSec2=st.phase==='plan'&&!ended?jyDemHTML:'';
  $('#app').innerHTML=`<div class="jywrap">
    <section class="panel jyhead"><div class="row" style="justify-content:space-between;align-items:center;gap:8px">
      <div><b style="font-size:18px">🛍️ Ronde ${st.round}/${st.rounds}</b> <span class="pill ${st.phase==='sell'?'playing':''}">${phase}</span></div>
      <div class="row" style="gap:6px;align-items:center">${timerHTML(st)}<button class="btn sm" data-act="tutorial" data-w="jualan" aria-label="Cara main">📖</button></div></div>
      ${st.phase==='sell'&&!ended?`<div class="bd" style="margin-top:6px">Giliran jualan: ${jyDot(st.teams[st.order[st.si]])}<b>${esc(st.teams[st.order[st.si]].name)}</b></div>`:''}</section>
    ${jyDemSec}
    ${T?`<section class="panel jymine" style="--tc:${T.col}"><h2 class="jyh2">${jyDot(T)}${esc(T.name)} <small class="mute">${st.split?'bagi peran':'mode sendiri'}</small></h2>
      ${jyBoardHTML(T,!ended&&st.phase==='plan'&&T.step==='plan'?jyDraft(st,mt):null,!ended&&st.phase==='plan'&&T.step==='plan')}
      ${ended||st.phase!=='plan'?'':jyPlanPanel(st,mt,me)}</section>`:`<section class="panel"><p class="mute">Kamu menonton. Kamu bukan anggota tim mana pun.</p></section>`}
    ${jyDemSec2}
    <section class="panel"><h2 class="jyh2">🏪 Semua tim</h2><div class="jytms">${jyTeamsHTML(st,mt)}</div>
      ${ended?'<button class="btn pri" data-act="jyend" style="margin-top:10px">🏆 Lihat hasil akhir</button>':''}</section>
    <section class="panel"><details ${innerWidth>900?'open':''}><summary><b>Catatan permainan</b></summary><div class="logbox">${log}</div></details></section>
  </div>`;
  jyMaybeRecap(st);
}
function jyMaybeRecap(st){
  const R=st.recap; if(!R||st.status!=='playing'||st.phase!=='plan')return;
  const key=(cur.lid||cur.gid)+':'+R.round; ui.jyRecap=ui.jyRecap||{}; if(ui.jyRecap[key]||modalOpen())return; ui.jyRecap[key]=1;
  const rows=st.teams.map((T,i)=>({T,i,rev:R.rev[i],cash:R.cash[i]})).sort((a,b)=>b.cash-a.cash);
  setTimeout(()=>{if(modalOpen())return;openModal(`<h3>📈 Rekap ronde ${R.round}</h3><div class="rkl">${rows.map((x,k)=>`<div class="rki ${x.i===jyMyTeam(st)?'me':''}"><span class="pos">${k+1}</span><span class="nm">${jyDot(x.T)}${esc(x.T.name)}<div class="bd">pendapatan ronde ini ${jyRp(x.rev)}</div></span><span class="pt" style="font-size:18px">${jyRp(x.cash)}</span></div>`).join('')}</div>
    <p class="bd" style="margin:10px 0 0">Ronde ${st.round} dari ${st.rounds} dimulai. Demand baru sudah keluar.</p><div class="mbtns"><button class="btn pri" data-act="close">Lanjut</button></div>`);},cur.local?700:300);
}
function jyChartSVG(st){
  const W=320,H=150,P=26, n=st.teams[0].hist.length, mx=Math.max(JY.TARGET,...st.teams.flatMap(T=>T.hist));
  const x=i=>P+i*(W-P-8)/Math.max(1,n-1), y=v=>H-18-(v/mx)*(H-30);
  const lines=st.teams.map(T=>`<polyline fill="none" stroke="${T.col}" stroke-width="2.5" points="${T.hist.map((v,i)=>x(i)+','+y(v)).join(' ')}"/>`).join('');
  return `<svg viewBox="0 0 ${W} ${H}" class="jychart" role="img" aria-label="Grafik kas per ronde"><line x1="${P}" x2="${W-8}" y1="${y(JY.TARGET)}" y2="${y(JY.TARGET)}" stroke="currentColor" stroke-dasharray="4 4" opacity=".4"/><text x="${W-8}" y="${y(JY.TARGET)-4}" text-anchor="end" font-size="10" fill="currentColor" opacity=".7">target 5 jt</text>${lines}${Array.from({length:n},(_,i)=>`<text x="${x(i)}" y="${H-4}" text-anchor="middle" font-size="10" fill="currentColor" opacity=".7">${i===0?'awal':'R'+i}</text>`).join('')}</svg>`;
}
function openJYEnd(){
  const st=cur.st, mt=jyMyTeam(st), order=st.teams.map((T,i)=>i).sort((a,b)=>st.teams[b].cash-st.teams[a].cash);
  const win=mt>=0&&st.winner.includes(mt);
  openModal(`<div class="endm"><div class="big">${win?'🏆':'🛍️'}</div><h3>${win?'Timmu juara! 🎉':esc(st.winner.map(i=>st.teams[i].name).join(' & '))+' juara'}</h3>
    <p class="why">Kas terbanyak di Keuangan setelah ${st.rounds} ronde.</p>
    <div class="rkl">${order.map((i,k)=>{const T=st.teams[i];return `<div class="rki ${k===0?'win':''} ${i===mt?'me':''}"><span class="pos">${['🥇','🥈','🥉','4'][k]}</span><span class="nm">${jyDot(T)}${esc(T.name)} ${'⭐'.repeat(T.stars||0)}<div class="bd" style="font-weight:400">${jyNames(st,i)} · terjual ${T.sold} barang</div></span><span class="pt" style="font-size:17px">${jyRp(T.cash)}</span></div>`;}).join('')}</div>
    ${jyChartSVG(st)}
    <p class="bd" style="margin:6px 0 0">⭐ kas minimal Rp5 jt · ⭐ kas terbanyak.</p>
    <div class="mbtns"><button class="btn" data-act="close">Lihat papan</button>${cur.local?'<button class="btn" data-act="restartlocalok">🆕 Main game baru</button><button class="btn" data-act="jylocal">Ganti pengaturan</button>':''}<button class="btn pri" data-act="lobby">Kembali ke lobi</button></div></div>`);
}
/* ---------- aksi pemain ---------- */
function jyInc(k,dir){
  const st=cur.st, t=jyMyTeam(st), T=st.teams[t], F=jyForm(st), d=jyDraft(st,t), step=k==='sl'?50:1;
  const v=Math.max(0,(d[k]||0)+dir*step);
  if(dir>0){const nd=Object.assign({},d,{[k]:v});if(jyDraftCost(nd).tot>Math.min(JY.CAP,T.cash))return toast('Batas belanja ronde ini '+jyRp(Math.min(JY.CAP,T.cash)));
    if(k==='u12'&&v>T.emp[0]||k==='u23'&&v>T.emp[1])return;}
  F.d[k]=v; render(); jyFlush();
}
function jyFlush(now){
  const F=ui.jy; if(!F||!Object.keys(F.d).length)return;
  if(cur.local){const s=clone(cur.st);try{jyAct(s,cur.human,{type:'draft',d:F.d});cur.st=s;F.d={};}catch(e){toast(e.message);F.d={};render();}return;}
  clearTimeout(ui.jyT); ui.jyT=setTimeout(async()=>{
    if(!cur||cur.local||!ui.jy||ui.jyBusy)return jyFlush();
    const sent=Object.assign({},ui.jy.d); if(!Object.keys(sent).length)return; ui.jyBusy=true;
    try{await commitOnline(s=>{const i=meIdx(s);if(i<0)throw NOOP;jyAct(s,i,{type:'draft',d:sent});});
      for(const k in sent)if(ui.jy&&ui.jy.d[k]===sent[k])delete ui.jy.d[k];}
    catch(e){if(e&&!e.noop){toast(e.message||'Gagal menyimpan');if(ui.jy)ui.jy.d={};render();}}
    finally{ui.jyBusy=false;if(ui.jy&&Object.keys(ui.jy.d).length)jyFlush();}
  },now?0:450);
}
async function jyReady(){
  const st=cur.st, me=jyMe(st), F=jyForm(st), d=Object.assign({},F.d);
  const run=(s,i)=>{if(Object.keys(d).length)jyAct(s,i,{type:'draft',d});jyAct(s,i,{type:'ready'});};
  try{run(clone(st),me);}catch(e){return toast(e.message);}
  if(cur.local){const s=clone(st);run(s,me);cur.st=s;F.d={};render();if(s.status==='ended')onGameEnded(s);return;}
  if(ui.busy)return; ui.busy=true; clearTimeout(ui.jyT);
  try{await commitOnline(s=>{const i=meIdx(s);if(i<0)fail('Kamu bukan pemain meja ini');run(s,i);});F.d={};}
  catch(e){if(!e.noop)toast(e.message||'Gagal menyimpan, coba lagi');}
  finally{ui.busy=false;}
}
async function jyMove(mv){
  const st=cur.st, me=jyMe(st);
  try{jyAct(clone(st),me,mv);}catch(e){return toast(e.message);}
  if(cur.local){const s=clone(st);jyAct(s,me,mv);cur.st=s;render();if(s.status==='ended')onGameEnded(s);return;}
  if(ui.busy)return; ui.busy=true;
  try{await commitOnline(s=>{const k=meIdx(s);if(k<0)fail('Kamu bukan pemain meja ini');jyAct(s,k,mv);});}
  catch(e){if(!e.noop)toast(e.message||'Gagal menyimpan, coba lagi');}
  finally{ui.busy=false;}
}
/* ---------- bot ---------- */
function jyMaybeBot(){
  if(!cur||!cur.local||cur.botTimer||cur.st.game!=='jualan')return;
  const st=cur.st, nx=jyBotNext(st,false); if(!nx)return;
  cur.botTimer=setTimeout(()=>{const c0=cur;if(!c0||!c0.local)return;c0.botTimer=null;if(c0.st!==st)return render();
    const s=clone(st), x=jyBotNext(s,false); if(!x)return render(); jyApplyBot(s,x); c0.st=s;
    if(s.status==='ended')onGameEnded(s); render();},nx.div==='sl'?1700:350);
}
function jyOnlineBot(){
  if(!cur||cur.local||!cur.st||cur.st.game!=='jualan'||canWrite===false||!myId)return;
  const st=cur.st; if(st.status!=='playing')return; const nx=jyBotNext(st,false); if(!nx)return;
  const key=cur.gid+':'+st.v; if(ui.obKey===key)return;
  const humans=st.players.filter(q=>!q.bot).map(q=>q.id), order=[st.host,...humans.filter(x=>x!==st.host)];
  const runner=order.find(id=>id===myId||ONLINE.has(id)), stalled=st.turnAt&&Date.now()-st.turnAt>9000;
  if(runner!==myId&&!(stalled&&humans.includes(myId))){if(!ui.obRetry)ui.obRetry=setTimeout(()=>{ui.obRetry=null;jyOnlineBot();},4000);return;}
  ui.obKey=key; const v=st.v;
  setTimeout(()=>{if(!cur||cur.local||!cur.st||cur.st.v!==v)return;
    commitOnline(s=>{if(s.status!=='playing'||s.v!==v)throw NOOP;const x=jyBotNext(s,false);if(!x)throw NOOP;jyApplyBot(s,x);}).catch(()=>{ui.obKey=null;});
  },nx.div==='sl'?1700:500);
}
function jyTimeoutRun(s){
  if(s.phase==='plan'){
    s.teams.forEach((T,t)=>{if(T.step!=='plan')return;
      if(T.bot)return jyApplyBot(s,{t,mv:{type:'plan',d:jyBotPlan(s,t)}});
      try{jyAct(s,-9,{type:'ready',team:t});}catch(e){if(!(e instanceof GameErr))throw e;T.draft=jyNewDraft();jyAct(s,-9,{type:'ready',team:t});}});
    s.log.push({p:-1,m:'⏱ Waktu rencana habis — rencana tiap tim dikirim apa adanya.'});}
  else if(s.phase==='sell'){const x=jyBotNext(s,true);if(x){jyApplyBot(s,x);s.log.push({p:-1,m:'⏱ Waktu habis — langkah jualan diambil otomatis.'});}}
}
/* ---------- ruang tunggu ---------- */
function renderWaitingJY(){
  const st=cur.st, mi=meIdx(st), isHost=st.host===myId, G=GAMES.jualan, n=st.players.length, nt=st.nteams||2, canAct=canWrite!==false&&myId;
  refreshNames(st.players.map(p=>p.id));
  const cols=Array.from({length:nt},(_,t)=>{const D=JY.TEAMS[t], mem=st.players.map((p,i)=>i).filter(i=>(st.players[i].team??-1)===t);
    return `<div class="jywt" style="--tc:${D.c}"><div class="jytmh"><span class="jydot" style="background:${D.c}"></span><b>${D.n}</b><span class="jytms">${mem.length?mem.length+' orang':'🤖 tim bot'}</span></div>
      ${mem.map(i=>`<div class="seat"><span class="dot ${ONLINE.has(st.players[i].id)?'on':''}"></span><b>${esc(nm(st,i))}</b>${st.players[i].id===st.host?'<span class="crown">· tuan rumah</span>':''}${i===mi?'<span class="mute">(kamu)</span>':''}</div>`).join('')||'<p class="bd" style="margin:4px 0">Kosong — akan dimainkan bot.</p>'}
      ${mi>=0&&(st.players[mi].team??-1)!==t&&canAct?`<button class="btn sm" data-act="jyjoin" data-t="${t}">Pindah ke sini</button>`:''}</div>`;}).join('');
  const none=st.players.map((p,i)=>i).filter(i=>(st.players[i].team??-1)<0||st.players[i].team>=nt);
  $('#app').innerHTML=`<section class="panel" style="max-width:760px;margin:0 auto">
    <h2 style="font-size:24px">${G.icon} ${esc(st.name||'Meja')}</h2>
    <p class="mute" style="font-size:14px;margin:6px 0 0">${G.name} · 2–4 tim. Kirim link meja ini, teman masuk lalu pilih tim.</p>
    ${shareBox(st)}
    <div class="row jycfg" style="margin:10px 0;gap:10px;align-items:center">
      <label class="field" style="min-width:0">Jumlah tim${isHost?`<select id="jyNt">${[2,3,4].map(k=>`<option ${k===nt?'selected':''}>${k}</option>`).join('')}</select>`:`<b>${nt}</b>`}</label>
      <label class="field" style="min-width:0">Mode${isHost?`<select id="jySp"><option value="0" ${!st.split?'selected':''}>Sendiri (semua bisa atur semua divisi)</option><option value="1" ${st.split?'selected':''}>Bagi peran (1 orang 1 divisi)</option></select>`:`<b>${st.split?'Bagi peran':'Sendiri'}</b>`}</label>
      <label class="field" style="min-width:0">Level tim bot${isHost?`<select id="jyLv"><option value="easy" ${st.botLevel==='easy'?'selected':''}>Santai</option><option value="normal" ${st.botLevel!=='easy'?'selected':''}>Normal</option></select>`:`<b>${st.botLevel==='easy'?'Santai':'Normal'}</b>`}</label>
      <label class="field" style="min-width:0">⏱ Waktu per tahap${isHost?`<select id="tmrSel" class="ordsel">${timerOptions(st.timer||0)}</select>`:`<b>${timerLabel(st.timer||0)}</b>`}</label>
    </div>
    <div class="jywts">${cols}</div>
    ${none.length?`<p class="bd">Belum pilih tim: ${none.map(i=>esc(nm(st,i))).join(', ')} — nanti dimasukkan ke tim yang paling sedikit orangnya.</p>`:''}
    <p class="hint" style="text-align:left">${st.split?'Bagi peran: 5 divisi (Keuangan, SDM, Produksi, Pemasaran, Penjualan) dibagi rata ke anggota tim. Kalau anggota kurang dari 5, ada yang pegang 2 divisi. Pemegang Keuangan yang menekan “Siap jualan”.':'Mode sendiri: semua anggota tim bisa mengatur semua divisi.'} Tim tanpa anggota dimainkan bot.${st.timer?' Kalau waktu habis, rencana dikirim apa adanya.':''}</p>
    <div class="row">
      ${mi<0&&canAct?'<button class="btn pri" data-act="join">Duduk di meja ini</button>':''}
      ${mi>=0&&!isHost?'<button class="btn" data-act="leave">Tinggalkan kursi</button>':''}
      ${isHost?`<button class="btn pri" data-act="start">Mulai main</button>`:''}
      <button class="btn" data-act="tutorial" data-w="jualan">📖 Cara main</button>
      ${(isHost||isOwnerFlag)?'<button class="btn danger sm" data-act="delete">Hapus meja</button>':''}
    </div></section>`;
}
/* ---------- lawan bot (lokal) ---------- */
function jyLocalSetup(){
  const L=ui.lastJy||{me:ui.nick||'Kamu',nbot:1,level:'normal',timer:0};
  openModal(`<h3>🛍️ Jualan Yuk · lawan tim bot</h3><p class="mute" style="font-size:14px;margin:0 0 10px">Kamu pegang semua divisi timmu (Keuangan, SDM, Produksi, Pemasaran, Penjualan). 5 ronde, kas terbanyak menang.</p>
    <div class="row" style="align-items:flex-end">
      <label class="field">Nama kamu<input id="jyMeN" maxlength="20" value="${esc(L.me)}"></label>
      <label class="field" style="min-width:0">Tim lawan<select id="jyNb" style="min-width:90px">${[1,2,3].map(n=>`<option value="${n}" ${n===L.nbot?'selected':''}>${n} tim bot</option>`).join('')}</select></label>
      <label class="field" style="min-width:0">Level<select id="jyLvL" style="min-width:110px"><option value="easy" ${L.level==='easy'?'selected':''}>Santai</option><option value="normal" ${L.level!=='easy'?'selected':''}>Normal</option></select></label>
      <label class="field" style="min-width:0">⏱ Waktu per tahap<select id="jyTm" style="min-width:120px">${timerOptions(L.timer||0)}</select></label>
    </div>
    <div class="mbtns"><button class="btn" data-act="close">Batal</button><button class="btn pri" data-act="jylocalgo">Mulai</button></div>`);
}
function jyLocalStart(){
  const L={me:($('#jyMeN').value.trim())||'Kamu',nbot:+$('#jyNb').value,level:$('#jyLvL').value,timer:+($('#jyTm').value||0)};
  ui.lastJy=L; jyStartCfg(L);
}
function jyStartCfg(L){
  const s={name:'Jualan Yuk lawan bot',game:'jualan',mode:'jualan',status:'lobby',players:[{id:'H',nick:L.me,team:0}],nteams:1+L.nbot,split:false,botLevel:L.level,v:1};
  jyStart(s); s.timer=L.timer||0; s.turnAt=Date.now();
  if(cur&&cur.unsub)cur.unsub(); if(cur&&cur.botTimer)clearTimeout(cur.botTimer); ui.guideFrom=null; ui.jy=null;
  cur={local:true,st:s,human:0,level:L.level,lid:'j'+Date.now().toString(36)+Math.random().toString(36).slice(2,6)}; ui.rec=[]; view='table'; closeModal(); render();
}
async function jyOnEnded(st){
  const rid=cur.local?cur.lid:'g_'+cur.gid; if(!rid||ui.saved[rid])return; ui.saved[rid]=true;
  const order=st.teams.map((T,i)=>i).sort((a,b)=>st.teams[b].cash-st.teams[a].cash), rankOf={};order.forEach((t,k)=>rankOf[t]=k+1);
  const players=st.players.map((p,i)=>({id:cur.local?(i===cur.human?myId:null):(p.bot?null:p.id),nick:p.nick||NAMES[p.id]||'',bot:!!p.bot,pts:Math.round((st.teams[p.team]||{cash:0}).cash/1000*10)/10,cards:0,rank:rankOf[p.team]||st.teams.length,team:p.team}));
  const ts=Date.now();
  const doc={variant:'jualan',mode:cur.local?'bot':'online',level:cur.local?cur.level:null,name:st.name||'',endedAt:ts,week:weekKey(ts),rounds:st.round,ids:players.filter(p=>p.id).map(p=>p.id),players,award:{},
    teams:st.teams.map(T=>({name:T.name,cash:T.cash,stars:T.stars||0})),log:st.log.slice(-40).map(l=>({p:l.p,m:l.m}))};
  try{const ref=db.doc('results/'+rid);await lease(ref);const ex=await ref.get();if(!ex.exists){await ref.set(doc);for(const uid of doc.ids){try{await bumpStats(uid,doc,rid);}catch(e){}}}}catch(e){}
  if(!cur.local&&cur.gid){const g=cur.gid;setTimeout(()=>{db.doc('games/'+g).delete().catch(()=>{});},20000);}
}
function jyRules(){
  return `<h4>🛍️ Jualan Yuk</h4><p>Kalian direksi perusahaan kain. 2–4 tim bersaing menjual ke pasar yang sama selama <b>5 ronde</b>. Tim dengan <b>kas Keuangan terbanyak</b> di akhir menang. Modal awal tiap tim ${jyRp(JY.START)}.</p>
  <h4>Alur tiap ronde</h4><ol>
  <li><b>Demand keluar</b>: papan 3×3 (kualitas Premium/Standar/Ekonomi × harga Mahal/Normal/Murah) berisi jumlah pembeli. Dipakai bersama semua tim.</li>
  <li><b>Belanja</b> (maksimal ${jyRp(JY.CAP)} per ronde, langsung dipotong dari kas): pilih jumlah yang mau dibeli, harganya dihitung otomatis. Selama belum menekan <b>Siap jualan</b> semuanya masih bisa diubah.
    <br>👥 <b>SDM</b>: rekrut karyawan level 1/2/3 (Rp50/100/150 rb) atau latih naik 1 level (Rp50 rb). Karyawan tidak bisa dipecat.
    <br>📦 <b>Produksi</b>: barang Ekonomi/Standar/Premium (Rp50/100/150 rb). Barang tidak laku disimpan di gudang.
    <br>❤️ <b>Pemasaran</b>: CR Rp50 rb/level, permanen. CR tertinggi jualan duluan; CR sama diundi.
    <br>🪙 <b>Dana jualan</b>: uang untuk membayar tiap percobaan menjual. Sisanya tersimpan untuk ronde berikutnya.</li>
  <li><b>Penjualan</b>: pilih kotak demand, bayar biaya dari dana jualan (murah 50 rb, normal 100 rb, mahal 150 rb), lalu ambil token 1–5 dari kantong. Angka bertanda ✕ = gagal. Boleh beli 2 token <b>Pasti</b> seharga 50 rb (maks. 4) untuk menambah peluang. Kalau laku, barang terjual = terkecil dari demand, stok, dan karyawan yang mampu. Pendapatan masuk ke Keuangan. Jualan berhenti kalau kamu berhenti atau tidak bisa jualan lagi.</li></ol>
  <h4>Cara baca papan demand</h4><ul>
  <li><b>Angka besar</b>: jumlah pembeli di kotak itu (maksimal 5). Demand dipakai bersama semua tim, siapa jualan duluan dapat duluan.</li>
  <li><b>Deret token ✕ ✕ 3 4 5</b>: isi kantong token 1–5. Token bertanda ✕ berarti gagal terjual, sisanya berarti laku. Makin banyak ✕, makin kecil peluangnya. Token Pasti menambah peluang.</li>
  <li><b>laku Rp…</b>: pendapatan per barang kalau terjual.</li>
  <li><b>Ikon orang (L1/L2/L3)</b>: level karyawan yang bisa menjual di kotak itu. Redup berarti timmu belum punya karyawan level tersebut.</li>
  <li><b>biaya jual</b> di judul kolom: dibayar dari dana jualan setiap kali mencoba menjual, laku atau tidak.</li></ul>
  <h4>Kemampuan karyawan</h4>${jyAblHTML().replace('<details class="jyabl">','<div class="jyabl">').replace('</details>','</div>').replace(/<summary>.*?<\/summary>/,'')}
  <h4>Peluang laku (token gagal)</h4><p>Premium: mahal ✕1–2, normal ✕1, murah selalu laku. Standar: mahal ✕1–3, normal ✕1, murah ✕1. Ekonomi: mahal ✕1–4, normal ✕1–3, murah ✕1–2.</p>
  <h4>Pendapatan per barang</h4><p>Premium 800/650/500 rb · Standar 700/550/400 rb · Ekonomi 500/450/300 rb (mahal/normal/murah).</p>
  <h4>Bintang akhir</h4><p>⭐ kas minimal Rp5 jt · ⭐ kas terbanyak.</p>
  <h4>Mode</h4><p><b>Sendiri</b>: semua anggota tim bisa mengatur semua divisi. <b>Bagi peran</b>: tiap bagian dipegang satu orang, dan pemegang Keuangan yang menekan Siap jualan. Tim tanpa anggota dimainkan bot.</p>`;
}
