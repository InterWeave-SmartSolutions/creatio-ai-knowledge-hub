# Complete Creatio Local Installation Guide

## Overview

This guide provides step-by-step instructions for setting up a complete local
Creatio development environment based on the official documentation and
developer course materials.

## Prerequisites

### Hardware Requirements

- **CPU**: Intel Core i5 (12 cores) or equivalent
- **RAM**: 16GB recommended (8GB minimum)
- **Storage**: SSD recommended for performance
- **OS**: Windows 10/11 Pro (Home has websocket limitations)

### Software Requirements

- Windows 10/11 Pro
- Microsoft SQL Server Developer Edition (recommended) or Express
- SQL Server Management Studio (SSMS)
- Redis for Windows
- .NET 6 SDK / .NET Framework 4.8
- Visual C++ Redistributables
- IIS (Internet Information Services)

## Step 1: Download Creatio Installation Files

1. Obtain the Creatio installation ZIP file (~1GB)
2. Choose the correct version:
   - Windows + Microsoft SQL Server
   - Windows + PostgreSQL
   - Linux + PostgreSQL
3. Extract to a non-protected folder (not in Program Files, Windows, etc.)
   - Recommended: `D:\Creatio\` or similar

## Step 2: Install and Configure Redis Cache Server

### Download and Install Redis

```bash
# Download Redis for Windows from GitHub
# https://github.com/tporadowski/redis/releases
# Install the MSI file with administrator privileges
```

### Verify Redis Installation

1. Check Windows Services for "Redis Server"
2. Ensure it's running
3. Default settings are sufficient for development

**Troubleshooting**: If Redis fails to start, uninstall and reinstall with
administrator privileges.

## Step 3: Database Server Setup

### Install Microsoft SQL Server

1. Download SQL Server Developer Edition (free)
2. Install with default settings
3. **Important**: Change authentication to "SQL Server and Windows
   Authentication mode"
4. Restart SQL Server after changing authentication mode

### Configure Database

1. Open SQL Server Management Studio (SSMS)
2. Restore database from backup file:
   ```sql
   -- Right-click Databases → Restore Database → From Device
   -- Select the .bak file from DB folder in Creatio installation
   -- Name database (e.g., "D1Studio" - avoid dots in name)
   ```

### Create Database Login and User

```sql
-- Create Login
CREATE LOGIN [D1Login] WITH PASSWORD = 'YourPassword'

-- Create User in Database
USE [D1Studio]
CREATE USER [D1Login] FOR LOGIN [D1Login]

-- Grant db_owner permissions
ALTER ROLE db_owner ADD MEMBER [D1Login]
```

## Step 4: Enable Required Windows Components

### Install Visual C++ Redistributables

- Download and install Microsoft Visual C++ Redistributables
- .NET 6 SDK
- .NET Framework 4.8 SDK

### Enable Windows Features

Go to Control Panel → Programs → Turn Windows features on or off:

**Required Components:**

- ✅ Internet Information Services
  - ✅ IIS Management Console
  - ✅ World Wide Web Services
  - ✅ Application Development Features
  - ✅ WebSocket Protocol
- ✅ .NET Framework 3.5 (includes .NET 2.0 and 3.0)
  - ✅ Windows Communication Foundation HTTP Activation
- ✅ .NET Framework 4.8 Advanced Services
  - ✅ Windows Communication Foundation HTTP Activation

**Critical**: Enable WebSocket Protocol and WCF HTTP Activation for both .NET
versions.

## Step 5: Configure IIS Application

### Create Application Pool

1. Open IIS Manager
2. Application Pools → Add Application Pool
3. Name: "CreatioStudio" (or your preferred name)
4. .NET CLR Version: .NET CLR Version v4.0
5. Managed Pipeline Mode: Integrated

### Create Website Application

1. Sites → Default Web Site → Add Application
2. **Important**: Alias must start with a LETTER, not digit (e.g., "D1Studio")
3. Application Pool: Select the pool created above
4. Physical Path: Point to Creatio root folder

### Add Inner Application

1. Select your created application → Add Application
2. Alias: "0" (zero)
3. Application Pool: Same as parent
4. Physical Path: Point to `Terrasoft.WebApp` folder inside Creatio installation

## Step 6: Configure Connection Strings

Edit `ConnectionStrings.config` in Creatio root folder:

```xml
<!-- Database Connection -->
<add name="db"
     connectionString="Data Source=localhost;Initial Catalog=D1Studio;User ID=D1Login;Password=YourPassword;MultipleActiveResultSets=True;ConnectRetryCount=2"
     providerName="System.Data.SqlClient" />

<!-- Redis Connection -->
<add name="redis"
     connectionString="host=localhost;db=1;port=6379" />
```

**Key Points:**

- Remove `Integrated Security=SSPI` if using SQL authentication
- Use unique `db` numbers for multiple Creatio instances
- Use `localhost` for Redis host if network name fails

## Step 7: Optional Log Configuration

Edit `Terrasoft.WebApp\NLog.config`:

```xml
<!-- Change log directory to accessible location -->
<variable name="logDir" value="C:\CreatioLogs\${var:name}" />
```

## Step 8: First Startup and Compilation

### Start the Application

1. In IIS Manager, browse your application
2. Default credentials: Username: `Supervisor`, Password: `Supervisor`

### Handle Common Compilation Error

If you encounter compilation errors:

1. Create folders: `C:\Windows\System32\inetsrv\NuGet\Migrations`
2. This fixes .NET 6 compilation issues

### Compile the Application

1. Go to System Designer → Advanced Settings
2. Click "Compile" button
3. Wait for compilation to complete
4. Verify DLL files appear in `Terrasoft.Configuration\bin` folder

## Step 9: Enable File System Development Mode

### Modify Web.config

Edit root `web.config` file:

```xml
<!-- Line ~510 -->
<add key="FileDesignMode" value="true" />

<!-- Line ~563 -->
<add key="UseStaticFileContent" value="false" />
```

### Download Packages to File System

1. Go to Configuration section (add `/0/dev` to URL)
2. Actions → Download packages to file system
3. Verify files appear in `Terrasoft.WebApp\conf\pkg` folder

### Final Compilation

Compile the system once more to ensure everything works correctly.

## Step 10: Optional Optimizations

### Disable Noisy Console Messages

1. User Profile → Additional Settings → Call Center
2. Disable "Call center integration"

### Disable Login Widgets

System Settings → Search for:

- "Show widget on login page" → Disable
- "Show widget on intro page" → Disable

## Step 11: Clio Setup (Development Tool)

Install and configure Clio for enhanced development experience:

```bash
# Install Clio globally
npm install -g clio

# Register development environment
clio reg-web-app local -u http://localhost/D1Studio -l Supervisor -p Supervisor
```

## Verification Checklist

- [ ] Redis service running
- [ ] SQL Server accessible with created login
- [ ] Database restored successfully
- [ ] IIS application responds to requests
- [ ] Successful login with Supervisor account
- [ ] System compiles without errors
- [ ] File system development mode enabled
- [ ] Package download to file system works

## Troubleshooting

### Common Issues

1. **Compilation Errors**: Create NuGet/Migrations folders in System32/inetsrv
2. **Redis Connection**: Use `localhost` instead of machine name
3. **IIS Hanging**: Check websocket limitations on Windows Home
4. **Database Connection**: Verify SQL authentication mode and login permissions
5. **File Permissions**: Ensure Creatio folder is not in protected Windows
   directory

### Log Locations

- Application logs: Configured location (e.g., `C:\CreatioLogs`)
- Compilation logs: `{LogDirectory}\0\Build.log`
- IIS logs: `C:\inetpub\logs\LogFiles`

## Next Steps

1. Set up Git integration for version control
2. Configure Visual Studio or other IDE integration
3. Create custom packages for development
4. Set up team development workflows

## Environment Types

- **Development**: Local file system mode with full debugging capabilities
- **Test**: Copy of production for testing deployments
- **Production**: Live environment with database-only mode

Remember: Always use separate environments and never develop directly on
production!

---

_This guide is based on Creatio 8.1.3+ and may need adjustments for different
versions._
