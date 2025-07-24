# PowerShell Script to Configure Application Pools for Creatio
# Run as Administrator in PowerShell

Import-Module WebAdministration

Write-Host "Configuring Application Pools for Creatio..." -ForegroundColor Green

# Function to create and configure application pool
function New-CreatioAppPool {
    param(
        [string]$PoolName,
        [string]$NetFrameworkVersion = "v4.0",
        [string]$ManagedPipelineMode = "Integrated",
        [int]$IdleTimeoutMinutes = 0,
        [int]$MaxProcesses = 1,
        [string]$Identity = "ApplicationPoolIdentity"
    )
    
    Write-Host "Creating application pool: $PoolName" -ForegroundColor Blue
    
    # Remove existing pool if it exists
    if (Get-IISAppPool -Name $PoolName -ErrorAction SilentlyContinue) {
        Remove-WebAppPool -Name $PoolName
        Write-Host "Removed existing pool: $PoolName" -ForegroundColor Yellow
    }
    
    # Create new application pool
    New-WebAppPool -Name $PoolName
    
    # Configure application pool settings
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "managedRuntimeVersion" -Value $NetFrameworkVersion
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "managedPipelineMode" -Value $ManagedPipelineMode
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "processModel.identityType" -Value $Identity
    
    # Set idle timeout (0 = disabled)
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "processModel.idleTimeout" -Value "00:0$($IdleTimeoutMinutes):00"
    
    # Set maximum worker processes
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "processModel.maxProcesses" -Value $MaxProcesses
    
    # Enable 32-bit applications if needed (usually false for modern systems)
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "enable32BitAppOnWin64" -Value $false
    
    # Set memory and CPU limits for better performance
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "processModel.memoryLimit" -Value 0  # 0 = no limit
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "cpu.limit" -Value 0  # 0 = no limit
    
    # Configure recycling conditions
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "recycling.periodicRestart.time" -Value "1.05:00:00"  # 29 hours
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "recycling.periodicRestart.memory" -Value 0  # 0 = disabled
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "recycling.periodicRestart.privateMemory" -Value 0  # 0 = disabled
    
    # Set failure settings
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "failure.rapidFailProtection" -Value $true
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "failure.rapidFailProtectionInterval" -Value "00:05:00"
    Set-ItemProperty -Path "IIS:\AppPools\$PoolName" -Name "failure.rapidFailProtectionMaxCrashes" -Value 5
    
    Write-Host "Application pool $PoolName configured successfully!" -ForegroundColor Green
}

# Create application pools for different Creatio instances
New-CreatioAppPool -PoolName "CreatioDevPool" -IdleTimeoutMinutes 0
New-CreatioAppPool -PoolName "CreatioTestPool" -IdleTimeoutMinutes 0
New-CreatioAppPool -PoolName "CreatioStagingPool" -IdleTimeoutMinutes 0

# Optional: Create a pool with specific user identity for database access
# Uncomment and modify as needed
# $credential = Get-Credential -Message "Enter credentials for Creatio service account"
# New-CreatioAppPool -PoolName "CreatioServicePool" -Identity "SpecificUser" -IdleTimeoutMinutes 0

Write-Host "All application pools created and configured!" -ForegroundColor Green

# Display created pools
Write-Host "`nCreated Application Pools:" -ForegroundColor Blue
Get-IISAppPool | Where-Object {$_.Name -like "*Creatio*"} | Select-Object Name, State, ManagedRuntimeVersion, ManagedPipelineMode
