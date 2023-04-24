# Set the path to the virtual environment
$venv_path = ".\env"
$src_path = ".\src"
$log_file = ".\logs\debug\log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
if (-not (Test-Path $log_file)) {
    New-Item $log_file -ItemType File | Out-Null
}

# Check if virtual environment exists
if (-not (Test-Path $venv_path)) {
    Write-Error "Virtual environment does not exist at '$venv_path'."
    Exit 1
}

# Activate virtual environment
try {
    & "$venv_path\Scripts\Activate.ps1"
}
catch {
    Write-Error "Failed to activate virtual environment. $_"
    Exit 1
}

# Start Django app
try {
    & "$venv_path\Scripts\python.exe" "$src_path\manage.py" runserver
}
catch {
    Write-Error "Failed to start Django app. $_"
    Exit 1
}

# Success message
Write-Host "Django app started successfully. Press enter to close this window."
pause
