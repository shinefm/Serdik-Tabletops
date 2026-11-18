# Saudagar Permata: istilah "tukar" untuk batas 10 token, dan pengingat waktu giliran
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b):
    global s
    n=s.count(a); assert n==1,(n,a[:90]); s=s.replace(a,b)

# 1. Batas 10 token: bukan "buang", tapi harus ditukar (token lama kembali ke bank)
rep("→ harus buang ${after-max}`","→ harus tukar ${after-max}`")
rep("'Penuh: ambil lagi = harus buang'","'Penuh: ambil lagi = harus tukar'")
rep("fail('Pilihan buang token tidak valid')","fail('Pilihan tukar token tidak valid')")
rep("if(disN)msg+='; mengembalikan '+fmtTok(dis);","if(disN)msg+='; menukar balik '+fmtTok(dis)+' ke bank';")
rep("msgs.push('mengembalikan '+","msgs.push('menukar balik '+")
rep("""<h3>Kembalikan ${ex.over} token</h3><p class="mute" style="font-size:14px;margin:0">Maksimal ${MAXTOK} token di tangan. Klik token yang ingin dikembalikan ke bank (${sum}/${ex.over}).</p>""",
    """<h3>🔄 Tukar ${ex.over} token</h3><p class="mute" style="font-size:14px;margin:0">Maksimal ${MAXTOK} token di tangan, jadi token baru harus ditukar dengan token lama. Klik token lama yang ingin ditukar ke bank (${sum}/${ex.over}).</p>""")
rep("kelebihan harus dikembalikan.</p>","kelebihan harus ditukar (token lama kembali ke bank).</p>")

# 2. Pengingat waktu: sisa 1 menit (kalau timer > 1 menit) dan sisa 30 detik
rep("""  if(l==null||l>0||cur.guided||ui.tmrBusy)return;
  if(st.game==='jualan'){""","""  tmrRemind(st,l);
  if(l==null||l>0||cur.guided||ui.tmrBusy)return;
  if(st.game==='jualan'){""")
rep("function tickTimer(){","""function tmrRemind(st,l){
  if(l==null||l<=0||cur.guided||(st.game&&st.game!=='pemukim'))return;
  const me=typeof turnSeat==='function'?turnSeat(st):actor(st);
  if(me<0||st.turn!==me||(st.players[st.turn]||{}).bot)return;
  const k=(cur.lid||cur.gid||'x')+':'+st.turnAt+':';
  const marks=[[60000,'Tinggal 1 menit'],[30000,'Tinggal 30 detik']].filter(([ms])=>st.timer*1000>ms);
  for(const [ms,txt] of marks){
    if(l>ms||l<=ms-3000||ui.tmrRem===k+ms)continue;   // muncul sekali saat melewati batas
    ui.tmrRem=k+ms;
    if(typeof turnPill==='function')turnPill(`⏱ <b>${txt}</b> untuk giliranmu`,'tmrwarn');else toast('⏱ '+txt);
    try{navigator.vibrate&&navigator.vibrate(ms===30000?[120,80,120]:150);}catch(e){}
    break;
  }
}
function tickTimer(){""")
rep("</style>","""#turnPill.tmrwarn{border-color:#ff8a4c;background:#3a1f12;color:#ffe9dc}
body.light #turnPill.tmrwarn{background:#fff1e8;color:#7a2e08;border-color:#e8692a}
</style>""")
open(F,'w').write(s)
print('ok sp2')
