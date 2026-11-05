@echo off
setlocal
cd /d "%~dp0"
echo V7.47 - EXACT 0.10 / NATIVE 0.10 / NATIVE 0.20
py -3 -m pip install -r requirements.txt
if errorlevel 1 goto :fail
py -3 run.py --smoke
if errorlevel 1 goto :fail
py -3 run.py --resume
if errorlevel 1 goto :fail
echo V7.47 run ended. Check v7_47_resultsV7_47_RESULTS.json
pause
exit /b 0
:fail
echo V7.47 halted. No failed arm is counted valid.
pause
exit /b 1
