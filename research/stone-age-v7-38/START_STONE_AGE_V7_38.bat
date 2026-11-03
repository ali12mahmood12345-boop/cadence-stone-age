@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY goto :fail
if exist v7_38_results (
 echo Existing results found. Rename that folder before a fresh run.
 goto :fail
)
if not exist .venv-v738\Scripts\python.exe %PY% -m venv .venv-v738
if errorlevel 1 goto :fail
set "VPY=.venv-v738\Scripts\python.exe"
"%VPY%" -m pip install -r requirements.txt
if errorlevel 1 goto :fail
"%VPY%" -u run.py --smoke
if errorlevel 1 goto :fail
"%VPY%" -u run.py
if errorlevel 1 goto :fail
echo Finished. Send back v7_38_results\V7_38_RESULTS.json.
pause
exit /b 0
:fail
echo Stopped. Python 3.12 or newer is required. Save any error above.
pause
exit /b 1

