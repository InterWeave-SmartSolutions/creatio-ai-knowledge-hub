# IIS Setup for Creatio Development Environment

This directory contains PowerShell scripts to automate the setup and
configuration of IIS (Internet Information Services) for local Creatio
development instances.

## Prerequisites

- Windows 10/11 or Windows Server 2019/2022
- PowerShell 5.1 or later
- Administrator privileges
- .NET Framework 4.8 or later

## Quick Start

1. **Open PowerShell as Administrator**
   - Right-click on PowerShell and select "Run as Administrator"

2. **Navigate to the script directory**

   ```powershell
   cd "C:\path\to\creatio-ai-knowledge-hub\iis-setup"
   ```

3. **Run the main setup script**
   ```powershell
   .\00-main-setup.ps1
   ```

This will run all setup steps in the correct order.

## Individual Scripts

If you prefer to run individual setup steps, use these scripts in order:

### 1. Enable IIS Features (`01-enable-iis-features.ps1`)

Enables all required IIS features for Creatio:

- IIS Core Features (Web Server, HTTP Features)
- ASP.NET 4.8 and .NET Framework support
- IIS Management Console
- Application Development features
- Security and authentication modules

```powershell
.\01-enable-iis-features.ps1
```

### 2. Configure Application Pools (`02-configure-application-pools.ps1`)

Creates and configures application pools optimized for Creatio:

- CreatioDevPool (Development)
- CreatioTestPool (Testing)
- CreatioStagingPool (Staging)

Each pool is configured with:

- .NET Framework 4.8
- Integrated pipeline mode
- No idle timeout
- Optimized recycling settings
- Proper failure handling

```powershell
.\02-configure-application-pools.ps1
```

### 3. Setup SSL Certificates (`03-setup-ssl-certificates.ps1`)

Creates self-signed certificates for local development:

- localhost certificate
- Custom domain certificates (creatio-dev.local, etc.)
- Automatically adds entries to hosts file
- Configures certificate trust

```powershell
.\03-setup-ssl-certificates.ps1
```

### 4. Create IIS Sites (`04-create-iis-sites.ps1`)

Creates IIS websites for different Creatio instances:

| Site           | URL                               | HTTPS URL                          | Physical Path                     |
| -------------- | --------------------------------- | ---------------------------------- | --------------------------------- |
| CreatioDev     | http://creatio-dev.local:8080     | https://creatio-dev.local:8443     | C:\inetpub\wwwroot\CreatioDev     |
| CreatioTest    | http://creatio-test.local:8081    | https://creatio-test.local:8444    | C:\inetpub\wwwroot\CreatioTest    |
| CreatioStaging | http://creatio-staging.local:8082 | https://creatio-staging.local:8445 | C:\inetpub\wwwroot\CreatioStaging |

```powershell
.\04-create-iis-sites.ps1
```

### 5. Configure Permissions (`05-configure-permissions.ps1`)

Sets up proper file system permissions and security:

- Application pool identity permissions
- IIS_IUSRS permissions
- Temp and log directory permissions
- Authentication settings
- Security headers
- Request filtering
- MIME types for modern web assets

```powershell
.\05-configure-permissions.ps1
```

## Advanced Usage

### Skip Specific Steps

```powershell
# Skip SSL setup
.\00-main-setup.ps1 -SkipSSL

# Skip multiple steps
.\00-main-setup.ps1 -SkipSSL -SkipPermissions
```

### Customizing Site Configuration

To modify the site configurations, edit the `$siteConfigs` array in
`04-create-iis-sites.ps1`:

```powershell
$siteConfigs = @(
    @{
        Name = "CreatioDev"
        Path = "C:\inetpub\wwwroot\CreatioDev"
        Pool = "CreatioDevPool"
        HttpPort = 8080
        HttpsPort = 8443
        HostHeader = "creatio-dev.local"
    }
    # Add more sites as needed
)
```

## Post-Setup Configuration

After running the scripts, you'll need to:

1. **Deploy Creatio Application Files**
   - Copy your Creatio application files to the respective directories
   - Ensure proper file permissions are maintained

2. **Configure Database Connections**
   - Update `web.config` files with database connection strings
   - Configure Redis connection strings if using caching

3. **Test Site Access**
   - Visit the URLs to verify sites are working
   - Check IIS Manager for any issues

4. **Configure Development Settings**
   - Enable debug mode in web.config for development
   - Configure logging levels
   - Set up any environment-specific settings

## Troubleshooting

### Common Issues

1. **"Access Denied" errors**
   - Ensure you're running PowerShell as Administrator
   - Check that application pool identity has proper permissions

2. **SSL Certificate errors**
   - Re-run the SSL setup script
   - Check that certificates are installed in both Personal and Trusted Root
     stores

3. **Site won't start**
   - Check application pool is running
   - Verify .NET Framework version compatibility
   - Check Windows Event Logs for detailed errors

4. **404 errors**
   - Verify application files are deployed correctly
   - Check default document settings
   - Ensure ASP.NET is properly registered

### Useful Commands

```powershell
# Check IIS installation
Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -like "IIS-*" -and $_.State -eq "Enabled"}

# List application pools
Get-IISAppPool

# List websites
Get-Website

# Check site bindings
Get-WebBinding -Name "CreatioDev"

# Restart application pool
Restart-WebAppPool -Name "CreatioDevPool"

# Check SSL certificates
Get-ChildItem -Path "Cert:\LocalMachine\My" | Where-Object {$_.Subject -like "*creatio*"}
```

### Event Logs

Check these event logs for troubleshooting:

- Windows Logs > Application
- Windows Logs > System
- Applications and Services Logs > Microsoft > Windows > IIS-W3SVC-WP

## Security Considerations

### Development Environment Only

These scripts are designed for local development environments. For production
deployments:

- Use proper SSL certificates from a trusted CA
- Configure more restrictive security settings
- Use service accounts with minimal required permissions
- Enable additional security features

### Default Security Settings

The scripts configure basic security settings:

- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- Request filtering
- Anonymous authentication enabled
- Forms authentication mode

## File Structure

```
iis-setup/
├── 00-main-setup.ps1              # Main orchestration script
├── 01-enable-iis-features.ps1     # IIS feature enablement
├── 02-configure-application-pools.ps1  # Application pool setup
├── 03-setup-ssl-certificates.ps1  # SSL certificate configuration
├── 04-create-iis-sites.ps1        # IIS site creation
├── 05-configure-permissions.ps1   # Permissions and security
└── README.md                       # This file
```

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review Windows Event Logs
3. Verify prerequisites are met
4. Ensure all scripts are run with Administrator privileges

## Contributing

To improve these scripts:

1. Test changes in a clean Windows environment
2. Ensure backward compatibility
3. Update documentation
4. Add error handling for edge cases

---

**Note**: These scripts modify system settings and install certificates. Always
test in a development environment first.
