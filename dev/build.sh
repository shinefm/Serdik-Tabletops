#!/bin/bash
# Bangun ulang situs: dev/base.html + patch hub/*.py  ->  index.html di root repo
set -e
cd "$(dirname "$0")"
cp base.html saudagar-permata.html
for p in patch patch_pm patch_wk patch_brand patch_gate patch_restart patch_resil patch_afk patch_turn patch_nav patch_jy patch_hub2 patch_sp2 patch_host patch_host2 patch_sandi patch_kota patch_misc patch_chat; do
  python3 hub/$p.py >/dev/null
done
python3 hub/patch_fb.py
