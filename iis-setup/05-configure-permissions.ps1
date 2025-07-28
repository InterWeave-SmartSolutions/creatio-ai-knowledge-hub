# PowerShell Script to Configure Permissions and Authentication for Creatio Sites
# Run as Administrator in PowerShell

Import-Module WebAdministration

Write-Host "Configuring Permissions and Authentication for Creatio Sites..." -ForegroundColor Green

# Function to set file system permissions
function Set-CreatioDirectoryPermissions {
    param(
        [string]$Path,
        [string]$SiteName
    )
    
    Write-Host "Setting file system permissions for $Path..." -ForegroundColor Blue
    
    # Get application pool identity
    $appPoolIdentity = "IIS AppPool\$((Get-WebApplication -Site $SiteName).ApplicationPool)"
    
    # Set permissions for IIS_IUSRS (read and execute)
    $acl = Get-Acl $Path
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS_IUSRS", "ReadAndExecute", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($accessRule)
    
    # Set permissions for application pool identity (modify)
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($appPoolIdentity, "Modify", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($accessRule)
    
    # Set permissions for NETWORK SERVICE (read and execute)
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("NETWORK SERVICE", "ReadAndExecute", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($accessRule)
    
    # Apply the ACL
    Set-Acl -Path $Path -AclObject $acl
    
    # Set specific permissions for temp and log directories
    $tempDirs = @("App_Data", "Temp", "Logs", "Files")
    foreach ($tempDir in $tempDirs) {
        $tempPath = Join-Path $Path $tempDir
        if (!(Test-Path $tempPath)) {
            New-Item -ItemType Directory -Path $tempPath -Force | Out-Null
        }
        
        $tempAcl = Get-Acl $tempPath
        $tempAccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($appPoolIdentity, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
        $tempAcl.SetAccessRule($tempAccessRule)
        
        $tempAccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS_IUSRS", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
        $tempAcl.SetAccessRule($tempAccessRule)
        
        Set-Acl -Path $tempPath -AclObject $tempAcl
        Write-Host "Set full control permissions for $tempPath" -ForegroundColor Green
    }
    
    Write-Host "File system permissions configured for $Path" -ForegroundColor Green
}

# Function to configure authentication settings
function Set-CreatioAuthentication {
    param([string]$SiteName)
    
    Write-Host "Configuring authentication for $SiteName..." -ForegroundColor Blue
    
    # Enable Anonymous Authentication
    Set-WebConfigurationProperty -Filter "system.webServer/security/authentication/anonymousAuthentication" -Name "enabled" -Value $true -PSPath "IIS:\" -Location $SiteName
    
    # Disable Windows Authentication for public access (enable if needed for intranet)
    Set-WebConfigurationProperty -Filter "system.webServer/security/authentication/windowsAuthentication" -Name "enabled" -Value $false -PSPath "IIS:\" -Location $SiteName
    
    # Disable Basic Authentication
    Set-WebConfigurationProperty -Filter "system.webServer/security/authentication/basicAuthentication" -Name "enabled" -Value $false -PSPath "IIS:\" -Location $SiteName
    
    # Configure Forms Authentication (Creatio handles this internally)
    Set-WebConfigurationProperty -Filter "system.web/authentication" -Name "mode" -Value "Forms" -PSPath "IIS:\" -Location $SiteName
    
    Write-Host "Authentication configured for $SiteName" -ForegroundColor Green
}

# Function to configure security headers
function Set-CreatioSecurityHeaders {
    param([string]$SiteName)
    
    Write-Host "Configuring security headers for $SiteName..." -ForegroundColor Blue
    
    # Add security headers
    $headers = @{
        "X-Content-Type-Options" = "nosniff"
        "X-Frame-Options" = "SAMEORIGIN"
        "X-XSS-Protection" = "1; mode=block"
        "Referrer-Policy" = "strict-origin-when-cross-origin"
    }
    
    foreach ($header in $headers.GetEnumerator()) {
        # Remove existing header if it exists
        Remove-WebConfigurationProperty -Filter "system.webServer/httpProtocol/customHeaders" -Name "." -AtElement @{name=$header.Key} -PSPath "IIS:\" -Location $SiteName -ErrorAction SilentlyContinue
        
        # Add new header
        Add-WebConfigurationProperty -Filter "system.webServer/httpProtocol/customHeaders" -Name "." -Value @{name=$header.Key; value=$header.Value} -PSPath "IIS:\" -Location $SiteName
    }
    
    Write-Host "Security headers configured for $SiteName" -ForegroundColor Green
}

# Function to configure request filtering
function Set-CreatioRequestFiltering {
    param([string]$SiteName)
    
    Write-Host "Configuring request filtering for $SiteName..." -ForegroundColor Blue
    
    # Configure file extension restrictions
    $allowedExtensions = @(".aspx", ".asmx", ".ashx", ".svc", ".axd", ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot", ".xml", ".json", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip")
    
    # Allow double escaping for Creatio
    Set-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering" -Name "allowDoubleEscaping" -Value $true -PSPath "IIS:\" -Location $SiteName
    
    # Allow high bit characters
    Set-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering" -Name "allowHighBitCharacters" -Value $true -PSPath "IIS:\" -Location $SiteName
    
    # Configure verb filtering (allow common HTTP methods)
    $allowedVerbs = @("GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS")
    Clear-WebConfiguration -Filter "system.webServer/security/requestFiltering/verbs" -PSPath "IIS:\" -Location $SiteName
    
    foreach ($verb in $allowedVerbs) {
        Add-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering/verbs" -Name "." -Value @{verb=$verb; allowed=$true} -PSPath "IIS:\" -Location $SiteName
    }
    
    Write-Host "Request filtering configured for $SiteName" -ForegroundColor Green
}

# Function to configure MIME types for Creatio
function Set-CreatioMimeTypes {
    param([string]$SiteName)
    
    Write-Host "Configuring MIME types for $SiteName..." -ForegroundColor Blue
    
    # Add MIME types for modern web fonts and files
    $mimeTypes = @{
        ".woff" = "font/woff"
        ".woff2" = "font/woff2"
        ".ttf" = "font/ttf"
        ".eot" = "application/vnd.ms-fontobject"
        ".svg" = "image/svg+xml"
        ".json" = "application/json"
        ".map" = "application/json"
    }
    
    foreach ($mimeType in $mimeTypes.GetEnumerator()) {
        # Remove existing MIME type if it exists
        Remove-WebConfigurationProperty -Filter "system.webServer/staticContent" -Name "." -AtElement @{fileExtension=$mimeType.Key} -PSPath "IIS:\" -Location $SiteName -ErrorAction SilentlyContinue
        
        # Add new MIME type
        Add-WebConfigurationProperty -Filter "system.webServer/staticContent" -Name "." -Value @{fileExtension=$mimeType.Key; mimeType=$mimeType.Value} -PSPath "IIS:\" -Location $SiteName
    }
    
    Write-Host "MIME types configured for $SiteName" -ForegroundColor Green
}

# Main configuration function
function Set-CreatioSitePermissions {
    param(
        [string]$SiteName,
        [string]$PhysicalPath
    )
    
    Write-Host "Configuring all permissions for $SiteName..." -ForegroundColor Yellow
    
    # Set file system permissions
    Set-CreatioDirectoryPermissions -Path $PhysicalPath -SiteName $SiteName
    
    # Configure authentication
    Set-CreatioAuthentication -SiteName $SiteName
    
    # Configure security headers
    Set-CreatioSecurityHeaders -SiteName $SiteName
    
    # Configure request filtering
    Set-CreatioRequestFiltering -SiteName $SiteName
    
    # Configure MIME types
    Set-CreatioMimeTypes -SiteName $SiteName
    
    Write-Host "All permissions and settings configured for $SiteName" -ForegroundColor Green
}

# Get all Creatio sites and configure them
$creatioSites = Get-Website | Where-Object {$_.Name -like "*Creatio*"}

if ($creatioSites.Count -eq 0) {
    Write-Host "No Creatio sites found. Please run 04-create-iis-sites.ps1 first." -ForegroundColor Red
    exit 1
}

foreach ($site in $creatioSites) {
    Set-CreatioSitePermissions -SiteName $site.Name -PhysicalPath $site.PhysicalPath
}

# Additional security configurations
Write-Host "`nApplying additional security configurations..." -ForegroundColor Blue

# Disable server header for security
Set-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering" -Name "removeServerHeader" -Value $true -PSPath "IIS:\"

# Configure machine-wide settings for ASP.NET
$machineConfigPath = "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\Config\machine.config"
if (Test-Path $machineConfigPath) {
    Write-Host "Machine.config found - consider reviewing trust levels and compilation settings" -ForegroundColor Yellow
}

Write-Host "`nPermissions and Authentication Configuration Complete!" -ForegroundColor Green

# Display summary
Write-Host "`nSummary of configured sites:" -ForegroundColor Blue
foreach ($site in $creatioSites) {
    Write-Host "Site: $($site.Name)" -ForegroundColor White
    Write-Host "  Path: $($site.PhysicalPath)" -ForegroundColor Gray
    Write-Host "  Authentication: Anonymous enabled, Forms authentication configured" -ForegroundColor Gray
    Write-Host "  Permissions: Application pool identity has Modify access" -ForegroundColor Gray
    Write-Host "  Security: Headers and request filtering configured" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Deploy Creatio application files to the configured directories" -ForegroundColor White
Write-Host "2. Update web.config files with database connection strings" -ForegroundColor White
Write-Host "3. Test site accessibility and authentication" -ForegroundColor White
Write-Host "4. Configure SSL certificates if not already done" -ForegroundColor White
