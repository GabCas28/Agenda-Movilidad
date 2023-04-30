# Initialize log file
$venvPath = ".\env"
$scriptPath = ".\src"
$log_directory = ".\logs\install"
$logFile = "$log_directory\install_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"


if (-not (Test-Path $log_directory -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $log_directory
}

if (-not (Test-Path $logFile)) {
    New-Item $logFile -ItemType File | Out-Null
}

# Log function
function Log($message) {
    $logEntry = "$(Get-Date -Format G) - $message"
    Write-Output $logEntry | Out-File -FilePath $logFile -Append
    Write-Host $message
}

# Check if Python is installed
if (-not (Get-Command python.exe -ErrorAction SilentlyContinue)) {
    Log "Python is not installed. Installing Python..."
    Write-Host "Python is not installed. Installing Python..."
    # Download Python installer
    $pythonUrl = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
    $pythonInstaller = "python-3.10.0-amd64.exe"
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    # Install Python
    try {
        & .\python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
        Log "Python installed successfully."
        Write-Host "Python installed successfully."
    } catch {
        $errorMessage = $_.Exception.Message
        Log "Failed to install Python: $errorMessage"
        Write-Error "Failed to install Python: $errorMessage"
    }
    # Remove installer
    Remove-Item $pythonInstaller
} else {
    Log "Python is already installed."
    Write-Host "Python is already installed."
}

# Check if pip is installed
if (-not (Get-Command pip.exe -ErrorAction SilentlyContinue)) {
    Log "Pip is not installed. Installing Pip..."
    Write-Host "Pip is not installed. Installing Pip..."
    # Download get-pip.py
    $getPipUrl = "https://bootstrap.pypa.io/get-pip.py"
    Invoke-WebRequest -Uri $getPipUrl -OutFile "get-pip.py"
    # Install pip
    try {
        & python.exe .\get-pip.py
        Log "Pip installed successfully."
    } catch {
        $errorMessage = $_.Exception.Message
        Log "Failed to install Pip: $errorMessage"
    }
    # Remove get-pip.py
    Remove-Item "get-pip.py"
} else {
    Log "Pip is already installed."
}


# Check if SQLite is installed
try {
    if (-not (Get-Command sqlite3.exe -ErrorAction SilentlyContinue)) {
        Log "SQLite is not installed. Installing SQLite..."
        # Download SQLite binaries
        $sqliteUrl = "https://www.sqlite.org/2022/sqlite-tools-win32-x86-3571650.zip"
        $sqliteZip = "sqlite-tools-win32-x86-3571650.zip"
        Invoke-WebRequest -Uri $sqliteUrl -OutFile $sqliteZip
        # Extract SQLite binaries
        Expand-Archive -Path $sqliteZip -DestinationPath .
        # Move SQLite binaries to system32
        Move-Item .\sqlite-tools-win32-x86-3571650\sqlite3.exe "$env:SystemRoot\System32\"
        # Remove extracted files and zip
        Remove-Item -Recurse .\sqlite-tools-win32-x86-3571650
        Remove-Item $sqliteZip
        Log "SQLite installed successfully."
    } else {
        Log "SQLite is already installed."
    }
} catch {
    Log "Error: $_"
}



# Create and activate virtual environment
if (-not (Test-Path $venvPath)) {
    try {
        & "python.exe" -m venv $venvPath
    }
    catch {
        Log "Failed to create virtual environment. $_"
        Write-Host "Press enter to close this window."
        pause
        Exit 1
    }
} else {
    Log "Virtual environment already exists, lets activate it. $_"
}

try {
    & "$($venvPath)\Scripts\Activate.ps1"
}
catch {
    Log "Failed to activate virtual environment. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

try {
    if (Test-Path ".\src\requirements.txt") {
        Log "Installing project requirements..."
        & "$venvPath\Scripts\pip.exe" install -r "$scriptPath\requirements.txt"
        Log "Project requirements installed successfully."
    } else {
        Log "requirements.txt file not found. Skipping project requirements installation."
    }
} catch {
    Log "Error: $_"
}

# Check if Outlook is installed
try {
    Log "Checking if Outlook is installed"
    $outlook = New-Object -ComObject Outlook.Application
}
catch {
    Log "Outlook is not installed. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Get PST file path


try {
    Log "Looking for PST file..."
    $namespace = $outlook.GetNameSpace("MAPI")
    $pst_path = $namespace.stores | ?{$_.ExchangeStoreType -eq 0} | select -First 1 | %{$_.FilePath}
    Log "PST file path: $pst_path"
    $env:MAIN_PST_PATH = $pst_path
    Log "PST file path saved in MAIN_PST_PATH config variable"
}
catch {
    Log "Failed to get PST file path. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Make migrations
try {
    Log "Creating app migrations..."
    & "$venvPath\Scripts\python.exe" "$scriptPath\manage.py" makemigrations 2>&1 | Out-File -FilePath $logFile -Append
    Log "Migrations created."
}
catch {
    Log "Failed to make migrations. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Run migrations
try {
    Log "Running app migrations..."
    & "$venvPath\Scripts\python.exe" "$scriptPath\manage.py" migrate 2>&1 | Out-File -FilePath $logFile -Append
    Log "Migrations completed."
}
catch {
    Log "Failed to run migrations. $_"
    Write-Host "Press enter to close this window."
    pause
    Exit 1
}

# Create superuser

# Prompt the user for the necessary information to create a superuser
if(($superuser_username = Read-Host "Introduce un nombre de usuario. Este nombre se utilizará para iniciar sesión. Por defecto 'admin'") -eq ''){$superuser_username ="admin"}

# Ask for username and check if it already exists
do {
    if($username_taken -eq 'True'){if(($superuser_username = Read-Host "El nombre de usuario introducido ya existe. Por favor, prueba con otro distinto. (Por defecto 'admin')") -eq ''){$superuser_username ="admin"}}
    $username_taken = & "$venvPath\Scripts\python.exe" "$scriptPath\manage.py" shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='$superuser_username').exists())"
} while ($username_taken -eq 'True')

# Ask for password
if(($superuser_password = Read-Host "Enter una contraseñe. Default 'MySecurePassword123'") -eq ''){$superuser_password = "MySecurePassword123"}

# dont ask for email
$superuser_email = "admin@admin.com"

try {
    # Execute the python command to create the superuser
    & "$venvPath\Scripts\python.exe" "$scriptPath\manage.py" createsuperuser --noinput --username $superuser_username  --email $superuser_email

    #  Execute the python command to retrieve the superuser and update their password
    & "$venvPath\Scripts\python.exe" "$scriptPath\manage.py" shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='$superuser_username'); user.set_password('$superuser_password'); user.save()"
}
catch {
    Log "Failed to create superuser. $_"
    Exit 1
}

# Success message
Write-Host "Installation completed successfully. Press enter to close this window."
pause