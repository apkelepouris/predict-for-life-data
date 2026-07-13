@echo off
setlocal

REM 1) Go to the Historic Data folder
cd /d "C:\Users\apkel\OneDrive\Desktop\Predict For Life\Predict For Life App\Historic Data"

echo ============================
echo Updating Predict For Life data
echo ============================
echo.

REM 2) Rebuild JSON (script decides whether version changes)
py build_json.py
if errorlevel 1 (
    echo Python script failed. Fix the CSV or script and try again.
    pause
    exit /b 1
)

echo.
echo Checking if anything changed in CSV/JSON...
echo.

REM 3) If there is no diff for these files, stop here
git diff --quiet -- set_for_life.csv set_for_life_history.json
if %errorlevel%==0 (
    echo No changes to commit. GitHub already has the same data.
    echo.
    goto :done
)

echo Changes detected. Staging files...
git add set_for_life.csv set_for_life_history.json

echo.
echo Committing...
git commit -m "Update draws %date% %time%"

echo.
echo Pushing to GitHub...
git push origin main

:done
echo.
echo Done. GitHub now has the latest data (if there were any changes).
echo.

pause
endlocal
