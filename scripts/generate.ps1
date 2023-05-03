$scripts_directory = ".\"
$output_directory = "..\"
$log_directory = "..\logs\generate"
$log_file = "$log_directory\log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

# Create log directory if it doesnt exist
if (-not (Test-Path $log_directory -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $log_directory
}

# Create log file if it doesnt exist
if (-not (Test-Path $log_file)) {
    New-Item $log_file -ItemType File | Out-Null
}

# Log function
function Log($message) {
    $logEntry = "$(Get-Date -Format G) - $message"
    Write-Output $logEntry | Out-File -FilePath $log_file -Append
    Write-Host $message
}

# Install ps2exe module if not already installed
if (-not (Get-Module -Name ps2exe -ListAvailable)) {
    try {
        Install-Module -Name ps2exe -Scope CurrentUser -Force 2>&1 | Out-File -FilePath $log_file -Append
    } 
    catch {
        Log "Failed to install ps2exe module."
        Exit 1
    }
}

# Generate the EXE file for generate.psi
try {
    Invoke-ps2exe -InputFile $scripts_directory\generator.ps1 -OutputFile .\generate.exe -Version "1.0.0.0" -Verbose  2>&1 | Out-File -FilePath $log_file -Append
    Log "EXE file generated successfully: ./generate.exe"
}
catch {
    Log "Failed to generate EXE file for generate.ps1. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Generate the EXE file for install.psi
try {
    Invoke-ps2exe -InputFile $scripts_directory\installer.ps1 -OutputFile $output_directory\install.exe -Version "1.0.0.0" -Verbose  2>&1 | Out-File -FilePath $log_file -Append
    Log "EXE file generated successfully: ./install.exe"
}
catch {
    Log "Failed to generate EXE file for install.ps1. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Generate the EXE file for debug.psi
try {
    Invoke-ps2exe -InputFile $scripts_directory\debugger.ps1 -OutputFile $output_directory\debug.exe -Version "1.0.0.0" -Verbose 2>&1 | Out-File -FilePath $log_file -Append
    Log "EXE file generated successfully: ./debug.exe"
}
catch {
    Log "Failed to generate EXE file for debug.ps1. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Generate the EXE file for run.psi
try {
    Invoke-ps2exe -InputFile $scripts_directory\runner.ps1 -OutputFile $output_directory\run.exe -Version "1.0.0.0" -Verbose 2>&1 | Out-File -FilePath $log_file -Append
    Log "EXE file generated successfully: ./run.exe"
}
catch {
    Log "Failed to generate EXE file for run.ps1. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Success message
Write-Host "Generation completed successfully. Press enter to close this window."
pause