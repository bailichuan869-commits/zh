@echo off
setlocal
set "ROOT=%~dp0"
cd /d "%ROOT%"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [ERROR] Python not found: %PY%
  echo Create the virtual environment and install dependencies first.
  pause
  exit /b 1
)
"%PY%" "%ROOT%tools\start_kb_web.py"
if errorlevel 1 pause
