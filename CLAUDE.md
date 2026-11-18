# Serdik Tabletop

Hub game papan online untuk teman-teman P3MDI SBM ITB: Saudagar Permata (mirip Splendor), Jualan Yuk (simulasi bisnis tim, terinspirasi Selling Race), Pemukim Nusantara, Rapat Rahasia Direksi, Werewolf, Sandi Syndicate (mirip Codenames). Pemilik: farhan. Bahasa antarmuka dan komunikasi: Bahasa Indonesia.

Situs: https://serdik-tabletops.vercel.app. Vercel otomatis deploy setiap ada push ke `main`.

## Struktur repo

- Root (`index.html`, `shim.js`, `firebase-config.js`, `fb/`, `tutorial-*`) = **hasil build** yang ditayangkan Vercel. Jangan edit `index.html` langsung; ubah sumbernya di `dev/` lalu build.
- `dev/base.html` = file dasar Saudagar Permata (sebelum hub).
- `dev/hub/*.py` = patch berurutan yang mengubah `base.html` jadi hub lengkap. `dev/hub/*.js` = mesin dan UI tiap game yang disisipkan patch:
  - `patch.py` (hub, Rapat, Werewolf), `patch_pm.py` (Pemukim), `patch_wk.py` (Werewolf Klasik), `patch_brand.py`, `patch_gate.py`, `patch_restart.py`, `patch_resil.py` (koneksi, lobi, hapus meja), `patch_afk.py` (lapor AFK + autopilot), `patch_turn.py` (notifikasi giliran), `patch_nav.py` (tombol back), `patch_jy.py` (Jualan Yuk: `jualan.js` mesin, `jy_ui.js` UI), `patch_hub2.py` (nama Serdik Tabletop, game unggulan, tema terang), `patch_sp2.py` (istilah tukar token, pengingat waktu 1 menit/30 detik), `patch_host.py` (menu ⚙️ Atur meja untuk tuan rumah: jeda, lewati giliran, ganti pemain dengan bot, pindahkan tuan rumah; Saudagar Permata & Pemukim), `patch_host2.py` (menu yang sama untuk Jualan Yuk — ganti bot per tim lewat `T.auto` —, Rapat Rahasia, Werewolf Satu Malam & Klasik — pemain `auto` tidak ditunggu; kalau yang tersisa hanya pemain otomatis, tahap diselesaikan dengan `{type:'timeout'}`), `patch_sandi.py` + `sandi_ui.js` (Sandi Syndicate: ruang tunggu tim & ketua, pilihan paket kata per MK, papan 5×5, petunjuk & tebakan, arti istilah, layar akhir; mesinnya `sandiAct` di `engines.js`), `patch_kota.py` + `kota.js` (Saudagar Permata mode Ekspansi Kota, `st.mode==='kota'`: pahlawan diganti 3 kartu kota dari 10 kota Indonesia; kota direbut otomatis di akhir giliran saat syarat poin + kartu bonus terpenuhi; kota pertama memicu ronde terakhir; hanya pemilik kota yang bisa menang. Simulasi bot: `dev/test_fb/kotasim.py`).
  - `patch_fb.py` (terakhir) = edisi Firebase: ganti `window.claude` dengan `dev/fbapp/shim.js`, lalu tulis ke root repo.
  - Patch memakai `rep(a,b)` yang wajib ketemu tepat sekali. Kalau satu patch mengubah teks, cek patch sesudahnya yang mungkin mencari teks lama.
- `dev/fbapp/` = shim Firebase, config publik, `firestore.rules`, `database.rules.json`.
- `dev/test/` (edisi Claude, mock `mock.js`) dan `dev/test_fb/` (edisi Firebase, mock `mockfb.js`) = tes Playwright.

## Alur kerja

```bash
bash dev/build.sh                 # bangun ulang root/index.html dkk
bash dev/fbapp/mktest.sh          # salinan tes dengan SDK palsu -> dev/fbapp/test_out
cd dev/test_fb && python3 smoke.py && python3 jy.py && python3 jyon.py
```

Tes memakai path absolut `/home/claude/serdik-tabletops/dev/...` dan Chrome di `/usr/bin/google-chrome`. Kalau repo di-clone ke tempat lain, ganti path itu dulu. Tambahkan nomor `BUILD_TAG` (di `patch_fb.py`, sekarang `fb-7`) setiap rilis supaya versi terlihat di baris akun lobi.

Setelah build dan tes lolos: commit, lalu push ke `main`. Kalau perubahannya besar, pakai branch dulu supaya Vercel membuat preview.

## Firebase (project `serdik-games`, paket gratis Spark)

- Login Google; Firestore untuk meja (`games/`), ringkasan lobi (`lobby/`), hasil, statistik, profil (`users/`); Realtime Database hanya untuk presence.
- Satu langkah game kira-kira 1 tulis dan 2 baca. Batas gratis 50 rb baca dan 20 rb tulis per hari, jadi jaga supaya listener dan tulisan tetap hemat.
- Pemilik (admin) dikenali dari `meta/owners.uids` di Firestore, bukan dari email.
- Aturan keamanan ada di `dev/fbapp/*.rules*`. Kalau diubah, farhan harus menempelkannya manual di Firebase console.
- Hanya config publik yang boleh ada di repo. Jangan pernah commit service account atau private key.

## Ide yang belum dikerjakan (Jualan Yuk)

Kartu kejadian tiap ronde, momen buka rencana dramatis, riset pasar (intip demand), interaksi antar tim (jual stok / perang harga), kekuatan khusus per divisi, biaya simpan gudang.
