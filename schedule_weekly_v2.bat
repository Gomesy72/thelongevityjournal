@echo off
:: Schedule The Longevity Journal weekly pipeline
:: Run this file as Administrator

echo ==========================================
echo THE LONGEVITY JOURNAL - Weekly Scheduler
echo ==========================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Please run this batch file as Administrator!
    echo Right-click - Run as Administrator
    pause
    exit /b 1
)

set TASK_NAME=LongevityJournal-Weekly-Pipeline
set SCRIPT_PATH=C:\Openclaw\agents\longevity-journal\weekly_pipeline_v2.py
set PYTHON_PATH=uv

:: Remove existing task if it exists
schtasks /delete /tn "%TASK_NAME%" /f > nul 2>&1

echo Creating scheduled task for Thursday 9:00 AM...

:: Create the task - Weekly on Thursday at 9:00 AM
schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "cmd /c cd /d C:\Openclaw\agents\longevity-journal && %PYTHON_PATH% run python %SCRIPT_PATH%" ^
    /sc weekly ^
    /d THU ^
    /st 09:00 ^
    /ru SYSTEM ^
    /rl HIGHEST ^
    /f

if %errorLevel% equ 0 (
    echo.
    echo SUCCESS! Task created.
    echo.
    echo Schedule Details:
    echo   - Day: Every Thursday
    echo   - Time: 9:00 AM
    echo   - Action: Generate article + Deploy + Send newsletter
    echo.
    echo To verify: schtasks /query /tn "%TASK_NAME%"
    echo To run now: schtasks /run /tn "%TASK_NAME%"
    echo To remove: schtasks /delete /tn "%TASK_NAME%" /f
) else (
    echo.
    echo ERROR: Failed to create task!
    echo Try running manually: %PYTHON_PATH% run python %SCRIPT_PATH%
)

echo.
pause
