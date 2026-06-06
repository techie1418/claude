@echo off
REM One-click launcher for Windows. Double-click this file.
REM It starts the Off-Page SEO tool, then open http://localhost:8000 in your browser.
cd /d "%~dp0\.."
echo Starting Off-Page SEO tool...
echo Open this in your browser:  http://localhost:8000
echo (Keep this window open while you use the tool. Close it to stop.)
python web\server.py || python3 web\server.py
pause
