# Tambahan kecil antarmuka
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b):
    global s
    n=s.count(a); assert n==1,(n,a[:90]); s=s.replace(a,b)

# Judul "Serdik Tabletop" di kiri atas: kembali ke lobi
rep('    <div class="brand">\n      <span class="brandico" aria-hidden="true">🎲</span>',
    '    <div class="brand" data-act="home" role="button" tabindex="0" title="Kembali ke lobi" aria-label="Serdik Tabletop, kembali ke lobi">\n      <span class="brandico" aria-hidden="true">🎲</span>')
rep("    case 'lobby':leaveTable();break;",
    "    case 'lobby':leaveTable();break;\n    case 'home':if(modalOpen())closeModal();if(view==='table')leaveTable();else window.scrollTo({top:0,behavior:'smooth'});break;")
rep("</style>",".brand[data-act=\"home\"]{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent}\n.brand[data-act=\"home\"]:active{transform:scale(.97)}\n</style>")
# Tag MK di kartu game
rep("desc:'Kumpulkan permata, beli kartu tambang sampai istana, dan raih dukungan pahlawan nasional. Bisa lawan bot.',mk:[['MK02','investasi bertahap']]",
    "desc:'Kumpulkan permata, beli kartu tambang sampai istana, dan raih dukungan pahlawan nasional. Bisa lawan bot.',mk:[['MK02','investasi bertahap'],['MK05','decision making & game theory']]")
rep("mk:[['MK02','alokasi anggaran'],['MK03','segmen & harga'],['MK04','kapasitas produksi']]",
    "mk:[['MK02','alokasi anggaran'],['MK03','marketing'],['MK04','kapasitas produksi']]")
# Animasi dapat pahlawan / bangsawan / kota
aw=open('hub/award.js').read()
rep("function maybeEndPopup(st){",aw+"\nfunction maybeEndPopup(st){")
n=s.count("maybeEndPopup(st); maybeRankPop(st); maybeBot(); maybeOnlineBot();"); assert n==3,n
s=s.replace("maybeEndPopup(st); maybeRankPop(st); maybeBot(); maybeOnlineBot();","awardWatch(st); maybeEndPopup(st); maybeRankPop(st); maybeBot(); maybeOnlineBot();")
rep("</style>",'''/* --- animasi dapat pahlawan/kota --- */
.awov{position:fixed;inset:0;z-index:9500;display:grid;place-items:center;background:rgba(20,14,8,.55);backdrop-filter:blur(2px);animation:awfade .25s ease-out;cursor:pointer;overflow:hidden}
.awov.out{animation:awfadeout .35s ease-in forwards}
.awrays{position:absolute;width:160vmax;height:160vmax;left:50%;top:50%;margin:-80vmax 0 0 -80vmax;background:repeating-conic-gradient(rgba(255,214,94,.28) 0 10deg,transparent 10deg 20deg);animation:awspin 9s linear infinite,awfade .6s ease-out;mask:radial-gradient(circle,#000 0,transparent 55%);-webkit-mask:radial-gradient(circle,#000 0,transparent 55%)}
.awbox{position:relative;display:flex;flex-direction:column;align-items:center;gap:14px;perspective:900px}
.awcard{animation:awpop .9s cubic-bezier(.2,1.4,.4,1) both;filter:drop-shadow(0 12px 24px rgba(0,0,0,.5)) drop-shadow(0 0 22px rgba(255,214,94,.65))}
.awpat{width:150px}.awpat .patron{width:150px;cursor:default}.awpat.awroy{width:170px}
.awkota{width:210px;border:3px solid #3b2a20;border-radius:12px;overflow:hidden;background:#f4efe3;box-shadow:0 0 0 3px #f0c55e}
.awkota .kart{width:100%;height:auto;aspect-ratio:100/70}.awkota .kart .kn{font-size:16px;padding:3px 10px 3px 8px}
.awtxt{text-align:center;color:#fff8e6;animation:awup .5s .35s ease-out both}
.awt{font:800 21px/1.2 Fraunces,serif;text-shadow:0 2px 8px rgba(0,0,0,.6)}
.aws{margin-top:4px;font-size:15px;color:#ffe9a8;text-shadow:0 1px 4px rgba(0,0,0,.6)}
.awov.me .awt{color:#ffe14d}
.awconf{position:absolute;inset:0;pointer-events:none}
.awconf i{position:absolute;left:50%;top:42%;width:9px;height:14px;border-radius:2px;background:hsl(calc(var(--k)*26),85%,60%);animation:awconf 1.4s calc(var(--k)*25ms) ease-out both;--a:calc(var(--k)*25.7deg)}
@keyframes awfade{from{opacity:0}to{opacity:1}}
@keyframes awfadeout{to{opacity:0}}
@keyframes awspin{to{transform:rotate(360deg)}}
@keyframes awpop{0%{transform:translateZ(-600px) rotateY(160deg) scale(.15);opacity:0}55%{transform:translateZ(60px) rotateY(-12deg) scale(1.18);opacity:1}75%{transform:rotateY(6deg) scale(.96)}100%{transform:none}}
@keyframes awup{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes awconf{0%{transform:translate(-50%,-50%) rotate(var(--a)) translateY(0) scale(.4);opacity:1}100%{transform:translate(-50%,-50%) rotate(var(--a)) translateY(-46vmin) rotate(220deg);opacity:0}}
@media(prefers-reduced-motion:reduce){.awcard,.awrays,.awconf i{animation:none}}
</style>''')
# Kartu pasar Tingkat I-III berbentuk persegi (Klasik & Kota)
rep("</style>",'''/* --- kartu pasar persegi --- */
.tier-row .card.rc{aspect-ratio:1/1}
.tier-row .deck{aspect-ratio:auto}
.tier-row .rc .rhead{height:27cqw;padding:0 3.5cqw 0 4.5cqw}
.tier-row .rc .rpts{font-size:25cqw}
.tier-row .rc .rgem{width:21cqw;height:21cqw}
.tier-row .rc .rcost{flex-direction:row;flex-wrap:wrap-reverse;width:44cqw;gap:2cqw;left:6cqw;bottom:6cqw}
.tier-row .rchip{width:19cqw;height:19cqw;font-size:15cqw}
.tier-row .rc .rtier{right:6cqw;bottom:6cqw;font-size:10cqw}
.tier-row .card.rc.can::after{top:52%}
.tier-row .rc .rart svg{object-fit:cover}
</style>''')
open(F,'w').write(s)
print('ok misc')
