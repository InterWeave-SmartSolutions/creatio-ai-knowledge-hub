# PowerShell Script to Create IIS Site Configurations for Creatio Instances
# Run as Administrator in PowerShell

Import-Module WebAdministration

Write-Host "Creating IIS Sites for Creatio Instances..." -ForegroundColor Green

# Function to create Creatio IIS site
function New-CreatioSite {
    param(
        [string]$SiteName,
        [string]$PhysicalPath,
        [string]$ApplicationPool,
        [int]$HttpPort = 80,
        [int]$HttpsPort = 443,
        [string]$HostHeader = "",
        [string]$CertificateThumbprint = ""
    )
    
    Write-Host "Creating IIS site: $SiteName" -ForegroundColor Blue
    
    # Ensure physical path exists
    if (!(Test-Path $PhysicalPath)) {
        New-Item -ItemType Directory -Path $PhysicalPath -Force
        Write-Host "Created directory: $PhysicalPath" -ForegroundColor Yellow
    }
    
    # Remove existing site if it exists
    if (Get-Website -Name $SiteName -ErrorAction SilentlyContinue) {
        Remove-Website -Name $SiteName
        Write-Host "Removed existing site: $SiteName" -ForegroundColor Yellow
    }
    
    # Create new website with HTTP binding
    if ($HostHeader) {
        New-Website -Name $SiteName -PhysicalPath $PhysicalPath -ApplicationPool $ApplicationPool -Port $HttpPort -HostHeader $HostHeader
    } else {
        New-Website -Name $SiteName -PhysicalPath $PhysicalPath -ApplicationPool $ApplicationPool -Port $HttpPort
    }
    
    # Add HTTPS binding if certificate is provided
    if ($CertificateThumbprint) {
        if ($HostHeader) {
            New-WebBinding -Name $SiteName -Protocol "https" -Port $HttpsPort -HostHeader $HostHeader
        } else {
            New-WebBinding -Name $SiteName -Protocol "https" -Port $HttpsPort
        }
        
        # Associate certificate with HTTPS binding
        $binding = Get-WebBinding -Name $SiteName -Protocol "https" -Port $HttpsPort
        $binding.AddSslCertificate($CertificateThumbprint, "my")
        Write-Host "HTTPS binding configured with certificate" -ForegroundColor Green
    }
    
    Write-Host "Site $SiteName created successfully!" -ForegroundColor Green
}

# Function to configure Creatio-specific settings for a site
function Set-CreatioSiteSettings {
    param([string]$SiteName)
    
    Write-Host "Configuring Creatio-specific settings for $SiteName..." -ForegroundColor Blue
    
    # Set default document
    Set-WebConfigurationProperty -Filter "system.webServer/defaultDocument/files" -Name "Collection" -Value @{value="Default.aspx"} -PSPath "IIS:\" -Location $SiteName
    
    # Configure request limits for large file uploads
    Set-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering/requestLimits" -Name "maxAllowedContentLength" -Value 104857600 -PSPath "IIS:\" -Location $SiteName  # 100MB
    Set-WebConfigurationProperty -Filter "system.web/httpRuntime" -Name "maxRequestLength" -Value 102400 -PSPath "IIS:\" -Location $SiteName  # 100MB in KB
    Set-WebConfigurationProperty -Filter "system.web/httpRuntime" -Name "executionTimeout" -Value 3600 -PSPath "IIS:\" -Location $SiteName  # 1 hour
    
    # Configure compilation settings
    Set-WebConfigurationProperty -Filter "system.web/compilation" -Name "debug" -Value $true -PSPath "IIS:\" -Location $SiteName
    Set-WebConfigurationProperty -Filter "system.web/compilation" -Name "targetFramework" -Value "4.8" -PSPath "IIS:\" -Location $SiteName
    
    # Configure session state
    Set-WebConfigurationProperty -Filter "system.web/sessionState" -Name "timeout" -Value 60 -PSPath "IIS:\" -Location $SiteName  # 60 minutes
    
    # Configure custom errors for development
    Set-WebConfigurationProperty -Filter "system.web/customErrors" -Name "mode" -Value "Off" -PSPath "IIS:\" -Location $SiteName
    
    # Enable detailed errors
    Set-WebConfigurationProperty -Filter "system.webServer/httpErrors" -Name "errorMode" -Value "Detailed" -PSPath "IIS:\" -Location $SiteName
    
    # Configure static content caching
    Set-WebConfigurationProperty -Filter "system.webServer/staticContent" -Name "clientCache" -Value @{cacheControlMode="UseMaxAge"; cacheControlMaxAge="7.00:00:00"} -PSPath "IIS:\" -Location $SiteName
    
    Write-Host "Creatio-specific settings configured for $SiteName" -ForegroundColor Green
}

# Define site configurations
$siteConfigs = @(
    @{
        Name = "CreatioDev"
        Path = "C:\inetpub\wwwroot\CreatioDev"
        Pool = "CreatioDevPool"
        HttpPort = 8080
        HttpsPort = 8443
        HostHeader = "creatio-dev.local"
    },
    @{
        Name = "CreatioTest"
        Path = "C:\inetpub\wwwroot\CreatioTest"
        Pool = "CreatioTestPool"
        HttpPort = 8081
        HttpsPort = 8444
        HostHeader = "creatio-test.local"
    },
    @{
        Name = "CreatioStaging"
        Path = "C:\inetpub\wwwroot\CreatioStaging"
        Pool = "CreatioStagingPool"
        HttpPort = 8082
        HttpsPort = 8445
        HostHeader = "creatio-staging.local"
    }
)

# Create sites
foreach ($config in $siteConfigs) {
    # Create the site
    New-CreatioSite -SiteName $config.Name -PhysicalPath $config.Path -ApplicationPool $config.Pool -HttpPort $config.HttpPort -HttpsPort $config.HttpsPort -HostHeader $config.HostHeader
    
    # Configure Creatio-specific settings
    Set-CreatioSiteSettings -SiteName $config.Name
    
    # Create a simple placeholder index file
    $indexContent = @"
<!DOCTYPE html>
<html>
<head>
    <title>$($config.Name) - Creatio Instance</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: #0066cc; color: white; padding: 20px; border-radius: 5px; }
        .content { padding: 20px; border: 1px solid #ddd; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>$($config.Name)</h1>
            <p>Creatio Development Instance</p>
        </div>
        <div class="content">
            <h2>Site Information</h2>
            <ul>
                <li><strong>Site Name:</strong> $($config.Name)</li>
                <li><strong>Application Pool:</strong> $($config.Pool)</li>
                <li><strong>HTTP Port:</strong> $($config.HttpPort)</li>
                <li><strong>HTTPS Port:</strong> $($config.HttpsPort)</li>
                <li><strong>Host Header:</strong> $($config.HostHeader)</li>
                <li><strong>Physical Path:</strong> $($config.Path)</li>
            </ul>
            <p><em>This is a placeholder page. Deploy your Creatio application to this directory.</em></p>
        </div>
    </div>
</body>
</html>
"@
    
    $indexPath = Join-Path $config.Path "index.html"
    $indexContent | Out-File -FilePath $indexPath -Encoding UTF8
    Write-Host "Created placeholder index.html for $($config.Name)" -ForegroundColor Green
}

Write-Host "`nAll Creatio IIS sites created successfully!" -ForegroundColor Green

# Display created sites
Write-Host "`nCreated Sites:" -ForegroundColor Blue
Get-Website | Where-Object {$_.Name -like "*Creatio*"} | Select-Object Name, State, PhysicalPath, @{Name="Bindings";Expression={($_.Bindings.Collection | ForEach-Object {$_.protocol + "://" + $_.bindingInformation}) -join ", "}} | Format-Table -AutoSize

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Deploy your Creatio application files to the respective directories" -ForegroundColor White
Write-Host "2. Configure database connections in web.config files" -ForegroundColor White
Write-Host "3. Set up SSL certificates using the 03-setup-ssl-certificates.ps1 script" -ForegroundColor White
Write-Host "4. Configure permissions using the 05-configure-permissions.ps1 script" -ForegroundColor White
