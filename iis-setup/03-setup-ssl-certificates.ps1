# PowerShell Script to Set up SSL Certificates for Local Creatio Development
# Run as Administrator in PowerShell

Import-Module WebAdministration

Write-Host "Setting up SSL Certificates for Local Creatio Development..." -ForegroundColor Green

# Function to create self-signed certificate
function New-CreatioSSLCertificate {
    param(
        [string]$DnsName = "localhost",
        [string]$FriendlyName = "Creatio Local Development",
        [int]$ValidityDays = 365
    )
    
    Write-Host "Creating self-signed certificate for $DnsName..." -ForegroundColor Blue
    
    # Create self-signed certificate
    $cert = New-SelfSignedCertificate -DnsName $DnsName -CertStoreLocation "cert:\LocalMachine\My" -FriendlyName $FriendlyName -NotAfter (Get-Date).AddDays($ValidityDays)
    
    # Export certificate to trusted root store to trust it locally
    $rootStore = Get-Item "cert:\LocalMachine\Root"
    $rootStore.Open("ReadWrite")
    $rootStore.Add($cert)
    $rootStore.Close()
    
    Write-Host "Certificate created and installed: $($cert.Thumbprint)" -ForegroundColor Green
    return $cert
}

# Function to configure SSL binding for IIS site
function Set-CreatioSSLBinding {
    param(
        [string]$SiteName,
        [string]$CertificateThumbprint,
        [int]$Port = 443,
        [string]$IPAddress = "*"
    )
    
    Write-Host "Configuring SSL binding for site: $SiteName" -ForegroundColor Blue
    
    # Remove existing SSL binding if it exists
    $existingBinding = Get-WebBinding -Name $SiteName -Protocol "https" -Port $Port -ErrorAction SilentlyContinue
    if ($existingBinding) {
        Remove-WebBinding -Name $SiteName -Protocol "https" -Port $Port
        Write-Host "Removed existing SSL binding" -ForegroundColor Yellow
    }
    
    # Add new SSL binding
    New-WebBinding -Name $SiteName -Protocol "https" -Port $Port -IPAddress $IPAddress
    
    # Associate certificate with the binding
    $binding = Get-WebBinding -Name $SiteName -Protocol "https" -Port $Port
    $binding.AddSslCertificate($CertificateThumbprint, "my")
    
    Write-Host "SSL binding configured for $SiteName on port $Port" -ForegroundColor Green
}

# Create certificates for different Creatio instances
$certs = @()

# Main localhost certificate
$localhost_cert = New-CreatioSSLCertificate -DnsName "localhost" -FriendlyName "Creatio Localhost"
$certs += $localhost_cert

# Create certificates for specific development domains
$dev_domains = @("creatio-dev.local", "creatio-test.local", "creatio-staging.local")

foreach ($domain in $dev_domains) {
    $cert = New-CreatioSSLCertificate -DnsName $domain -FriendlyName "Creatio $domain"
    $certs += $cert
    
    # Add to hosts file for local resolution
    $hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
    $hostEntry = "127.0.0.1`t$domain"
    
    # Check if entry already exists
    $hostsContent = Get-Content $hostsPath
    if ($hostsContent -notcontains $hostEntry -and $hostsContent -notlike "*$domain*") {
        Add-Content -Path $hostsPath -Value $hostEntry
        Write-Host "Added $domain to hosts file" -ForegroundColor Green
    }
}

Write-Host "`nSSL Certificates Created:" -ForegroundColor Blue
$certs | Select-Object Subject, Thumbprint, NotAfter | Format-Table -AutoSize

# Function to apply SSL settings to existing sites (call this after creating sites)
function Set-CreatioSSLSettings {
    param([string]$SiteName)
    
    # Enable SSL for the site
    Set-WebConfigurationProperty -Filter "system.web/httpCookies" -Name "requireSSL" -Value $true -PSPath "IIS:\" -Location $SiteName
    Set-WebConfigurationProperty -Filter "system.web/httpCookies" -Name "sameSite" -Value "Lax" -PSPath "IIS:\" -Location $SiteName
    
    # Configure SSL settings
    Set-WebConfiguration -Filter "system.webServer/security/access" -Value @{sslFlags="Ssl"} -PSPath "IIS:\" -Location $SiteName
    
    Write-Host "SSL settings applied to $SiteName" -ForegroundColor Green
}

Write-Host "`nSSL Certificate setup completed!" -ForegroundColor Green
Write-Host "Certificates have been installed and trusted locally." -ForegroundColor Yellow
Write-Host "Use Set-CreatioSSLBinding function to bind certificates to your IIS sites." -ForegroundColor Yellow

# Example usage (uncomment when you have sites created):
# Set-CreatioSSLBinding -SiteName "CreatioDev" -CertificateThumbprint $localhost_cert.Thumbprint
# Set-CreatioSSLSettings -SiteName "CreatioDev"
