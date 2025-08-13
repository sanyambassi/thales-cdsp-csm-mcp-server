@echo off
REM Batch script to start Thales CSM Akeyless Vault MCP Server
REM This script sets up the environment and starts the MCP server

echo 🚀 Starting Thales CSM Akeyless Vault MCP Server...
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

python --version
echo ✅ Python found

REM Check if virtual environment exists
if exist "venv" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️  Virtual environment not found. Creating one...
    
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment created and activated
    
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
)

REM Check if .env file exists
if exist ".env" (
    echo ✅ Environment file (.env) found
) else (
    echo ⚠️  Environment file (.env) not found
    echo Please create a .env file with your Thales CSM Akeyless Vault credentials
    echo Example:
    echo   AKEYLESS_API_URL=https://api.akeyless.io
    echo   AKEYLESS_ACCESS_ID=your_access_id_here
    echo   AKEYLESS_ACCESS_KEY=your_access_key_here
)

echo.
echo 🔧 Starting MCP server...
echo Transport modes available:
echo   stdio (default): python main.py --transport stdio
echo   HTTP: python main.py --transport streamable-http --host 0.0.0.0 --port 8000
echo Press Ctrl+C to stop the server
echo.

REM Start the server with stdio transport (default)
echo 🚀 Starting server with stdio transport...
python main.py --transport stdio

if %errorlevel% neq 0 (
    echo ❌ Failed to start server
    pause
    exit /b 1
) 