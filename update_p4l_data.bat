@echo off
setlocal

REM 1) Go to the Historic Data folder
cd /d "C:\Users\apkel\OneDrive\Desktop\Predict For Life\Predict For Life App\Historic Data"

echo ============================
echo Updating Predict For Life data
echo ============================
echo.

REM 2) Rebuild JSON (also bumps VERSION automatically)
py build_json.py
if errorlevel 1 (
    echo Python script failed. Fix the CSV or script and try again.
    pause
    exit /b 1
)

echo.
echo JSON rebuilt successfully.
echo.

REM 3) Stage changed files
git add set_for_life.csv set_for_life_history.json

REM 4) Commit (if there is anything to commit)
git commit -m "Update draws %date% %time%" || (
    echo Nothing new to commit.
)

echo.
echo Pushing to GitHub...
echo.

REM 5) Push to GitHub
git push origin main

echo.
echo Done. GitHub now has the latest data.
echo.

pause
endlocal
