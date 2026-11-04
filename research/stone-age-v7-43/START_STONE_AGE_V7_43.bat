@echo off
setlocal
cd /d "%~dp0"
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY goto :fail
if exist v7_43_results goto :fail
if not exist .venv-old\Scripts\python.exe %PY% -m venv .venv-old
if errorlevel 1 goto :fail
if not exist .venv-new\Scripts\python.exe %PY% -m venv .venv-new
if errorlevel 1 goto :fail
.venv-old\Scripts\python.exe -m pip install cadence-net==0.91.1 "numpy>=2,<3"
if errorlevel 1 goto :fail
.venv-new\Scripts\python.exe -m pip install cadence-net==0.93.1 "numpy>=2,<3"
if errorlevel 1 goto :fail
.venv-old\Scripts\python.exe run_compare.py
if errorlevel 1 goto :fail
pause
exit /b 0
:fail
echo Stopped. Check Python installation, errors above, or an existing results folder.
pause
exit /b 1

