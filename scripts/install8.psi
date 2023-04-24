# Set the path for the new PST file
$pst_path = "$(Get-Location)\outlook_backup.pst"

# Check if Outlook is installed
try {
    $outlook = New-Object -ComObject Outlook.Application
}
catch {
    Write-Error "Outlook is not installed."
    Exit 1
}

# Create a new PST file
try {
    New-PSTDataFile -Path $pst_path -DisplayName "Outlook Backup" #-Password (ConvertTo-SecureString -String "MyPassword" -AsPlainText -Force)
    Write-Host "New PST file created successfully: $pst_path"
}
catch {
    Write-Error "Failed to create PST file: $_"
    Exit 1
}

# Import new PST file
try {
    $namespace = $outlook.GetNameSpace("MAPI")
    $pst = $namespace.AddStoreEx($pst_path, 3)
    $pst.DisplayName = "New PST"
}
catch {
    Write-Error "Failed to import new PST file. $_"
    Exit 1
}

# # Output PST file path to file
# try {
#     $pstPath | Out-File -FilePath ".\pst_path.txt" -Encoding ascii
#     Write-Host "PST file path: $pstPath"
#     Write-Host "PST file path saved to 'pst_path.txt'"
# }
# catch {
#     Write-Error "Failed to save PST file path. $_"
#     Exit 1
# }

# Success message
Write-Host "Installation completed successfully. Press enter to close this window."
pause