# Enable Required Windows Features for Creatio
# Run this script as Administrator

param(
    [switch]$WhatIf = $false
)

Write-Host "🚀 Enabling Windows Features for Creatio Development" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "This script must be run as Administrator. Exiting..."
    exit 1
}

# Define required Windows features
$requiredFeatures = @(
    # IIS Core Features
    "IIS-WebServerRole",
    "IIS-WebServer",
    "IIS-CommonHttpFeatures",
    "IIS-HttpErrors",
    "IIS-HttpLogging",
    "IIS-HttpRedirect",
    "IIS-ApplicationDevelopment",
    "IIS-NetFxExtensibility45",
    "IIS-HealthAndDiagnostics",
    "IIS-HttpLogging",
    "IIS-Security",
    "IIS-RequestFiltering",
    "IIS-Performance",
    "IIS-WebServerManagementTools",
    "IIS-ManagementConsole",
    "IIS-IIS6ManagementCompatibility",
    "IIS-Metabase",
    
    # ASP.NET Support
    "IIS-ASPNET45",
    "IIS-NetFxExtensibility45",
    "IIS-ISAPIExtensions",
    "IIS-ISAPIFilter",
    
    # WebSocket Protocol (Critical for Creatio)
    "IIS-WebSockets",
    
    # .NET Framework Features
    "NetFx3",
    "WCF-HTTP-Activation",
    "WCF-HTTP-Activation45",
    
    # Windows Communication Foundation
    "NetFx4Extended-ASPNET45",
    "WCF-Services45",
    "WCF-HTTP-Activation45",
    "WCF-TCP-Activation45",
    "WCF-Pipe-Activation45",
    "WCF-MSMQ-Activation45"
)

Write-Host "Checking current feature status..." -ForegroundColor Yellow

# Check current status of features
$featureStatus = @{}
foreach ($feature in $requiredFeatures) {
    try {
        $status = Get-WindowsOptionalFeature -Online -FeatureName $feature -ErrorAction SilentlyContinue
        if ($status) {
            $featureStatus[$feature] = $status.State
            $statusColor = if ($status.State -eq "Enabled") { "Green" } else { "Red" }
            Write-Host "  $feature : $($status.State)" -ForegroundColor $statusColor
        } else {
            $featureStatus[$feature] = "NotFound"
            Write-Host "  $feature : Not Found" -ForegroundColor Magenta
        }
    } catch {
        $featureStatus[$feature] = "Error"
        Write-Host "  $feature : Error checking status" -ForegroundColor Red
    }
}

if ($WhatIf) {
    Write-Host "`n🔍 What-If Mode: The following features would be enabled:" -ForegroundColor Cyan
    $featuresToEnable = $requiredFeatures | Where-Object { $featureStatus[$_] -ne "Enabled" -and $featureStatus[$_] -ne "NotFound" }
    foreach ($feature in $featuresToEnable) {
        Write-Host "  - $feature" -ForegroundColor Yellow
    }
    Write-Host "`nRun without -WhatIf to actually enable features" -ForegroundColor Cyan
    exit 0
}

Write-Host "`n🔧 Enabling required features..." -ForegroundColor Yellow

$enabledCount = 0
$errorCount = 0
$skippedCount = 0

foreach ($feature in $requiredFeatures) {
    if ($featureStatus[$feature] -eq "Enabled") {
        Write-Host "  ✓ $feature (already enabled)" -ForegroundColor Green
        $skippedCount++
        continue
    }
    
    if ($featureStatus[$feature] -eq "NotFound") {
        Write-Host "  ⚠ $feature (not found - may not be available on this Windows edition)" -ForegroundColor Yellow
        $skippedCount++
        continue
    }
    
    try {
        Write-Host "  🔄 Enabling $feature..." -ForegroundColor Cyan
        Enable-WindowsOptionalFeature -Online -FeatureName $feature -All -NoRestart | Out-Null
        Write-Host "  ✅ $feature enabled successfully" -ForegroundColor Green
        $enabledCount++
    } catch {
        Write-Host "  ❌ Failed to enable $feature : $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host "`n📊 Summary:" -ForegroundColor Cyan
Write-Host "  Features enabled: $enabledCount" -ForegroundColor Green
Write-Host "  Features skipped: $skippedCount" -ForegroundColor Yellow
Write-Host "  Errors: $errorCount" -ForegroundColor $(if ($errorCount -gt 0) { "Red" } else { "Green" })

if ($enabledCount -gt 0) {
    Write-Host "`n⚠️  IMPORTANT: Some features require a system restart to take effect." -ForegroundColor Yellow
    Write-Host "   Please restart your computer before proceeding with Creatio installation." -ForegroundColor Yellow
    
    $restart = Read-Host "`nWould you like to restart now? (y/N)"
    if ($restart -match "^[Yy]") {
        Write-Host "Restarting system in 10 seconds..." -ForegroundColor Red
        Start-Sleep -Seconds 10
        Restart-Computer -Force
    }
}

Write-Host "`n✅ Windows features configuration completed!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Install Microsoft SQL Server Developer Edition" -ForegroundColor White
Write-Host "2. Install Redis for Windows" -ForegroundColor White
Write-Host "3. Download and install .NET 6 SDK and .NET Framework 4.8 SDK" -ForegroundColor White
Write-Host "4. Configure IIS with Creatio application" -ForegroundColor White
