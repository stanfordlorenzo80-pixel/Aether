# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['aether\\server.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['aether.providers.ollama', 'aether.providers.claude', 'aether.providers.openrouter', 'aether.memory.vector_store', 'aether.swarm.node', 'uvicorn', 'pydantic_settings'],
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
    name='engine-x86_64-pc-windows-msvc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
