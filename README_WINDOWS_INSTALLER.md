# Broadcast-Studio Pro V05.0 — Clean Windows Installer Pipeline

**Purpose:** An isolated Windows build pipeline, *not* a compiled installer and *not* the full application source. This repository previously contained no application code. This pipeline is intentionally on its own branch to avoid changing the experimental working tree.

## Required input files from the verified application
Place these next to BUILD_WINDOWS.bat:
- broadcast_studio_professional.py (the verified current application entry point)
- requirements-app.txt (pinned app dependencies from the verified source/environment)
- any Python modules imported by that entry point, including ai_backend.py if used
- tools/ffmpeg.exe and tools/ffprobe.exe
- ai_models/ containing the required offline model weights; adapt packaging for any additional AI assets
- optionally assets/broadcast_studio.ico

Do not copy temporary build directories, old dist/build folders, unrelated v6 patches, existing virtual environments, or customer media. Keep the approved application layout and exclude all BS Broadcast branding.

## Build
On Windows 10/11 x64 with Python 3.11 available as \`py -3.11\` and Inno Setup 6 installed, open a command prompt in the extracted directory and run:

    BUILD_WINDOWS.bat

The script creates an isolated \`.venv_build\`, installs pinned app requirements, packages a one-folder EXE using PyInstaller, checks key runtime assets and invokes Inno Setup.

**Expected result after a successful build:**
\`Installer/ Broadcast-Studio-Pro-V05.0-Setup.exe\` (without the space after slash)

The EXE is *not* a single-file standalone program: it requires the adjacent \`_internal\` folder. The Setup EXE carries the complete onedir distribution.

## Release gates — mandatory
1. Confirm the dark navy/royal gold/electric blue approved interface with **no BS Broadcast logo**.
2. Verify input/output monitors, independently controlled source loading and 16:9 Safe Fit.
3. Test smooth synchronous playback and exported lip-sync with real clips and both audio streams.
4. Verify actual Real-ESRGAN output visible in Output Monitor, GPU execution and bundled models without internet.
5. Confirm MP4 output, Stop & Save and full output path display.
6. Install Setup EXE on a **clean compatible Windows computer** with no Python.
7. Run offline and verify bundled FFmpeg, required model files and AI processing.
8. Check external licensing and package size before distribution.

The static gate catches missing files but **cannot certify lip-sync, offline models, external DLLs, CUDA/Vulkan dependencies, UI quality or clean-PC portability**. Do not say the installer is final until those tests pass.

## GitHub
This branch is solely the build-pipeline delivery. The application source is not currently committed in \`Csrarytest-debug/Amjad-Qadir\`. A GitHub Actions Windows build should be added only after the verified source and exact requirements are available. Do not merge placeholder files from \`Csrarytest-debug-patch-1\` as if they were app code.
