# PowerShell script to activate AKeyless MCP Server Virtual Environment

Write-Host "Activating Thales CDSP CSM MCP Server Virtual Environment..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run 'uv venv' first to create the environment." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate the virtual environment
& .venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  python tests\test_server.py          - Run test suite" -ForegroundColor Yellow
Write-Host "  python tests\example_transport_modes.py - Demo transport modes" -ForegroundColor Yellow
Write-Host "  python main.py --help - Show server options" -ForegroundColor Yellow
Write-Host ""
Write-Host "To start the server:" -ForegroundColor Cyan
Write-Host "  python main.py                    - stdio mode" -ForegroundColor Yellow
Write-Host "  python main.py --transport streamable-http - HTTP mode" -ForegroundColor Yellow
Write-Host ""
Write-Host "To deactivate, type: deactivate" -ForegroundColor Cyan
Write-Host "" 