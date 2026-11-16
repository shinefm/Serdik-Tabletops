/* ================= GERBANG LOGIN / AKSES ================= */
function inAppBrowser(){const u=navigator.userAgent||'';return /WhatsApp|FBAN|FBAV|Instagram|Line\/|Telegram|TikTok|Twitter|LinkedInApp/i.test(u)?(/WhatsApp/i.test(u)?'WhatsApp':/Instagram/i.test(u)?'Instagram':/Telegram/i.test(u)?'Telegram':/Line\//i.test(u)?'LINE':'aplikasi ini'):null;}
function pageLink(){return (LEAGUE_URL||'')+(location.hash||'');}
function chromeIntent(){const u=pageLink();return /Android/i.test(navigator.userAgent||'')&&/^https:\/\//.test(u)?'intent://'+u.slice(8)+'#Intent;scheme=https;package=com.android.chrome;end':'';}
function accessGateHTML(){
  if(EDITION==='latihan'||online==='connecting')return '';
  if(online==='off'){
    const app=inAppBrowser();
    return `<section class="panel gate"><div class="gh"><span class="gi">🔐</span><div><h2>Login dulu untuk main online</h2><p class="bd" style="margin:2px 0 0">Meja online, profil, dan peringkat hanya muncul kalau kamu membuka halaman ini dalam keadaan <b>sudah login ke Claude</b>.</p></div></div>
      ${app?`<div class="gwarn">⚠️ Kamu membuka link dari <b>${app}</b>. Browser bawaan ${app} tidak bisa login ke Claude. ${chromeIntent()?`<a class="btn pri" style="margin:6px 0;display:inline-block;text-decoration:none" href="${esc(chromeIntent())}">🌐 Buka di Chrome</a><br>Kalau tombol itu tidak jalan: `:''}ketuk <b>⋮</b> atau ikon kompas di pojok, lalu pilih <b>Buka di Chrome</b> (Android) atau <b>Buka di Safari</b> (iPhone).</div>`:''}
      <ol class="gsteps"><li>Buka link ini di <b>Chrome</b> atau <b>Safari</b>${app?'':' (bukan dari dalam WhatsApp)'}.</li>
        <li>Login ke <b>claude.ai</b>. Bisa pakai <b>“Lanjutkan dengan Google”</b>, dan belum punya akun? Daftar gratis.</li>
        <li>Buka lagi link Serdik Games / link meja dari temanmu.</li>
        <li>Pakai <b>email yang sudah diundang</b> tuan rumah. Kalau belum diundang, halaman ini akan menampilkan emailmu untuk dikirim ke mereka.</li></ol>
      <div class="row" style="gap:8px"><a class="btn pri" href="${esc(pageLink())}" target="_blank" rel="noopener">🔑 Login ke Claude</a><button class="btn" data-act="gatecopy">🔗 Salin link halaman ini</button></div>
      <p class="bd" style="margin:8px 0 0">Belum sempat login? Kamu tetap bisa main <b>🤖 lawan bot</b> di bawah, tapi hasilnya tidak tercatat.</p></section>`;
  }
  if(online==='on'&&canWrite===false){
    const em=ui.email||'';
    const wa='https://wa.me/?text='+encodeURIComponent(`Halo, tolong undang email saya${em?' '+em:''} ke Serdik Games (Share → Invite people by email → akses "Commenter") supaya saya bisa main online 🙏 ${LEAGUE_URL||''}`);
    return `<section class="panel gate"><div class="gh"><span class="gi">✉️</span><div><h2>Akunmu belum diundang</h2><p class="bd" style="margin:2px 0 0">Kamu sudah login, tapi akunmu baru bisa <b>melihat</b>. Supaya bisa duduk di meja, tuan rumah perlu mengundang emailmu lewat tombol <b>Share</b> di claude.ai dengan akses <b>Commenter</b>.</p></div></div>
      ${em?`<div class="gmail"><span class="bd">Emailmu:</span> <b>${esc(em)}</b></div>`:''}
      <div class="row" style="gap:8px">${em?'<button class="btn" data-act="gatemail">📋 Salin email</button>':''}<a class="btn wa" href="${esc(wa)}" target="_blank" rel="noopener">${WA_ICON} Kirim ke tuan rumah</a></div>
      <p class="bd" style="margin:8px 0 0">Setelah diundang, buka <b>email undangan dari Claude</b> → <b>View invitation</b> → <b>Accept and open</b>. Kalau sudah diundang tapi pesan ini tetap muncul, minta tuan rumah mengubah akses link dari “Anyone with the link” ke “Only you”. Sambil menunggu, kamu bisa main 🤖 lawan bot.</p></section>`;
  }
  return '';
}
function openLoginPop(){
  const app=inAppBrowser();
  openModal(`<div style="text-align:center"><div style="font-size:52px;line-height:1.1">🔐</div><h3 style="font-size:22px;margin:6px 0 4px">Masuk dulu, yuk!</h3>
    <p style="font-size:14.5px;line-height:1.55;margin:0 0 10px">Supaya bisa <b>main online bareng teman</b>, punya profil, rekor, dan peringkat, kamu perlu login ke <b>Claude</b>. Bisa langsung pakai akun <b>Google</b>, gratis.</p></div>
    ${app?`<div class="gwarn">⚠️ Kamu membuka dari <b>${app}</b>. Login Claude tidak bisa di browser bawaan ${app}. ${chromeIntent()?`<a class="btn pri" style="margin:6px 0;display:inline-block;text-decoration:none" href="${esc(chromeIntent())}">🌐 Buka di Chrome</a><br>Atau `:''}ketuk <b>⋮</b> / ikon kompas lalu pilih <b>Buka di Chrome/Safari</b>.</div>`:''}
    <ol class="gsteps" style="margin-bottom:6px"><li>Ketuk tombol <b>Masuk</b> milik Claude di bagian bawah layar (atau <b>🔑 Login ke Claude</b> di bawah), lalu pilih <b>Continue with Google</b>.</li><li>Setelah login kamu dibawa kembali ke halaman ini. Kalau malah ke beranda Claude, buka lagi link Serdik Games.</li></ol>
    <div class="mbtns" style="justify-content:center"><button class="btn" data-act="close">Nanti saja, main lawan bot</button><a class="btn pri" href="${esc(pageLink())}" target="_blank" rel="noopener" style="text-decoration:none">🔑 Login ke Claude</a></div>`);
}
