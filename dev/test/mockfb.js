/* Tiruan Firebase compat SDK (memori) untuk tes. Meniru batasan Firestore yang penting:
   tolak nilai undefined & array bersarang, tolak where+orderBy beda field (butuh indeks). */
(function(){
  const clone=x=>x===undefined?undefined:JSON.parse(JSON.stringify(x));
  const later=f=>setTimeout(f,0);
  function check(v,path,inArr){
    if(v===undefined)throw Object.assign(new Error('Unsupported field value: undefined ('+path+')'),{code:'invalid-argument'});
    if(Array.isArray(v)){if(inArr)throw Object.assign(new Error('Nested arrays are not supported ('+path+')'),{code:'invalid-argument'});v.forEach((x,i)=>check(x,path+'.'+i,true));return;}
    if(v&&typeof v==='object')for(const k in v)check(v[k],path+'.'+k,false);
  }
  /* ---------- auth ---------- */
  let user=null;
  try{const u=window.__MOCKUSER!==undefined?window.__MOCKUSER:JSON.parse(localStorage.getItem('mockfb_user')||'null');user=u===undefined?null:u;}catch(e){}
  if(window.__MOCKUSER===undefined&&user===null&&localStorage.getItem('mockfb_user')===null)user={uid:'u_me',email:'me@example.com',displayName:'Farhan',photoURL:null};
  const authL=[];
  const auth={get currentUser(){return user;},
    onAuthStateChanged(cb){authL.push(cb);later(()=>cb(user));return()=>{};},
    async signInWithPopup(){user=window.__MOCKLOGIN||{uid:'u_new',email:'new@example.com',displayName:'Baru'};try{localStorage.setItem('mockfb_user',JSON.stringify(user));}catch(e){}authL.forEach(f=>later(()=>f(user)));return {user};},
    async signInWithRedirect(){return this.signInWithPopup();},
    async getRedirectResult(){return {user:null};},
    async signOut(){user=null;try{localStorage.setItem('mockfb_user','null');}catch(e){}authL.forEach(f=>later(()=>f(null)));}};
  function GoogleAuthProvider(){}GoogleAuthProvider.prototype.setCustomParameters=function(){};
  /* ---------- firestore ---------- */
  const S=window.__FS=window.__FS||{}; const docL={}, qL=[];
  window.__FSOPS={reads:0,writes:0};
  function snapDoc(path){const d=S[path];return {exists:d!==undefined,id:path.split('/').pop(),data:()=>clone(d),metadata:{fromCache:false}};}
  function notify(path){(docL[path]||[]).forEach(f=>later(()=>{window.__FSOPS.reads++;f(snapDoc(path));}));const coll=path.split('/').slice(0,-1).join('/');qL.filter(q=>q.coll===coll).forEach(q=>later(()=>q.fire()));}
  function write(path,data,opt){check(data,path,false);window.__FSOPS.writes++;S[path]=opt&&opt.merge&&S[path]?Object.assign(S[path],clone(data)):clone(data);notify(path);}
  function del(path){window.__FSOPS.writes++;delete S[path];notify(path);}
  function docRef(path){return {id:path.split('/').pop(),path,
    async get(){window.__FSOPS.reads++;return snapDoc(path);},
    async set(d,o){write(path,d,o);}, async delete(){del(path);},
    onSnapshot(n,e){(docL[path]=docL[path]||[]).push(n);later(()=>{window.__FSOPS.reads++;n(snapDoc(path));});return()=>{docL[path]=(docL[path]||[]).filter(x=>x!==n);};}};}
  function coll(name,ops){ops=ops||[];
    function run(){
      const ws=ops.filter(o=>o[0]==='w'),os=ops.filter(o=>o[0]==='o'),ls=ops.filter(o=>o[0]==='l');
      if(ws.length&&os.some(o=>!ws.some(w=>w[1]===o[1])))throw Object.assign(new Error('The query requires an index'),{code:'failed-precondition'});
      let rows=Object.keys(S).filter(p=>p.split('/').slice(0,-1).join('/')===name).map(p=>({p,d:S[p]}));
      ws.forEach(([_,f,op,v])=>{rows=rows.filter(r=>op==='=='?r.d[f]===v:op==='array-contains'?Array.isArray(r.d[f])&&r.d[f].includes(v):true);});
      os.forEach(([_,f,dir])=>{rows=rows.filter(r=>r.d[f]!==undefined);rows.sort((a,b)=>(a.d[f]<b.d[f]?-1:a.d[f]>b.d[f]?1:0)*(dir==='desc'?-1:1));});
      if(ls.length)rows=rows.slice(0,ls[ls.length-1][1]);
      window.__FSOPS.reads+=Math.max(1,rows.length);
      const docs=rows.map(r=>snapDoc(r.p));return {docs,size:docs.length,empty:!docs.length,metadata:{fromCache:false},forEach:f=>docs.forEach(f)};
    }
    return {where:(f,op,v)=>coll(name,ops.concat([['w',f,op,v]])),orderBy:(f,d)=>coll(name,ops.concat([['o',f,d||'asc']])),limit:n=>coll(name,ops.concat([['l',n]])),
      doc:id=>docRef(name+'/'+id),
      async get(){return run();},
      onSnapshot(n,e){const q={coll:name,fire(){try{n(run());}catch(err){e&&e(err);}}};qL.push(q);later(()=>q.fire());return()=>{const i=qL.indexOf(q);if(i>=0)qL.splice(i,1);};}};}
  let txChain=Promise.resolve();
  const fs={doc:docRef,collection:n=>coll(n),
    batch(){const ops=[];return {set(r,d,o){ops.push(()=>write(r.path,d,o));},delete(r){ops.push(()=>del(r.path));},async commit(){ops.forEach(f=>f());}};},
    runTransaction(fn){const p=txChain.then(async()=>{const ops=[];const t={async get(r){window.__FSOPS.reads++;return snapDoc(r.path);},set(r,d,o){check(d,r.path,false);ops.push(()=>write(r.path,d,o));},delete(r){ops.push(()=>del(r.path));}};
      const out=await fn(t);ops.forEach(f=>f());return out;});txChain=p.catch(()=>{});return p;}};
  /* ---------- realtime database ---------- */
  const R={}; const rL=[];
  function getAt(path){if(path==='.info/connected')return true;let o=R;for(const k of path.split('/').filter(Boolean)){if(o==null||typeof o!=='object')return null;o=o[k];}return o===undefined?null:o;}
  function setAt(path,v){const ks=path.split('/').filter(Boolean);let o=R;for(let i=0;i<ks.length-1;i++){o=o[ks[i]]=o[ks[i]]&&typeof o[ks[i]]==='object'?o[ks[i]]:{};}if(v===null)delete o[ks[ks.length-1]];else o[ks[ks.length-1]]=clone(v);const P=ks.join('/');rL.filter(l=>!l.path.startsWith('.info')&&(P.startsWith(l.path)||l.path.startsWith(P))).forEach(l=>later(()=>l.f(snap(l.path))));}
  function snap(path){const v=getAt(path);return {key:path.split('/').pop(),val:()=>clone(v),forEach(f){if(v&&typeof v==='object')Object.keys(v).forEach(k=>f(snap(path+'/'+k)));}};}
  function rref(path){return {key:path.split('/').pop(),
    async set(v){const T=x=>x&&typeof x==='object'?Object.fromEntries(Object.entries(x).map(([k,y])=>[k,y&&y['.sv']?Date.now():T(y)])):x;setAt(path,T(v));},
    async remove(){setAt(path,null);},
    on(ev,f){rL.push({path,f});later(()=>f(snap(path)));return f;},
    off(ev,f){const i=rL.findIndex(l=>l.f===f);if(i>=0)rL.splice(i,1);},
    onDisconnect(){return {remove:async()=>{}};}};}
  const rtdb={ref:rref};
  const apps=[];
  window.firebase={apps,initializeApp(c){apps.push({c});return apps[0];},app(){return apps[0];},
    auth:Object.assign(()=>auth,{GoogleAuthProvider}),
    firestore:()=>fs,
    database:Object.assign(()=>rtdb,{ServerValue:{TIMESTAMP:{'.sv':'timestamp'}}})};
  window.__RTDB=R;
  window.__store=new Proxy({},{get:(t,k)=>{const d=S[k];return d&&typeof d._j==='string'?JSON.parse(d._j):d;},has:(t,k)=>k in S});
})();
