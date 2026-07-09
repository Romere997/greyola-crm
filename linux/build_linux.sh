#!/usr/bin/env bash
# Build the Linux Greyola CRM one-file executable.
# Run from the linux/ directory:  bash build_linux.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="$(dirname "$HERE")"
SRC_HTML="$APP_ROOT/Greyola CRM.html"
DEST_HTML="$HERE/assets/crm.html"

echo "==> Syncing CRM front-end into assets/ ..."
mkdir -p "$HERE/assets"
cp "$SRC_HTML" "$DEST_HTML"

echo "==> Installing Python deps (pywebview, PyInstaller) ..."
pip install -r "$HERE/requirements.txt"

echo "==> Building with PyInstaller ..."
pyinstaller "$HERE/build_linux.spec" --noconfirm --clean

echo "==> Done. Executable at: $HERE/dist/greyola-crm"
