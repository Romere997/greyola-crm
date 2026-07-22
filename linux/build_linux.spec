# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller one-file spec for the Linux Greyola CRM app.

Run from the linux/ directory:
    pyinstaller build_linux.spec --noconfirm --clean
Produces: dist/greyola-crm  (a single Linux executable)
"""

import os

app_dir = os.path.dirname(os.path.abspath(SPEC))
datas = []

# Bundle the CRM front-end (assets/crm.html must be present at build time).
html_src = os.path.join(app_dir, 'assets', 'crm.html')
if os.path.exists(html_src):
    datas.append((html_src, 'assets'))

block_cipher = None

a = Analysis(
    [os.path.join(app_dir, 'linux_launcher.py')],
    pathex=[app_dir],
    binaries=[],
    datas=datas,
    hiddenimports=['webview', 'webview.platforms.gtk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ---------------------------------------------------------------------------
# Version note (informational only on Linux; PyInstaller does not embed a
# Windows-style VERSION resource on this platform). Greyola CRM release:
# APP_VERSION = 1.1.0  (kept in sync with launcher.py / linux_launcher.py
# and CHANGELOG.md).
# ---------------------------------------------------------------------------

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='greyola-crm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
