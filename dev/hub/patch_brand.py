p='saudagar-permata.html'; s=open(p).read()
for a,b in [("<title>Saudagar Permata — P3MD</title>","<title>Serdik Games — P3MD</title>"),
 ('''<svg class="gem" style="width:40px;height:40px;filter:drop-shadow(2px 2px 0 #111)" viewBox="0 0 40 40"><use href="#gem-r"/></svg>
      <div><h1>Saudagar Permata</h1><small>Permainan dagang permata · P3MD</small></div>''','''<span class="brandico" aria-hidden="true">🎲</span>
      <div><h1>Serdik Games</h1><small>Game papan online · P3MD</small></div>'''),
 ("body.light .rtag.o{",".brandico{font-size:36px;line-height:1;filter:drop-shadow(2px 2px 0 #111)}\nbody.light .rtag.o{")]:
    assert s.count(a)==1,a[:60]; s=s.replace(a,b)
open(p,'w').write(s); print('brand ok')
