@echo off
cd /d "%~dp0"
echo Starting Alfapilot Backend Server...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python app\main.py
pause
