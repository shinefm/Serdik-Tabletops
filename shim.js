/* Serdik Tabletop — adaptor Firebase.
   Meniru API window.claude.use('db'|'user'|'room') yang dipakai game, di atas Firebase compat SDK.
   - Dokumen disimpan sebagai JSON di field `_j` (aman dari undefined & array bersarang),
     ditambah beberapa field indeks untuk query (createdAt, endedAt, host, ids, ...).
   - Lobi membaca koleksi `lobby` (ringkasan kecil), bukan state penuh `games`, supaya hemat kuota baca.
   - Status online memakai Realtime Database `presence/<uid>/<tab>`. */
(function(){
  'use strict';
  if(!window.firebase||!window.FIREBASE_CONFIG){console.warn('Firebase belum dimuat');return;}
  const app=firebase.apps.length?firebase.app():firebase.initializeApp(window.FIREBASE_CONFIG);
  const auth=firebase.auth(), fs=firebase.firestore(), rtdb=firebase.database();
  const TABID=Math.random().toString(36).slice(2,10);
  const IDX=['createdAt','updatedAt','endedAt','host','ids','status','uid','game','mode','at','week'];
  const LOBBY_REFRESH=10*60e3;

  /* ---------- auth ---------- */
  try{auth.getRedirectResult().catch(()=>{});}catch(e){}
  let readyRes; const authReady=new Promise(r=>readyRes=r);
  let first=true;
  auth.onAuthStateChanged(u=>{
    if(first){first=false;readyRes(u);return;}
    // login/logout setelah halaman siap: muat ulang supaya seluruh game ikut berganti akun
    if(!!u!==!!window.__fbUser||(u&&window.__fbUser&&u.uid!==window.__fbUser.uid))location.reload();
  });
  authReady.then(u=>{window.__fbUser=u||null;});
  function errText(e){const c=e&&e.code||'';
    if(c==='auth/unauthorized-domain')return 'Alamat halaman ini belum didaftarkan di Firebase (Authentication → Settings → Authorized domains).';
    if(c==='auth/network-request-failed')return 'Koneksi internet bermasalah. Coba lagi.';
    if(c==='auth/web-storage-unsupported'||c==='auth/operation-not-supported-in-this-environment')return 'Browser ini tidak mendukung login Google. Buka link di Chrome atau Safari.';
    return 'Login gagal ('+(c||(e&&e.message)||'tidak diketahui')+'). Coba lagi, atau buka link di Chrome/Safari.';}
  window.fbLogin=async function(){
    const p=new firebase.auth.GoogleAuthProvider(); p.setCustomParameters({prompt:'select_account'});
    try{await auth.signInWithPopup(p);return true;}
    catch(e){
      const c=e&&e.code;
      if(c==='auth/popup-closed-by-user'||c==='auth/cancelled-popup-request')return false;
      if(c==='auth/popup-blocked'||c==='auth/operation-not-supported-in-this-environment'){try{await auth.signInWithRedirect(p);return true;}catch(e2){throw new Error(errText(e2));}}
      throw new Error(errText(e));
    }
  };
  window.fbLogout=async function(){try{await rtdb.ref('presence/'+(auth.currentUser&&auth.currentUser.uid)+'/'+TABID).remove();}catch(e){} await auth.signOut();};

  /* ---------- encoding ---------- */
  function enc(d){
    const o={_j:JSON.stringify(d===undefined?null:d)};
    if(d&&typeof d==='object')for(const k of IDX){const v=d[k];
      if(v===undefined||v===null)continue;
      if(typeof v==='string'||typeof v==='number'||typeof v==='boolean')o[k]=v;
      else if(Array.isArray(v)&&v.every(x=>typeof x==='string'))o[k]=v;}
    return o;
  }
  function dec(raw){if(!raw)return raw;if(typeof raw._j==='string'){try{return JSON.parse(raw._j);}catch(e){return null;}}return raw;}
  function lobbySummary(st){
    if(!st||typeof st!=='object')return null;
    const keep=['name','status','host','createdAt','updatedAt','game','mode','timer','nteams','split','botLevel','special'];
    const s={_sum:1}; for(const k of keep)if(st[k]!==undefined)s[k]=st[k];
    s.players=(st.players||[]).map(p=>{const q={id:p.id};if(p.nick)q.nick=p.nick;if(p.bot)q.bot=true;if(p.team!=null)q.team=p.team;return q;});
    return s;
  }
  function sumKey(s){const c=Object.assign({},s);delete c.updatedAt;return JSON.stringify(c);}

  /* ---------- snapshots ---------- */
  function wrapDoc(s){return {exists:s.exists,id:s.id,data:()=>dec(s.data()),metadata:s.metadata||{fromCache:false}};}
  function wrapQuery(s){const docs=s.docs.map(wrapDoc);return {docs,size:docs.length,empty:!docs.length,metadata:s.metadata||{fromCache:false},forEach:f=>docs.forEach(f)};}
  const isGame=p=>/^games\/[^/]+$/.test(p);
  const lobbyPath=p=>'lobby/'+p.split('/')[1];

  /* ---------- document ref ---------- */
  function docRef(path){
    const r=fs.doc(path);
    return {
      id:r.id, path,
      async get(){return wrapDoc(await r.get());},
      async set(data){
        if(isGame(path)){
          const s=lobbySummary(data), raw=enc(data); raw._lh=sumKey(s); raw._lt=Date.now();
          const b=fs.batch(); b.set(r,raw); b.set(fs.doc(lobbyPath(path)),enc(s)); await b.commit(); return;
        }
        await r.set(enc(data));
      },
      async delete(){
        if(isGame(path)){const b=fs.batch();b.delete(r);b.delete(fs.doc(lobbyPath(path)));await b.commit();return;}
        await r.delete();
      },
      onSnapshot(next,err){return r.onSnapshot(s=>next(wrapDoc(s)),e=>err&&err(e));},
      /* kunci sederhana (dipakai saat menyimpan hasil & statistik) */
      async acquire(o){
        const lr=fs.doc('locks/'+path.replace(/\//g,'__'));
        try{
          const ok=await fs.runTransaction(async t=>{const s=await t.get(lr);const d=s.exists?s.data():null;const now=Date.now();
            if(d&&d.until>now&&d.holder!==o.holder)return false; t.set(lr,{holder:o.holder,until:now+(o.ttlMs||5000)}); return true;});
          return {acquired:ok};
        }catch(e){return {acquired:true};}
      }
    };
  }
  /* transaksi baca-ubah-tulis untuk satu dokumen (dipakai untuk setiap langkah game) */
  async function txn(path,fn){
    const r=fs.doc(path);
    return fs.runTransaction(async t=>{
      const s=await t.get(r); const raw=s.exists?s.data():null;
      const out=fn(raw?dec(raw):null);
      if(out===undefined)return out;
      const w=enc(out);
      if(isGame(path)){
        const sm=lobbySummary(out), k=sumKey(sm), now=Date.now();
        if(!raw||raw._lh!==k||!(raw._lt>now-LOBBY_REFRESH)){w._lh=k;w._lt=now;t.set(fs.doc(lobbyPath(path)),enc(sm));}
        else{w._lh=raw._lh;w._lt=raw._lt;}
      }
      t.set(r,w); return out;
    });
  }

  /* ---------- query ---------- */
  function query(coll,ops){
    ops=ops||[];
    const q={
      where(f,op,v){return query(coll,ops.concat([['w',f,op,v]]));},
      orderBy(f,dir){return query(coll,ops.concat([['o',f,dir||'asc']]));},
      limit(n){return query(coll,ops.concat([['l',n]]));},
      doc(id){return docRef((coll==='lobby'?'games':coll)+'/'+id);},
      build(){
        let r=fs.collection(coll);
        const ws=ops.filter(o=>o[0]==='w'), os=ops.filter(o=>o[0]==='o'), ls=ops.filter(o=>o[0]==='l');
        ws.forEach(o=>{r=r.where(o[1],o[2],o[3]);});
        // where + orderBy pada field lain butuh indeks gabungan: urutkan di browser saja
        const clientSort=ws.length&&os.length&&os.some(o=>!ws.some(w=>w[1]===o[1]));
        if(!clientSort)os.forEach(o=>{r=r.orderBy(o[1],o[2]);});
        if(ls.length)r=r.limit(ls[ls.length-1][1]);
        return {r,clientSort,os};
      },
      post(w,b){if(b.clientSort){const o=b.os[0];const dir=o[2]==='desc'?-1:1;w.docs.sort((a,c)=>{const x=(a.data()||{})[o[1]]||0,y=(c.data()||{})[o[1]]||0;return x<y?-dir:x>y?dir:0;});}return w;},
      async get(){const b=q.build();return q.post(wrapQuery(await b.r.get()),b);},
      onSnapshot(next,err){const b=q.build();return b.r.onSnapshot(s=>next(q.post(wrapQuery(s),b)),e=>err&&err(e));}
    };
    return q;
  }
  const db={
    doc:docRef,
    collection(name){return query(name==='games'?'lobby':name);},
    __txn:txn
  };

  /* ---------- user ---------- */
  let ownerP=null, profCache={};
  function userApi(u){return {
    async id(){return u.uid;},
    async can(){return true;},
    async isOwner(){if(!ownerP)ownerP=fs.doc('meta/owners').get().then(s=>{const d=s.exists?s.data():null;return !!(d&&Array.isArray(d.uids)&&d.uids.includes(u.uid));}).catch(()=>false);return ownerP;},
    async email(){return u.email||null;},
    async me(){return {name:u.displayName||'',avatarUrl:u.photoURL||null};},
    async profiles(ids){
      const out={}, need=[];
      for(const id of ids){if(profCache[id])out[id]=profCache[id];else if(typeof id==='string'&&id&&!id.startsWith('bot'))need.push(id);}
      await Promise.all(need.slice(0,30).map(id=>fs.doc('users/'+id).get().then(s=>{const d=s.exists?s.data():null;profCache[id]={name:(d&&d.name)||''};out[id]=profCache[id];}).catch(()=>{})));
      return out;
    }
  };}

  /* ---------- room (status online) ---------- */
  function roomApi(u){
    const mine=rtdb.ref('presence/'+u.uid+'/'+TABID); let last={uid:u.uid,g:null};
    rtdb.ref('.info/connected').on('value',s=>{if(s.val()===true){mine.onDisconnect().remove().then(()=>mine.set(Object.assign({},last,{t:firebase.database.ServerValue.TIMESTAMP}))).catch(()=>{});}});
    return {
      presence(p){last={uid:u.uid,g:(p&&p.g)||null};return mine.set(Object.assign({},last,{t:firebase.database.ServerValue.TIMESTAMP}));},
      onPeers(cb){const ref=rtdb.ref('presence');const h=s=>{const peers=[];s.forEach(us=>{us.forEach(t=>{const v=t.val()||{};peers.push({by:v.uid||us.key,presence:v});});});cb({peers});};ref.on('value',h);return ()=>ref.off('value',h);},
      on(){return ()=>{};},
      emit(){return Promise.resolve();}
    };
  }

  /* ---------- pintu masuk yang dipanggil game ---------- */
  window.claude={
    async use(name){
      const u=await authReady;
      if(!u)return null;
      if(name==='db')return db;
      if(name==='user')return userApi(u);
      if(name==='room')return roomApi(u);
      return null;
    }
  };
  // simpan nama tampilan supaya pemain lain bisa melihatnya
  authReady.then(u=>{if(u)fs.doc('users/'+u.uid).set({name:u.displayName||'',updatedAt:Date.now()},{merge:true}).catch(()=>{});});
  window.__fbReady=authReady;
})();
