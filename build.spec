# PyInstaller spec for the Greyola CRM Windows app.
# Produces a single-file, console-less .exe that opens a native Edge WebView2 window.
import os

block_cipher = None

app_dir = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    [os.path.join(app_dir, 'launcher.py')],
    pathex=[app_dir],
    binaries=[],
    datas=[
        (os.path.join(app_dir, 'assets', 'crm.html'), 'assets'),
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.edgechromium',
        'webview.platforms.winforms',
        'webview.js',
        'webview.util',
        'webview.window',
        'webview.menu',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'webview.platforms.cocoa',
        'webview.platforms.gtk',
        'webview.platforms.qt',
        'webview.platforms.android',
        'tkinter',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'cairo', 'gi',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Greyola CRM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,          # no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(app_dir, '..', 'greyola.ico'),
)
