@echo on
setlocal enableextensions
REM Always run from the script's folder
cd /d "%~dp0"

set "VENV=.venv"
set "PYEXE=%CD%\%VENV%\Scripts\python.exe"

REM --- Create venv if missing ---
if not exist "%PYEXE%" (
  echo === Creating Python venv ===
  set "PYCMD="
  where py >nul 2>&1 && set "PYCMD=py -3.11"
  if not defined PYCMD where python >nul 2>&1 && set "PYCMD=python"
  if not defined PYCMD (
    echo.
    echo *** ERROR: Python 3.11+ not found on PATH.
    echo     Install from https://www.python.org/downloads/windows/ and check "Add Python to PATH".
    goto :fail
  )
  %PYCMD% -m venv "%VENV%" || goto :fail
)

echo Using Python: "%PYEXE%"

REM --- Ensure pip and core build tools ---
"%PYEXE%" -m ensurepip --upgrade || goto :fail
"%PYEXE%" -m pip install --upgrade pip setuptools wheel || goto :fail

REM --- Install your package and deps ---
echo === Installing package (editable) ===
"%PYEXE%" -m pip install -e . || goto :fail

echo === Installing data/ML deps ===
"%PYEXE%" -m pip install datasets huggingface_hub opencv-python matplotlib pillow scikit-learn pandas jupyter || goto :fail

REM --- Fetch real data (MURA mirror) ---
echo === Fetching real X-rays (MURA) ===
"%PYEXE%" -m datasetqa.fetch_bones --source mura --out-dir ".\examples\bones_real" --max 60 || goto :fail

REM --- Reviewer UI (optional; can close these if you just want exports) ---
echo === Review: broken ===
"%PYEXE%" -m datasetqa.review --image-dir ".\examples\bones_real\broken_bone" --type BB --overwrite || goto :fail

echo === Review: non-broken ===
"%PYEXE%" -m datasetqa.review --image-dir ".\examples\bones_real\non_broken" --type NB --overwrite || goto :fail

REM --- Export labeled CSVs ---
echo === Export CSVs ===
"%PYEXE%" -m datasetqa.export --image-dir ".\examples\bones_real\broken_bone" --type BB --out bones_real_bb.csv || goto :fail
"%PYEXE%" -m datasetqa.export --image-dir ".\examples\bones_real\non_broken" --type NB --out bones_real_nb.csv || goto :fail

echo.
echo SUCCESS ✅  CSVs written to: %CD%
echo Open notebooks\\bones_baseline.ipynb in VS Code and "Run All" for metrics & visuals.
pause
exit /b 0

:fail
echo.
echo *** ERROR: A command failed. Scroll up for details. This window is paused so you can read the error. ***
pause
exit /b 1
