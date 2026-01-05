@echo off
REM Check if URL argument is provided
if "%~1"=="" (
    echo Usage: run_crawler.bat ^<URL^>
    exit /b 1
)

REM Run the crawler using the virtual environment python
"%~dp0venv\Scripts\python.exe" "%~dp0crawler.py" %*
