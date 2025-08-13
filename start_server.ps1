# PowerShell script to start Thales CSM Akeyless Vault MCP Server
# This script sets up the environment and starts the MCP server

Write-Host "🚀 Starting Thales CSM Akeyless Vault MCP Server..." -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ and add it to PATH" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found. Creating one..." -ForegroundColor Yellow
    
    try {
        python -m venv venv
        & "venv\Scripts\Activate.ps1"
        Write-Host "✅ Virtual environment created and activated" -ForegroundColor Green
        
        Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create virtual environment: $_" -ForegroundColor Red
        exit 1
    }
}

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "✅ Environment file (.env) found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Environment file (.env) not found" -ForegroundColor Yellow
    Write-Host "Please create a .env file with your Thales CSM Akeyless Vault credentials" -ForegroundColor Yellow
    Write-Host "Example:" -ForegroundColor Cyan
    Write-Host "  AKEYLESS_API_URL=https://api.akeyless.io" -ForegroundColor White
    Write-Host "  AKEYLESS_ACCESS_ID=your_access_id_here" -ForegroundColor White
    Write-Host "  AKEYLESS_ACCESS_KEY=your_access_key_here" -ForegroundColor White
}

Write-Host ""
Write-Host "🔧 Starting MCP server..." -ForegroundColor Yellow
Write-Host "Transport modes available:" -ForegroundColor Cyan
Write-Host "  stdio (default): python main.py --transport stdio" -ForegroundColor White
Write-Host "  HTTP: python main.py --transport streamable-http --host 0.0.0.0 --port 8000" -ForegroundColor White
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

try {
    # Start the server with stdio transport (default)
    Write-Host "🚀 Starting server with stdio transport..." -ForegroundColor Green
    python main.py --transport stdio
} catch {
    Write-Host "❌ Failed to start server: $_" -ForegroundColor Red
    exit 1
} 