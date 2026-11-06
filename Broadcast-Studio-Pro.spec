# -*- mode: python ; coding: utf-8 -*-
# Build from verified Windows source; keep the one-folder layout.
from pathlib import Path

root = Path(SPECPATH)
datas = []
binaries = [
    (str(root / "tools" / "ffmpeg.exe"), "tools"),
    (str(root / "tools" / "ffprobe.exe"), "tools"),
]

# Include all supplied AI model files in the installed program.
if (root / "ai_models").is_dir():
    datas += [(str(path), str(path.parent.relative_to(root))) for path in (root / "ai_models").rglob("*") if path.is_file()]

icon_file = root / "assets" / "broadcast_studio.ico"
icon_path = str(icon_file) if icon_file.exists() else None

a = Analysis(
    [str(root / "broadcast_studio_professional.py")],
    pathex=[str(root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Broadcast-Studio-Pro",
    console=False,
    icon=icon_path,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="Broadcast-Studio-Pro",
)
