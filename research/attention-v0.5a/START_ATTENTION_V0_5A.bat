@echo off
setlocal
pushd "%~dp0"

echo ========================================================================================================================
echo  CADENCE ATTENTION V0.5A - CONJUNCTIVE MULTI-FACT MEMORY
echo ========================================================================================================================
echo Cadence: 0.88.0
echo Fresh development founders: 59001-59008
echo 2-head vs 1-head supported Recall attention
echo Conjunctive rule: either relevant fact alone is exactly chance
echo.

set "PYEXE="
where python >nul 2>nul
if %errorlevel%==0 set "PYEXE=python"
if not defined PYEXE (
  where py >nul 2>nul
  if %errorlevel%==0 set "PYEXE=py -3"
)
if not defined PYEXE goto :fail

if not exist ".venv-attention-v05a\Scripts\python.exe" (
  %PYEXE% -m venv .venv-attention-v05a || goto :fail
  call .venv-attention-v05a\Scripts\activate.bat || goto :fail
  python -m pip install --upgrade pip || goto :fail
  python -m pip install -r requirements.txt || goto :fail
) else (
  call .venv-attention-v05a\Scripts\activate.bat || goto :fail
)

python -c "import importlib.metadata as m; print('cadence-net:',m.version('cadence-net'))" || goto :fail
python smoke_test_v0_5a.py || goto :fail

echo.
echo Running V0.5A...
echo NOTE: qualified 0.88 multi-head teaching is compute-heavy; the development block is 8 founders.
python attention_v0_5a.py --output attention_v0_5a_output
set RC=%errorlevel%

echo.
echo ========================================================================================================================
echo  ATTENTION V0.5A FINISHED
echo ========================================================================================================================
echo.
echo Send ChatGPT:
echo   attention_v0_5a_output\ATTENTION_V0_5A_REPORT.txt
echo   attention_v0_5a_output\ATTENTION_V0_5A_RESULTS.json
echo   attention_v0_5a_output\ATTENTION_V0_5A_SUMMARY.csv
echo   attention_v0_5a_output\ATTENTION_V0_5A_PER_SEED.csv
echo.
pause
popd
exit /b %RC%

:fail
echo ERROR: V0.5A setup or smoke test failed.
pause
popd
exit /b 1
