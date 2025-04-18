# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('Message.ui', '.'), ('Plot.ui', '.'), ('resource/img.png', 'resource'), ('resource/login.jpg', 'resource'), ('resource/broom.svg', 'resource'), ('resource/reset.svg', 'resource'), ('resource/white.jpg', 'resource'), ('resource/pause.svg', 'resource'), ('resource/icon.png', 'resource'), ('Menu.ui', '.'), ('Login.ui', '.'), ('userinfo.csv', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'pandas', 'matplotlib', 'PIL.GifImagePlugin', 'scipy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resource\\icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
