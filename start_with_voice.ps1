# PowerShell script to start Voice-Enabled AI Automation Assistant
# Starts both AI Brain and Automation Engine

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Voice-Enabled AI Automation Assistant" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will start both components:" -ForegroundColor Yellow
Write-Host "1. AI Brain (with voice input support)" -ForegroundColor Yellow
Write-Host "2. Automation Engine (executes workflows)" -ForegroundColor Yellow
Write-Host ""

# Set UTF-8 encoding for this session
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Check if GEMINI_API_KEY is set
if (-not $env:GEMINI_API_KEY) {
    Write-Host "WARNING: GEMINI_API_KEY is not set!" -ForegroundColor Red
    Write-Host "Please set it first:" -ForegroundColor Yellow
    Write-Host '   $env:GEMINI_API_KEY="your_api_key_here"' -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit
    }
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Starting Automation Engine in new window..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; `$env:PYTHONIOENCODING='utf-8'; python -m automation_engine.main"

Write-Host "Waiting 3 seconds for engine to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting AI Brain with Voice Input..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Voice Commands:" -ForegroundColor Yellow
Write-Host "  - Type 'voice' to enable voice mode" -ForegroundColor White
Write-Host "  - Say 'text mode' to switch back" -ForegroundColor White
Write-Host "  - Type 'test mic' to test microphone" -ForegroundColor White
Write-Host "  - Type 'help' for more info" -ForegroundColor White
Write-Host ""

# Start AI Brain in current window
python -m ai_brain.main

Write-Host ""
Write-Host "AI Brain stopped. Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
