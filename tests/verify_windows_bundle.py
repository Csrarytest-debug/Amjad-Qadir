"""Static packaging gate; not a replacement for GUI or real-video QC."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
app = root / "dist" / "Broadcast-Studio-Pro"
exe = app / "Broadcast-Studio-Pro.exe"
checks = {"Standalone launcher": exe.is_file(), "One-folder payload": (app / "_internal").is_dir()}
for tool in ("ffmpeg.exe", "ffprobe.exe"):
    checks[f"Bundled {tool}"] = any(p.name.lower() == tool.lower() and "tools" in p.parts for p in app.rglob(tool))
checks["Bundled AI model files"] = any(p.suffix.lower() in (".onnx", ".pth", ".pt", ".safetensors", ".param", ".bin") and "ai_models" in p.parts for p in app.rglob("*") if p.is_file())
for name, passed in checks.items():
    print(("[PASS] " if passed else "[FAIL] ") + name)
if not all(checks.values()):
    print("Build incomplete. Do NOT distribute as offline standalone.")
    sys.exit(1)
print("Static bundle check passed; test installation, GPU inference, playback, lip-sync, export and offline operation on a separate Windows PC.")
