@echo off
setlocal
cd /d "%~dp0"
echo CADENCE STONE AGE V7.48 - Fresh paired founder confirmation
py -3 -m pip install -r requirements.txt
if errorlevel 1 goto :fail
py -3 run.py --smoke
if errorlevel 1 goto :fail
py -3 run.py --resume
if errorlevel 1 goto :fail
echo V7.48 runner finished. Upload the complete v7_48_results folder.
pause
exit /b 0
:fail
echo V7.48 halted or failed. Inspect the console and saved result files.
pause
exit /b 1
