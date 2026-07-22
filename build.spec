# PyInstaller spec for the Greyola CRM Windows app.
# Produces a single-file, console-less .exe that opens a native Edge WebView2 window.
import os

from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable,
    StringStruct, VarFileInfo, VarStruct,
)

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

# ---------------------------------------------------------------------------
# Version resource for the built executable (Greyola CRM v1.1.0).
# PyInstaller 6.x expects a VSVersionInfo object (or a path to a version-info
# text file); a bare string is treated as a file path and would break the
# build, so we construct the resource in-line.
version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 1, 0, 0),
        prodvers=(1, 1, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
    ),
    kids=[
        StringFileInfo(
            [StringTable(
                '040904B0',
                [StringStruct('CompanyName', 'Greyola'),
                 StringStruct('FileDescription', 'Greyola CRM'),
                 StringStruct('FileVersion', '1.1.0.0'),
                 StringStruct('InternalName', 'Greyola CRM'),
                 StringStruct('LegalCopyright', 'Copyright (c) 2026 Greyola'),
                 StringStruct('OriginalFilename', 'Greyola CRM.exe'),
                 StringStruct('ProductName', 'Greyola CRM'),
                 StringStruct('ProductVersion', '1.1.0.0')])]
        ),
        VarFileInfo([VarStruct('Translation', [1033, 1200])]),
    ],
)

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
    icon=os.path.join(app_dir, 'greyola.ico'),
    version=version_info,
)
