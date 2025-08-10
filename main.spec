# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=[('app/Data/*', 'Data/'), ('app/Fantome/Ressources/Images/*', 'Fantome/Ressources/Images/'), ('app/Flappy_Bird/Ressources/*', 'Flappy_Bird/Ressources/'), ('app/Minesweeper/Images/*', 'Minesweeper/Images/'), ('app/Parametters/*', 'Parametters/'), ('app/Pendu/ressources/*', 'Pendu/ressources/'), ('app/Pong/res/*', 'Pong/res/'), ('app/Snake/images/*', 'Snake/images/'), ('app/Tete_chercheuse/image/*', 'Tete_chercheuse/image/'), ('app/Tetris/Images/*', 'Tetris/Images/'), ('app/thumbnail/*', 'thumbnail/')],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
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
