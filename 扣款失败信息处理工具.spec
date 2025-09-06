# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['excel_processor_cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pandas', 'openpyxl', 'pypinyin'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['flask', 'werkzeug', 'jinja2', 'click', 'itsdangerous', 'markupsafe'],
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
    name='扣款失败信息处理工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
