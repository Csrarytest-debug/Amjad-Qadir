@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo.
echo ===== Broadcast-Studio Pro V05.0 CLEAN Windows Installer Build =====
echo.

if not exist "broadcast_studio_professional.py" (
  echo [BLOCKED] Missing broadcast_studio_professional.py in this build folder.
  echo Copy the verified application source here. No experimental patch files are required.
  exit /b 10
)
if not exist "requirements-app.txt" (
  echo [BLOCKED] Missing requirements-app.txt from the working application.
  echo Do not guess dependency versions. Export/pin dependencies from the known-good build.
  exit /b 11
)
if not exist "tools\ffmpeg.exe" (
  echo [BLOCKED] Missing tools\ffmpeg.exe
  exit /b 12
)
if not exist "tools\ffprobe.exe" (
  echo [BLOCKED] Missing tools\ffprobe.exe
  exit /b 13
)
if not exist "ai_models" (
  echo [BLOCKED] Missing ai_models directory. Offline AI cannot be called portable without its models.
  exit /b 14
)

if not exist ".venv_build\Scripts\python.exe" (
  py -3.11 -m venv .venv_build
  if errorlevel 1 (
    echo [ERROR] Python 3.11 is required to create this isolated build environment.
    exit /b 15
  )
)
set "PYTHON=.venv_build\Scripts\python.exe"
"%PYTHON%" -m pip install --upgrade pip
if errorlevel 1 exit /b 20
"%PYTHON%" -m pip install -r requirements-build.txt
if errorlevel 1 exit /b 21
"%PYTHON%" -m pip install -r requirements-app.txt
if errorlevel 1 exit /b 22
"%PYTHON%" -m pip check
if errorlevel 1 exit /b 23

"%PYTHON%" -m PyInstaller --noconfirm --clean "Broadcast-Studio-Pro.spec"
if errorlevel 1 exit /b 30
"%PYTHON%" "tests\verify_windows_bundle.py"
if errorlevel 1 exit /b 31

set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC (
  echo [BLOCKED] Inno Setup 6 not found. EXE folder is in dist\Broadcast-Studio-Pro.
  exit /b 40
)
"%ISCC%" "Broadcast-Studio-Pro-Setup.iss"
if errorlevel 1 exit /b 41
if not exist "Installer\Broadcast-Studio-Pro-V05.0-Setup.exe" exit /b 42

echo.
echo [BUILT] Installer\Broadcast-Studio-Pro-V05.0-Setup.exe
echo [IMPORTANT] Run a fresh-PC offline test before approving release.
endlocal
exit /b 0
