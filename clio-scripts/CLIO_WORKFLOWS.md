# Clio Workflows Documentation

## Table of Contents

1. [Getting Started](#getting-started)
2. [Environment Management](#environment-management)
3. [Package Development Workflow](#package-development-workflow)
4. [Workspace Management](#workspace-management)
5. [Development and Debugging](#development-and-debugging)
6. [Deployment Workflows](#deployment-workflows)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Getting Started

### Initial Setup

1. **Install Clio globally:**

   ```bash
   npm install -g clio
   ```

2. **Verify installation:**

   ```bash
   clio --version
   ```

3. **Register your first environment:**

   ```bash
   # For cloud environments
   clio reg-web-app myenv -u https://mysite.creatio.com -l username -p password

   # For local environments
   clio reg-web-app local -u http://localhost -l Supervisor -p Supervisor
   ```

## Environment Management

### Registering Environments

#### Cloud Environment (mkpdev-interweave)

```bash
# Register the environment
clio reg-web-app mkpdev-interweave -u https://mkpdev-interweave.creatio.com

# Set credentials (replace with actual values)
clio reg-web-app mkpdev-interweave -u https://mkpdev-interweave.creatio.com -l YOUR_USERNAME -p YOUR_PASSWORD --checkLogin

# Set as active environment
clio reg-web-app mkpdev-interweave -a
```

#### Local Development Environment

```bash
# Register local environment
clio reg-web-app local -u http://localhost -l Supervisor -p Supervisor -a

# For IIS environments
clio reg-web-app local-iis -u http://localhost/CreatioInstance -l Supervisor -p Supervisor
```

### Environment Operations

```bash
# List all environments
clio show-web-app-list

# Test connection
clio ping-app -e mkpdev-interweave

# Open in browser
clio open-web-app -e mkpdev-interweave

# Restart application (use with caution)
clio restart-web-app -e mkpdev-interweave
```

## Package Development Workflow

### Creating a New Package

```bash
# Create new package
clio new-pkg MyCustomPackage

# Navigate to package directory
cd MyCustomPackage

# Add schemas/items to package
clio add-item entity MyEntity -p MyCustomPackage
clio add-item page MyPage -p MyCustomPackage
clio add-item process MyProcess -p MyCustomPackage
```

### Package Development Cycle

#### 1. Local Development

```bash
# Create package locally
clio new-pkg MyPackage

# Develop your schemas, pages, processes
# Add items as needed
clio add-item entity Contact -p MyPackage
```

#### 2. Push to Development Environment

```bash
# Push package to environment
clio push-pkg MyPackage -e mkpdev-interweave

# Set developer mode for easier debugging
clio set-dev-mode -e mkpdev-interweave
```

#### 3. Testing and Iteration

```bash
# Pull modified package back (if changes made in UI)
clio pull-pkg MyPackage -e mkpdev-interweave

# Make changes locally, then push again
clio push-pkg MyPackage -e mkpdev-interweave
```

#### 4. Package Management

```bash
# List packages in environment
clio get-pkg-list -e mkpdev-interweave

# Delete package from environment
clio delete-pkg-remote MyPackage -e mkpdev-interweave

# Generate package archive
clio generate-pkg-zip MyPackage
```

## Workspace Management

### Creating and Managing Workspaces

```bash
# Create a new workspace
clio create-workspace MyWorkspace

# This creates a MyWorkspace.cmd file
# Configure workspace for specific environment
clio cfg-worspace -e mkpdev-interweave

# Add packages to workspace
clio add-package MyPackage1 MyPackage2

# Push entire workspace
clio push-workspace -e mkpdev-interweave

# Restore workspace
clio restore-workspace
```

### Workspace Best Practices

1. **Environment-specific workspaces:** Create separate workspaces for different
   environments
2. **Version control:** Keep workspace configuration files in version control
3. **Dependency management:** Ensure all required packages are included in
   workspace

## Development and Debugging

### Developer Mode

```bash
# Enable developer mode
clio set-dev-mode -e mkpdev-interweave

# This enables:
# - Detailed error messages
# - SQL query logging
# - Enhanced debugging capabilities
```

### System Settings Management

```bash
# Set system setting
clio set-syssetting "SettingName" "SettingValue" -e mkpdev-interweave

# Examples:
clio set-syssetting "UseDebugMode" "true" -e mkpdev-interweave
clio set-syssetting "SqlCommandTimeout" "300" -e mkpdev-interweave
```

### Feature Toggle Management

```bash
# Enable feature
clio set-feature "FeatureName" "true" -e mkpdev-interweave

# Disable feature
clio set-feature "FeatureName" "false" -e mkpdev-interweave
```

### SQL Script Execution

```bash
# Execute SQL script
clio execute-sql-script script.sql -e mkpdev-interweave

# Example script content (script.sql):
# UPDATE SysSettings SET Value = 'true' WHERE Name = 'UseDebugMode'
```

### DataService and Web Service Calls

```bash
# DataService request
clio dataservice -e mkpdev-interweave -t "select" -d '{"rootSchemaName":"Contact","operationType":0}'

# Call custom web service
clio call-service MyService MyMethod -e mkpdev-interweave
```

## Deployment Workflows

### Standard Deployment Process

#### 1. Prepare Package

```bash
# Create package archive
clio generate-pkg-zip MyPackage

# Verify package contents
clio extract-pkg-zip MyPackage.zip ./temp-extract
```

#### 2. Deploy to Environment

```bash
# Push package
clio push-pkg MyPackage -e mkpdev-interweave

# Verify deployment
clio get-pkg-list -e mkpdev-interweave | grep MyPackage
```

#### 3. Post-Deployment Tasks

```bash
# Compile configuration if needed
clio compile-configuration -e mkpdev-interweave

# Restart application if required
clio restart-web-app -e mkpdev-interweave
```

### Advanced Deployment with Manifests

```bash
# Create and apply manifest
clio apply-manifest manifest.json -e mkpdev-interweave

# Example manifest.json:
# {
#   "Packages": ["Package1", "Package2"],
#   "Settings": {
#     "SettingName": "SettingValue"
#   },
#   "Features": {
#     "FeatureName": true
#   }
# }
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Authentication Problems

```bash
# Re-register environment with credentials
clio reg-web-app mkpdev-interweave -u https://mkpdev-interweave.creatio.com -l username -p password --checkLogin

# Check current configuration
clio show-web-app-list
```

#### 2. Package Push Failures

```bash
# Check package structure
ls -la MyPackage/

# Verify environment connection
clio ping-app -e mkpdev-interweave

# Try with force flag (use carefully)
clio push-pkg MyPackage -e mkpdev-interweave --force
```

#### 3. Compilation Issues

```bash
# Get compilation log
clio last-compilation-log -e mkpdev-interweave

# Manually trigger compilation
clio compile-configuration -e mkpdev-interweave
```

#### 4. Environment Not Responding

```bash
# Check environment status
clio ping-app -e mkpdev-interweave

# Get system information
clio get-info -e mkpdev-interweave

# Health check
clio healthcheck -e mkpdev-interweave
```

### Debug Commands

```bash
# Show package file content
clio show-package-file-content MyPackage MySchema.cs

# Get build information
clio get-build-info -e mkpdev-interweave

# Monitor with websocket
clio listen -e mkpdev-interweave
```

## Best Practices

### 1. Environment Management

- **Use descriptive names** for environments
- **Test connections** before deployment
- **Keep credentials secure** - consider using environment variables
- **Document environment purposes** (dev, test, prod)

### 2. Package Development

- **Follow naming conventions** for packages and schemas
- **Use version control** for package source code
- **Test thoroughly** before deployment
- **Maintain package dependencies** properly

### 3. Deployment Strategy

- **Always backup** before major deployments
- **Use staging environments** for testing
- **Deploy during maintenance windows** for production
- **Monitor applications** after deployment

### 4. Security Considerations

- **Use strong passwords** for environment access
- **Limit developer mode** to development environments only
- **Review SQL scripts** before execution
- **Audit package contents** before deployment

### 5. Performance Optimization

- **Enable compilation** after package deployment
- **Monitor system settings** that affect performance
- **Use appropriate timeout values** for long-running operations
- **Clean up unused packages** regularly

## Quick Reference Commands

### Most Used Commands

```bash
# Environment management
clio show-web-app-list
clio ping-app -e <env>
clio set-dev-mode -e <env>

# Package operations
clio new-pkg <name>
clio push-pkg <package> -e <env>
clio pull-pkg <package> -e <env>
clio get-pkg-list -e <env>

# Workspace operations
clio create-workspace <name>
clio push-workspace -e <env>
clio restore-workspace

# Utilities
clio open-web-app -e <env>
clio restart-web-app -e <env>
clio execute-sql-script <file> -e <env>
```

### Useful Aliases

Add these to your `.bashrc` or `.zshrc`:

```bash
alias clio-envs='clio show-web-app-list'
alias clio-ping='clio ping-app -e'
alias clio-packages='clio get-pkg-list -e'
alias clio-push='clio push-pkg'
alias clio-pull='clio pull-pkg'
```

---

**Note:** Replace `mkpdev-interweave` with your actual environment name and
provide actual credentials when setting up authentication.

For more detailed information, consult the official Clio documentation or use
`clio help <command>` for specific command help.
