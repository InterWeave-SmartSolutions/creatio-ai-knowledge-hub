# PowerShell Script to Enable IIS Features for Creatio
# Run as Administrator in PowerShell

Write-Host "Enabling IIS Features for Creatio..." -ForegroundColor Green

# Enable IIS Core Features
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpRedirect -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationDevelopment -All

# Enable ASP.NET Features
Enable-WindowsOptionalFeature -Online -FeatureName IIS-NetFxExtensibility45 -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-NetFxExtensibility48 -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ASPNET45 -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ASPNET48 -All

# Enable .NET Framework Features
Enable-WindowsOptionalFeature -Online -FeatureName NetFx4Extended-ASPNET45 -All
Enable-WindowsOptionalFeature -Online -FeatureName NetFx4-AdvSrvs -All

# Enable IIS Management Console
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ManagementConsole -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-IIS6ManagementCompatibility -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Metabase -All

# Enable Additional Features for Creatio
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DefaultDocument -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DirectoryBrowsing -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-StaticContent -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestFiltering -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Security -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WindowsAuthentication -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestMonitor -All

# Enable WebDAV (if needed for Creatio file operations)
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebDAV -All

Write-Host "IIS Features enabled successfully!" -ForegroundColor Green
Write-Host "You may need to restart your computer for all changes to take effect." -ForegroundColor Yellow

# Verify installation
Write-Host "Verifying IIS installation..." -ForegroundColor Blue
Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -like "IIS-*" -and $_.State -eq "Enabled"} | Select-Object FeatureName, State
