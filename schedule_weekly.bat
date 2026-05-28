@echo off
REM Weekly Article Pipeline Scheduler
REM Run this script to schedule the weekly article generation

echo ==========================================
echo The Longevity Journal - Weekly Scheduler
echo ==========================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Please run as Administrator
    echo Right-click - Run as administrator
    pause
    exit /b 1
)

REM Define schedule - Every Thursday at 9:00 AM
set TASK_NAME="LongevityJournal-WeeklyArticle"
set PYTHON_PATH=uv
set SCRIPT_PATH=C:\Openclaw\agents\longevity-journal\weekly_pipeline.py

REM Remove existing task if present
schtasks /delete /tn %TASK_NAME% /f >nul 2>&1

REM Create weekly task (Thursday at 9:00 AM)
schtasks /create ^
    /tn %TASK_NAME% ^
    /tr "%PYTHON_PATH% run python %SCRIPT_PATH% --live" ^
    /sc weekly ^
    /d THU ^
    /st 09:00 ^
    /ru SYSTEM ^
    /rl HIGHEST ^
    /desc "Generate and publish weekly longevity article" ^
    /f

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Weekly task scheduled.
    echo Schedule: Every Thursday at 9:00 AM
    echo.
    echo To verify:
    echo   schtasks /query /tn %TASK_NAME%
    echo.
    echo To test run now:
    echo   cd C:\Openclaw\agents\longevity-journal
    echo   uv run python weekly_pipeline.py --test
) else (
    echo.
    echo ERROR: Failed to create scheduled task
    echo Try running manually:
    echo   uv run python %SCRIPT_PATH% --test
)

echo.
pause
