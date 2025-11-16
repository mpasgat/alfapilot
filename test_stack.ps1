#!/usr/bin/env pwsh
# Complete Stack Test Script for Alfapilot

Write-Host "`n🚀 Alfapilot Full Stack Test" -ForegroundColor Cyan
Write-Host "="*60

# Test 1: Check if Docker is running
Write-Host "`n[1/6] Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Test 2: Check if .env exists
Write-Host "`n[2/6] Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file exists" -ForegroundColor Green
    
    # Check for required variables
    $envContent = Get-Content ".env" -Raw
    $hasApiKey = $envContent -match "OPENROUTER_API_KEY=(?!<)"
    
    if ($hasApiKey) {
        Write-Host "✅ OPENROUTER_API_KEY is configured" -ForegroundColor Green
    } else {
        Write-Host "⚠️  OPENROUTER_API_KEY not set. Set DEMO_MODE=true for testing." -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env created. Please edit it with your API keys." -ForegroundColor Green
}

# Test 3: Check if services are running
Write-Host "`n[3/6] Checking running services..." -ForegroundColor Yellow
$backendRunning = $false
$frontendRunning = $false

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "✅ Backend is running on port 8000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Backend not running on port 8000" -ForegroundColor Yellow
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $frontendRunning = $true
        Write-Host "✅ Frontend is running on port 3000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Frontend not running on port 3000" -ForegroundColor Yellow
}

# Test 4: Start services if not running
if (-not $backendRunning -or -not $frontendRunning) {
    Write-Host "`n[4/6] Starting services with Docker Compose..." -ForegroundColor Yellow
    Write-Host "This may take a few minutes on first run..." -ForegroundColor Gray
    
    Start-Process docker-compose -ArgumentList "up", "--build", "-d" -NoNewWindow -Wait
    
    Write-Host "`nWaiting for services to start (30 seconds)..." -ForegroundColor Gray
    Start-Sleep -Seconds 30
    
    Write-Host "✅ Services started" -ForegroundColor Green
} else {
    Write-Host "`n[4/6] Services already running, skipping start..." -ForegroundColor Yellow
}

# Test 5: Test backend API endpoints
Write-Host "`n[5/6] Testing backend API endpoints..." -ForegroundColor Yellow

$endpoints = @(
    @{Name="Health"; Url="http://localhost:8000/health"; Method="GET"},
    @{Name="Marketing"; Url="http://localhost:8000/api/v1/marketing/generate-posts"; Method="POST"; Body='{"idea":"test","tone":"professional","target_audience":"general"}'},
    @{Name="Documents"; Url="http://localhost:8000/api/v1/documents/generate-document"; Method="POST"; Body='{"doc_type":"letter","content":"test","style":"formal"}'},
    @{Name="Legal"; Url="http://localhost:8000/api/v1/legal/analyze-contract"; Method="POST"; Body='{"contract_text":"test contract","analyze_risks":true}'},
    @{Name="Finance"; Url="http://localhost:8000/api/v1/finance/analyze-data"; Method="POST"; Body='{"data":"test data","analysis_type":"summary"}'}
)

$passedTests = 0
$totalTests = $endpoints.Count

foreach ($endpoint in $endpoints) {
    try {
        if ($endpoint.Method -eq "GET") {
            $response = Invoke-WebRequest -Uri $endpoint.Url -Method GET -TimeoutSec 10 -ErrorAction Stop
        } else {
            $response = Invoke-WebRequest -Uri $endpoint.Url -Method POST -ContentType "application/json" -Body $endpoint.Body -TimeoutSec 10 -ErrorAction Stop
        }
        
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✅ $($endpoint.Name) endpoint: OK" -ForegroundColor Green
            $passedTests++
        } else {
            Write-Host "  ⚠️  $($endpoint.Name) endpoint: Status $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ❌ $($endpoint.Name) endpoint: Failed" -ForegroundColor Red
        Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Gray
    }
}

# Test 6: Test frontend
Write-Host "`n[6/6] Testing frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Summary
Write-Host "`n" + "="*60
Write-Host "📊 Test Summary" -ForegroundColor Cyan
Write-Host "="*60
Write-Host "Backend API Tests: $passedTests/$totalTests passed" -ForegroundColor $(if ($passedTests -eq $totalTests) { "Green" } else { "Yellow" })

if ($backendRunning -or $frontendRunning) {
    Write-Host "`n🌐 Access Points:" -ForegroundColor Cyan
    Write-Host "  Frontend:    http://localhost:3000" -ForegroundColor White
    Write-Host "  Backend API: http://localhost:8000" -ForegroundColor White
    Write-Host "  API Docs:    http://localhost:8000/docs" -ForegroundColor White
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
if ($passedTests -lt $totalTests) {
    Write-Host "  1. Check docker-compose logs: docker-compose logs -f" -ForegroundColor Yellow
    Write-Host "  2. Verify .env configuration" -ForegroundColor Yellow
    Write-Host "  3. Enable DEMO_MODE=true if API keys are rate-limited" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ All systems operational!" -ForegroundColor Green
    Write-Host "  • Open frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "  • Test API: http://localhost:8000/docs" -ForegroundColor White
}

Write-Host "`n💡 Useful Commands:" -ForegroundColor Cyan
Write-Host "  View logs:     docker-compose logs -f" -ForegroundColor Gray
Write-Host "  Restart:       docker-compose restart" -ForegroundColor Gray
Write-Host "  Stop:          docker-compose down" -ForegroundColor Gray
Write-Host "  Rebuild:       docker-compose up --build" -ForegroundColor Gray

Write-Host "`n✨ Testing complete!`n" -ForegroundColor Green
