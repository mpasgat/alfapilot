#!/usr/bin/env pwsh
# Test Runner Script for Alfapilot Backend

Write-Host "🧪 Alfapilot Backend Test Runner" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if backend is running
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "✅ Backend is already running on http://localhost:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Backend is not running. Please start it first:" -ForegroundColor Yellow
    Write-Host "   cd backend" -ForegroundColor Gray
    Write-Host "   python app\main.py" -ForegroundColor Gray
    Write-Host ""
}

if ($backendRunning) {
    Write-Host ""
    Write-Host "🚀 Running API tests..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location -Path "backend"
    python test_api.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=" * 50
        Write-Host "✅ All tests passed successfully!" -ForegroundColor Green
        Write-Host "=" * 50
    } else {
        Write-Host ""
        Write-Host "=" * 50
        Write-Host "❌ Some tests failed. Check the output above." -ForegroundColor Red
        Write-Host "=" * 50
    }
} else {
    Write-Host ""
    Write-Host "📝 To start the backend:" -ForegroundColor Yellow
    Write-Host "   1. Open a new terminal" -ForegroundColor Gray
    Write-Host "   2. cd backend" -ForegroundColor Gray
    Write-Host "   3. python app\main.py" -ForegroundColor Gray
    Write-Host "   4. Wait for 'Uvicorn running on...' message" -ForegroundColor Gray
    Write-Host "   5. Run this script again" -ForegroundColor Gray
}
