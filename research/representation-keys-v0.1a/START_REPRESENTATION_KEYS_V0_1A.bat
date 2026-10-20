@echo off
setlocal
pushd "%~dp0"

echo ========================================================================================================================
echo  CADENCE REPRESENTATION KEYS V0.1A - LEARNED COMPACT KEY PROOF-OF-PRINCIPLE
echo ========================================================================================================================
echo Cadence: 0.84.3
echo Fresh development seeds: 45001-45024
echo.
echo Tests whether a task-trained 12-neuron association state is a better memory key for nuisance-variable observations.
echo Development proof-of-principle only; no Cadence core-memory modification.
echo.

set "PYEXE="
where python >nul 2>nul
if %errorlevel%==0 set "PYEXE=python"
if not defined PYEXE (
  where py >nul 2>nul
  if %errorlevel%==0 set "PYEXE=py -3"
)
if not defined PYEXE (
  echo ERROR: Python 3 was not found in PATH.
  goto :fail
)

if not exist ".venv-representation-v01a\Scripts\python.exe" (
  echo First run: creating environment...
  %PYEXE% -m venv .venv-representation-v01a || goto :fail
  call .venv-representation-v01a\Scripts\activate.bat || goto :fail
  python -m pip install --upgrade pip || goto :fail
  python -m pip install -r requirements.txt || goto :fail
) else (
  call .venv-representation-v01a\Scripts\activate.bat || goto :fail
)

python -c "import importlib.metadata as m; print('cadence-net:',m.version('cadence-net'))" || goto :fail
python smoke_test_v0_1a.py || goto :fail

echo.
echo Running Representation Keys V0.1A...
python representation_keys_v0_1a.py --output representation_keys_v0_1a_output || goto :fail

echo.
echo ========================================================================================================================
echo  REPRESENTATION KEYS V0.1A FINISHED
echo ========================================================================================================================
echo.
echo Send ChatGPT these first:
echo   representation_keys_v0_1a_output\REPRESENTATION_KEYS_V0_1A_REPORT.txt
echo   representation_keys_v0_1a_output\REPRESENTATION_KEYS_V0_1A_RESULTS.json
echo   representation_keys_v0_1a_output\REPRESENTATION_KEYS_V0_1A_SUMMARY.csv
echo.
pause
popd
exit /b 0

:fail
echo.
echo ERROR: Representation Keys V0.1A stopped because a command failed.
pause
popd
exit /b 1
