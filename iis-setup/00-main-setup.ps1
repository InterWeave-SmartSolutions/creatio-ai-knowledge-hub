# Main IIS Setup Script for Creatio Development Environment
# Run as Administrator in PowerShell
# This script orchestrates all the setup steps

param(
    [switch]$SkipFeatures,
    [switch]$SkipAppPools,
    [switch]$SkipSSL,
    [switch]$SkipSites,
    [switch]$SkipPermissions,
    [switch]$RunAll
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Creatio IIS Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Function to run a script with error handling
function Invoke-SetupScript {
    param(
        [string]$ScriptPath,
        [string]$Description
    )
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  $Description" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
    try {
        if (Test-Path $ScriptPath) {
            & $ScriptPath
            Write-Host "✓ $Description completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "✗ Script not found: $ScriptPath" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ Error in $Description`: $($_.Exception.Message)" -ForegroundColor Red
        $global:hasErrors = $true
    }
}

# Initialize error tracking
$global:hasErrors = $false

Write-Host "Starting Creatio IIS Setup Process..." -ForegroundColor Yellow
Write-Host "This will configure IIS for local Creatio development." -ForegroundColor White
Write-Host ""

# Step 1: Enable IIS Features
if (-not $SkipFeatures) {
    Invoke-SetupScript -ScriptPath (Join-Path $scriptDir "01-enable-iis-features.ps1") -Description "Enabling IIS Features"
} else {
    Write-Host "Skipping IIS Features setup..." -ForegroundColor Yellow
}

# Step 2: Configure Application Pools
if (-not $SkipAppPools) {
    Invoke-SetupScript -ScriptPath (Join-Path $scriptDir "02-configure-application-pools.ps1") -Description "Configuring Application Pools"
} else {
    Write-Host "Skipping Application Pools setup..." -ForegroundColor Yellow
}

# Step 3: Create IIS Sites
if (-not $SkipSites) {
    Invoke-SetupScript -ScriptPath (Join-Path $scriptDir "04-create-iis-sites.ps1") -Description "Creating IIS Sites"
} else {
    Write-Host "Skipping IIS Sites creation..." -ForegroundColor Yellow
}

# Step 4: Configure Permissions and Authentication
if (-not $SkipPermissions) {
    Invoke-SetupScript -ScriptPath (Join-Path $scriptDir "05-configure-permissions.ps1") -Description "Configuring Permissions and Authentication"
} else {
    Write-Host "Skipping Permissions configuration..." -ForegroundColor Yellow
}

# Step 5: Setup SSL Certificates (optional, as it requires additional confirmation)
if (-not $SkipSSL) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  SSL Certificate Setup" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
    $sslChoice = Read-Host "Do you want to set up SSL certificates for local development? (y/n)"
    if ($sslChoice -eq 'y' -or $sslChoice -eq 'Y') {
        Invoke-SetupScript -ScriptPath (Join-Path $scriptDir "03-setup-ssl-certificates.ps1") -Description "Setting up SSL Certificates"
    } else {
        Write-Host "SSL setup skipped. You can run 03-setup-ssl-certificates.ps1 manually later." -ForegroundColor Yellow
    }
} else {
    Write-Host "Skipping SSL setup..." -ForegroundColor Yellow
}

# Final summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($global:hasErrors) {
    Write-Host "⚠️  Setup completed with some errors. Please review the output above." -ForegroundColor Yellow
} else {
    Write-Host "✅ All setup steps completed successfully!" -ForegroundColor Green
}

Write-Host "`nCreated Creatio Development Environment:" -ForegroundColor White
Write-Host "• Development Site: http://creatio-dev.local:8080" -ForegroundColor Gray
Write-Host "• Test Site: http://creatio-test.local:8081" -ForegroundColor Gray
Write-Host "• Staging Site: http://creatio-staging.local:8082" -ForegroundColor Gray

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Deploy your Creatio application files to:" -ForegroundColor White
Write-Host "   • C:\inetpub\wwwroot\CreatioDev" -ForegroundColor Gray
Write-Host "   • C:\inetpub\wwwroot\CreatioTest" -ForegroundColor Gray
Write-Host "   • C:\inetpub\wwwroot\CreatioStaging" -ForegroundColor Gray
Write-Host "2. Configure database connections in web.config files" -ForegroundColor White
Write-Host "3. Test the sites by visiting the URLs above" -ForegroundColor White
Write-Host "4. If you need SSL, run 03-setup-ssl-certificates.ps1" -ForegroundColor White

Write-Host "`nFor troubleshooting, check:" -ForegroundColor Yellow
Write-Host "• IIS Manager (inetmgr.exe)" -ForegroundColor Gray
Write-Host "• Event Viewer > Windows Logs > Application" -ForegroundColor Gray
Write-Host "• Application pool identities and permissions" -ForegroundColor Gray

Write-Host "`nPress any key to exit..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
