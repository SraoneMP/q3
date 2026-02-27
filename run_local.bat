@echo off
echo ================================================
echo   FastAPI Sentiment Analysis - Local Server
echo ================================================
echo.

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo.
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo Please edit .env and add your OPENAI_API_KEY
    echo Then run this script again.
    pause
    exit /b 1
)

echo Starting FastAPI server...
echo.
echo Server will be available at:
echo   http://localhost:8000
echo.
echo API Documentation:
echo   http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

uvicorn main:app --reload --port 8000
