@echo off
echo Activating Thales CDSP CSM MCP Server Virtual Environment...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run 'uv venv' first to create the environment.
    pause
    exit /b 1
)

REM Activate the virtual environment
call .venv\Scripts\activate.bat

echo.
echo Virtual environment activated!
echo.
echo Available commands:
echo   python tests\test_server.py          - Run test suite
echo   python tests\example_transport_modes.py - Demo transport modes
echo   python main.py --help - Show server options
echo.
echo To start the server:
echo   python main.py                    - stdio mode
echo   python main.py --transport streamable-http - HTTP mode
echo.
echo To deactivate, type: deactivate
echo. 