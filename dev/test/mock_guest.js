(()=>{
const S=window.__store={};const L=[];const cl=o=>o===undefined?undefined:JSON.parse(JSON.stringify(o));
const snap=(p,d)=>({id:p.split('/').pop(),exists:d!==undefined,data:()=>d,metadata:{fromCache:false,hasPendingWrites:false}});
const notify=()=>setTimeout(()=>L.forEach(f=>f()),0);
const db={doc(p){return {path:p,id:p.split('/').pop(),get:async()=>snap(p,cl(S[p])),set:async d=>{S[p]=cl(d);notify();},update:async d=>{S[p]=Object.assign(S[p]||{},cl(d));notify();},delete:async()=>{delete S[p];notify();},acquire:async()=>({acquired:true}),onSnapshot(n){const f=()=>n(snap(p,cl(S[p])));L.push(f);setTimeout(f,0);return()=>{};}};},
 collection(c){const mk=(F,O,N)=>{const run=()=>{let ks=Object.keys(S).filter(k=>k.startsWith(c+'/')&&!k.slice(c.length+1).includes('/'));let ds=ks.map(k=>({k,d:S[k]}));
   for(const [f,op,v] of F)ds=ds.filter(x=>op==='=='?x.d[f]===v:op==='array-contains'?(x.d[f]||[]).includes(v):true);
   if(O)ds.sort((a,b)=>(a.d[O[0]]>b.d[O[0]]?1:-1)*(O[1]==='desc'?-1:1));ds=ds.slice(0,N);const docs=ds.map(x=>snap(x.k,cl(x.d)));return {docs,size:docs.length,empty:!docs.length,metadata:{fromCache:false},docChanges:()=>[]};};
   return {where:(f,op,v)=>mk([...F,[f,op,v]],O,N),orderBy:(f,d)=>mk(F,[f,d||'asc'],N),limit:n=>mk(F,O,n),get:async()=>run(),onSnapshot(n){const f=()=>n(run());L.push(f);setTimeout(f,0);return()=>{};},doc:id=>db.doc(c+'/'+(id||Math.random().toString(36).slice(2)))};};
  return mk([],null,1000);}};
const user={id:async()=>'u_me',can:async()=>false,isOwner:async()=>true,profiles:async ids=>Object.fromEntries([].concat(ids).map(i=>[i,{id:i,name:'Akun '+i.slice(2)}]))};
window.claude={use:async n=>n==='db'?db:n==='user'?user:null};
})();
