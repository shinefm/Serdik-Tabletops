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
open(F,'w').write(s)
print('ok misc')
