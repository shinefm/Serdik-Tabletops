#!/bin/bash
# Salinan situs untuk tes lokal: SDK Firebase diganti mock (test/mockfb.js)
set -e
cd "$(dirname "$0")/.."
rm -rf fbapp/test_out && mkdir -p fbapp/test_out
OUT=$PWD/fbapp/test_out python3 hub/patch_fb.py >/dev/null
cp ../fb/* fbapp/test_out/fb/ 2>/dev/null || true
cp test/mockfb.js fbapp/test_out/fb/firebase-app-compat.js
for f in auth firestore database; do echo "" > fbapp/test_out/fb/firebase-$f-compat.js; done
for f in ../tutorial-*; do ln -sf "$(realpath $f)" fbapp/test_out/; done
echo "test_out siap"
