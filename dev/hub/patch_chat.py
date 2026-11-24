# Chat meja online: tab "Chat" di samping "Catatan" pada setiap game (chat.js).
# Pesan sementara di Realtime Database chat/<gid>, dihapus saat game selesai / meja dihapus.
import re
F='saudagar-permata.html'
s=open(F).read()
def rep(a,b):
    global s
    n=s.count(a); assert n==1,(n,a[:90]); s=s.replace(a,b)

# 1. modul chat, sebelum render() supaya bisa membungkusnya
rep("function render(){\n",open('hub/chat.js').read()+"\nfunction render(){\n")

# 2. panel Catatan -> tab Catatan | Chat (semua game: Permata klasik/mobile/duel, Rapat, Sandi, Werewolf, Pemukim, WK)
pat=re.compile(r'<details class="panel log" (\$\{[^}]*\}[^ ]*) ontoggle="ui\.logOpen=this\.open"><summary style="([^"]*)">(Catatan [a-z]+)</summary>\$\{logs\}</details>')
def sub(m):
    return ('<details class="panel log${chatCls()}" '+m.group(1)+' ontoggle="ui.logOpen=this.open"><summary style="'+m.group(2)+'">'
            "${logSum('"+m.group(3)+"')}</summary>${logPanes(logs)}</details>")
s,n=pat.subn(sub,s); assert n==8,n
# Jualan Yuk
rep("""<section class="panel"><details ${innerWidth>900?'open':''}><summary><b>Catatan permainan</b></summary><div class="logbox">${log}</div></details></section>""",
    """<section class="panel${chatOn()?' jychat':''}"><details ${(chatOn()?(ui.logOpen??(innerWidth>900)):innerWidth>900)?'open':''} ontoggle="if(chatOn())ui.logOpen=this.open"><summary>${logSum('<b>Catatan permainan</b>')}</summary>${logPanes('<div class="logbox">'+log+'</div>')}</details></section>""")

# 3. meja dihapus -> chat ikut dihapus
rep("function render(){\n","function chatClearGid(id){if(!id)return;chatApi().then(a=>{if(a)return a.clear(id);}).catch(()=>{});}\nfunction render(){\n")
rep("case 'lobdelok':{closeModal();const id=ui.lobDel;ui.lobDel=null;if(!id)break;try{await db.doc('games/'+id).delete();",
    "case 'lobdelok':{closeModal();const id=ui.lobDel;ui.lobDel=null;if(!id)break;try{await db.doc('games/'+id).delete();chatClearGid(id);")
rep("case 'delok':closeModal();try{await db.doc('games/'+cur.gid).delete();",
    "case 'delok':closeModal();try{chatClearGid(cur.gid);await db.doc('games/'+cur.gid).delete();")
rep("try{await db.doc('games/'+g._id).delete();n++;}catch(e){}",
    "try{await db.doc('games/'+g._id).delete();chatClearGid(g._id);n++;}catch(e){}")

# 4. gaya
rep("</style>","""/* --- chat meja --- */
.log.haschat{max-height:none;overflow:visible}
.log .lgpane{padding:0;border:0}
.log.haschat .lglog{max-height:220px;overflow:auto}
.lgtabs{display:inline-flex;gap:4px;padding:3px;border:1px solid var(--line);border-radius:999px;background:var(--panel);vertical-align:middle}
.lgtabs button{font:inherit;font-size:14px;color:var(--mute);background:none;border:0;border-radius:999px;padding:5px 12px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;min-height:34px}
.lgtabs button b{color:inherit}
.lgtabs button.on{background:var(--gold);color:#1f1830;font-weight:700}
.lgtabs .cbadge{font-style:normal;font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:800;min-width:18px;height:18px;line-height:18px;padding:0 5px;border-radius:999px;background:#e5484d;color:#fff;text-align:center}
.lgtabs .cbadge[hidden]{display:none}
.chatbox{display:flex;flex-direction:column;gap:8px;margin-top:8px}
.log .chatbox,.log .chatbox div{padding:0;border:0}
.chatlist{max-height:240px;min-height:120px;overflow:auto;display:flex;flex-direction:column;gap:6px;padding:4px 2px}
.log .chatlist .cmsg,.chatlist .cmsg{align-self:flex-start;max-width:86%;padding:6px 10px;border:1px solid var(--line);border-radius:12px 12px 12px 4px;background:var(--panel);font-size:13.5px;line-height:1.35;overflow-wrap:anywhere}
.log .chatlist .cmsg.me,.chatlist .cmsg.me{align-self:flex-end;border-radius:12px 12px 4px 12px;background:color-mix(in srgb,var(--gold) 22%,var(--panel))}
.cmsg .cn{display:block;font-weight:800;font-size:12px;color:var(--gold)}
.cmsg .cw{display:block;font-size:10.5px;color:var(--mute);text-align:right;margin-top:2px}
.chatempty{color:var(--mute);font-size:13px;text-align:center;margin:auto 0}
.chatin{display:flex;gap:6px}
.chatin input{flex:1;min-width:0;padding:9px 12px;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--ink);font:inherit;font-size:16px}
.chatin input:disabled{opacity:.65}
.chatnote{font-size:11.5px;color:var(--mute)}
.jychat summary{list-style:none;cursor:pointer}
.jychat .lglog{max-height:240px;overflow:auto}
</style>""")
open(F,'w').write(s)
print('ok')
