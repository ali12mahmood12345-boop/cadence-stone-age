@echo off
title CADENCE STONE AGE V5 REPRODUCIBILITY - 5 SEEDS

if not exist ".venv-v5\Scripts\activate.bat" (
    echo.
    echo ERROR: .venv-v5 was not found in this folder.
    echo Put this BAT file inside your existing CADENCE_STONE_AGE_V5_MOCHI_STYLE folder.
    echo.
    pause
    exit /b 1
)

call .venv-v5\Scripts\activate

echo.
echo ================================================================
echo  CADENCE // STONE AGE V5 - REPRODUCIBILITY TEST
echo ================================================================
echo.
echo SAME protocol as the successful Quick run:
echo   train episodes:      120
echo   guided/autonomous:   4 / 8 decisions
echo   frozen eval:         100 episodes
echo   post-caregiver life: 80 episodes
echo   fingerprint samples: 300
echo.
echo ONLY CHANGE:
echo   seeds: 1  ^>  5
echo.
echo Seeds will be 42, 43, 44, 45, 46.
echo.
echo Do not close this window while it is running.
echo.

python v5_mochi_style.py --train 120 --eval 100 --post-life 80 --guided-span 4 --autonomous-span 8 --fingerprint-samples 300 --seeds 5 --name repro5

echo.
echo ================================================================
echo  FINISHED
echo ================================================================
echo.
echo Main report:
echo benchmark_output_v5\repro5_REPORT.txt
echo.
pause
