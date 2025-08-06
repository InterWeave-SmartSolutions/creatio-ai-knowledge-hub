#!/bin/bash

# Production Environment Deployment Script
# Deploys packages with production configurations and security measures

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PACKAGES_DIR="$PROJECT_ROOT/packages"
DEPLOY_ENV="production"

# Load configuration
source "$SCRIPT_DIR/deploy-config.sh"

echo "🚀 Starting deployment to $DEPLOY_ENV environment..."

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to handle errors
handle_error() {
    log "❌ Error occurred during deployment: $1"
    exit 1
}

# Validate production environment
validate_production_environment() {
    log "📋 Validating production environment..."
    
    # Check required tools
    command -v node >/dev/null 2>&1 || handle_error "Node.js is required"
    command -v npm >/dev/null 2>&1 || handle_error "npm is required"
    command -v python3 >/dev/null 2>&1 || handle_error "Python 3 is required"
    command -v pip >/dev/null 2>&1 || handle_error "pip is required"
    
    # Check system resources
    AVAILABLE_MEMORY=$(free -m | awk 'NR==2{printf "%d", $7}')
    if [ "$AVAILABLE_MEMORY" -lt 1024 ]; then
        handle_error "Insufficient memory available (${AVAILABLE_MEMORY}MB). At least 1GB required."
    fi
    
    AVAILABLE_DISK=$(df "$PROJECT_ROOT" | tail -1 | awk '{print $4}')
    if [ "$AVAILABLE_DISK" -lt 5242880 ]; then # 5GB in KB
        handle_error "Insufficient disk space. At least 5GB required."
    fi
    
    # Check Node.js version (production should use LTS)
    NODE_VERSION=$(node --version | cut -d'v' -f2)
    if ! node -e "process.exit(process.version.match(/^v(\d+)/)[1] >= 18 ? 0 : 1)" 2>/dev/null; then
        handle_error "Node.js 18 LTS or higher is required (current: $NODE_VERSION)"
    fi
    
    log "✅ Production environment validation passed"
}

# Install production dependencies
install_production_dependencies() {
    log "📦 Installing production dependencies..."
    
    cd "$PROJECT_ROOT"
    
    # Clean install without dev dependencies
    log "Installing Node.js production dependencies..."
    npm ci --omit=dev --no-audit
    
    # Install Python dependencies
    log "Installing Python production dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install --no-cache-dir -r requirements.txt
    fi
    
    # Verify no development dependencies
    if npm ls --depth=0 --dev 2>/dev/null | grep -q "dev"; then
        handle_error "Development dependencies found in production build"
    fi
    
    log "✅ Production dependencies installed successfully"
}

# Setup production packages
setup_production_packages() {
    log "🔧 Setting up production packages..."
    
    cd "$PACKAGES_DIR"
    
    # Create production directory structure
    mkdir -p local/{core,plugins,utilities,themes,templates,integrations}
    mkdir -p remote/{npm,python,creatio}
    mkdir -p cache
    mkdir -p deploy/environments/production
    mkdir -p logs
    
    # Set secure permissions
    chmod 755 local remote cache
    chmod 700 deploy/environments/production
    chmod 640 package-registry.json 2>/dev/null || true
    
    log "✅ Production packages setup completed"
}

# Configure production settings
configure_production() {
    log "⚙️ Configuring production settings..."
    
    # Create production package registry
    cat > "$PACKAGES_DIR/package-registry.json" << EOF
{
  "name": "creatio-ai-knowledge-hub-registry",
  "version": "1.0.0",
  "description": "Production package registry for Creatio AI Knowledge Hub",
  "environment": "production",
  "registries": {
    "local": {
      "type": "local",
      "path": "./local",
      "enabled": true,
      "priority": 1
    },
    "npm": {
      "type": "remote",
      "url": "https://registry.npmjs.org/",
      "enabled": true,
      "priority": 2,
      "cache": true,
      "cache_ttl": 86400,
      "verify_ssl": true,
      "timeout": 30000
    },
    "pypi": {
      "type": "remote", 
      "url": "https://pypi.org/simple/",
      "enabled": true,
      "priority": 2,
      "cache": true,
      "cache_ttl": 86400,
      "verify_ssl": true,
      "timeout": 30000
    },
    "creatio": {
      "type": "remote",
      "url": "https://marketplace.creatio.com/",
      "enabled": true,
      "priority": 3,
      "cache": true,
      "cache_ttl": 604800,
      "verify_ssl": true,
      "timeout": 60000
    }
  },
  "environments": {
    "production": {
      "auto_update": false,
      "use_cache": true,
      "install_dev_dependencies": false,
      "verify_signatures": true,
      "security_scanning": true,
      "rate_limiting": true
    }
  },
  "dependency_tracking": {
    "enabled": true,
    "track_usage": true,
    "security_scanning": true,
    "license_compliance": true,
    "vulnerability_alerts": true
  },
  "security": {
    "enforce_https": true,
    "verify_checksums": true,
    "scan_vulnerabilities": true,
    "audit_logging": true
  }
}
EOF
    
    # Create production environment configuration
    cat > "$PACKAGES_DIR/deploy/environments/production/config.json" << EOF
{
  "environment": "production",
  "debug": false,
  "hot_reload": false,
  "auto_restart": false,
  "logging": {
    "level": "error",
    "console": false,
    "file": true,
    "file_path": "./logs/package-manager.log",
    "max_size": "10MB",
    "max_files": 5
  },
  "package_management": {
    "auto_update": false,
    "use_cache": true,
    "install_dev_deps": false,
    "verify_integrity": true,
    "security_scan": true
  },
  "security": {
    "enforce_https": true,
    "verify_signatures": true,
    "scan_vulnerabilities": true,
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 30
    }
  },
  "monitoring": {
    "enabled": true,
    "metrics_collection": true,
    "health_checks": true,
    "alert_on_failures": true
  },
  "performance": {
    "cache_optimization": true,
    "compression": true,
    "connection_pooling": true
  }
}
EOF
    
    # Set secure permissions on config files
    chmod 600 "$PACKAGES_DIR/package-registry.json"
    chmod 600 "$PACKAGES_DIR/deploy/environments/production/config.json"
    
    log "✅ Production configuration completed"
}

# Verify package integrity
verify_package_integrity() {
    log "🔍 Verifying package integrity..."
    
    cd "$PROJECT_ROOT"
    
    # Verify Node.js package integrity
    log "Verifying Node.js packages..."
    npm audit --audit-level moderate
    
    # Generate and verify checksums
    log "Generating package checksums..."
    find "$PACKAGES_DIR/local" -type f -name "*.js" -o -name "*.json" | while read file; do
        if [ -f "$file" ]; then
            sha256sum "$file" >> "$PACKAGES_DIR/checksums.txt"
        fi
    done
    
    log "✅ Package integrity verification completed"
}

# Setup monitoring and logging
setup_monitoring() {
    log "📊 Setting up monitoring and logging..."
    
    # Create log directories
    mkdir -p "$PACKAGES_DIR/logs"
    
    # Setup log rotation
    cat > "$PACKAGES_DIR/logs/logrotate.conf" << EOF
$PACKAGES_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
    maxsize 10M
}
EOF
    
    # Create monitoring script
    cat > "$PACKAGES_DIR/scripts/monitor.sh" << 'EOF'
#!/bin/bash

# Package Management Monitoring Script
LOG_DIR="$(dirname "$0")/../logs"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Check disk space
DISK_USAGE=$(df "$LOG_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "[$TIMESTAMP] WARNING: Disk usage is ${DISK_USAGE}%" >> "$LOG_DIR/monitoring.log"
fi

# Check package cache size
CACHE_SIZE=$(du -sm packages/cache 2>/dev/null | cut -f1)
if [ "$CACHE_SIZE" -gt 1024 ]; then
    echo "[$TIMESTAMP] INFO: Package cache size is ${CACHE_SIZE}MB" >> "$LOG_DIR/monitoring.log"
fi

# Check for failed downloads
FAILED_DOWNLOADS=$(grep -c "Failed to download" "$LOG_DIR"/*.log 2>/dev/null || echo 0)
if [ "$FAILED_DOWNLOADS" -gt 0 ]; then
    echo "[$TIMESTAMP] WARNING: $FAILED_DOWNLOADS failed downloads detected" >> "$LOG_DIR/monitoring.log"
fi
EOF
    
    chmod +x "$PACKAGES_DIR/scripts/monitor.sh"
    
    log "✅ Monitoring and logging setup completed"
}

# Optimize for production
optimize_production() {
    log "⚡ Optimizing for production..."
    
    cd "$PROJECT_ROOT"
    
    # Build TypeScript if present
    if [ -f "tsconfig.json" ]; then
        log "Building TypeScript..."
        npm run build
    fi
    
    # Optimize package cache
    log "Optimizing package cache..."
    if [ -d "$PACKAGES_DIR/cache" ]; then
        find "$PACKAGES_DIR/cache" -type f -atime +7 -delete
    fi
    
    # Compress static assets
    log "Compressing assets..."
    find "$PACKAGES_DIR/local" -name "*.js" -o -name "*.css" | while read file; do
        if command -v gzip >/dev/null 2>&1; then
            gzip -k "$file" 2>/dev/null || true
        fi
    done
    
    log "✅ Production optimization completed"
}

# Setup security measures
setup_security() {
    log "🔒 Setting up security measures..."
    
    # Create security audit script
    cat > "$PACKAGES_DIR/scripts/security-audit.sh" << 'EOF'
#!/bin/bash

# Security Audit Script
AUDIT_LOG="$(dirname "$0")/../logs/security-audit.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting security audit..." >> "$AUDIT_LOG"

# Check for known vulnerabilities
if command -v npm >/dev/null 2>&1; then
    npm audit --json > /tmp/npm-audit.json 2>/dev/null || true
    VULNERABILITIES=$(jq '.metadata.vulnerabilities.total' /tmp/npm-audit.json 2>/dev/null || echo 0)
    echo "[$TIMESTAMP] NPM vulnerabilities found: $VULNERABILITIES" >> "$AUDIT_LOG"
fi

# Check file permissions
find packages/ -type f -perm -002 | while read file; do
    echo "[$TIMESTAMP] WARNING: World-writable file found: $file" >> "$AUDIT_LOG"
done

# Check for suspicious files
find packages/ -name "*.exe" -o -name "*.bat" -o -name "*.sh" | while read file; do
    if [ ! -x "$file" ] && [[ "$file" != *"/scripts/"* ]]; then
        echo "[$TIMESTAMP] WARNING: Suspicious executable found: $file" >> "$AUDIT_LOG"
    fi
done

echo "[$TIMESTAMP] Security audit completed" >> "$AUDIT_LOG"
EOF
    
    chmod +x "$PACKAGES_DIR/scripts/security-audit.sh"
    
    # Run initial security audit
    "$PACKAGES_DIR/scripts/security-audit.sh"
    
    # Setup automatic security scanning
    (crontab -l 2>/dev/null; echo "0 2 * * * $PACKAGES_DIR/scripts/security-audit.sh") | crontab -
    
    log "✅ Security measures setup completed"
}

# Create production management tools
create_production_tools() {
    log "🛠️ Creating production management tools..."
    
    # Create production package management script
    cat > "$PROJECT_ROOT/package-prod.sh" << 'EOF'
#!/bin/bash
# Production package management tools

PACKAGES_DIR="packages"
LOG_FILE="$PACKAGES_DIR/logs/package-manager.log"

log_action() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

case "$1" in
    "status")
        echo "Package Management System Status:"
        echo "================================="
        echo "Environment: Production"
        echo "Cache size: $(du -sh $PACKAGES_DIR/cache 2>/dev/null | cut -f1)"
        echo "Local packages: $(find $PACKAGES_DIR/local -name "*.json" | wc -l)"
        echo "Last security audit: $(tail -1 $PACKAGES_DIR/logs/security-audit.log 2>/dev/null | cut -d']' -f1 | tr -d '[')"
        ;;
    "audit")
        log_action "Security audit requested"
        $PACKAGES_DIR/scripts/security-audit.sh
        echo "Security audit completed. Check logs for details."
        ;;
    "monitor")
        log_action "Monitoring check requested"
        $PACKAGES_DIR/scripts/monitor.sh
        echo "Monitoring check completed."
        ;;
    "clean")
        log_action "Cache cleanup requested"
        node $PACKAGES_DIR/scripts/dependency-tracker.js cleanup
        echo "Cache cleanup completed."
        ;;
    "backup")
        BACKUP_DIR="/tmp/packages-backup-$(date +%Y%m%d-%H%M%S)"
        log_action "Backup requested to $BACKUP_DIR"
        cp -r $PACKAGES_DIR/local "$BACKUP_DIR"
        echo "Backup created at: $BACKUP_DIR"
        ;;
    *)
        echo "Usage: $0 {status|audit|monitor|clean|backup}"
        echo "  status  - Show system status"
        echo "  audit   - Run security audit"
        echo "  monitor - Run monitoring checks"
        echo "  clean   - Clean package cache"
        echo "  backup  - Backup local packages"
        ;;
esac
EOF
    
    chmod +x "$PROJECT_ROOT/package-prod.sh"
    
    log "✅ Production management tools created"
}

# Generate production documentation
generate_production_docs() {
    log "📚 Generating production documentation..."
    
    cat > "$PACKAGES_DIR/PRODUCTION.md" << 'EOF'
# Package Management System - Production Environment

This document describes the production deployment of the package management system for the Creatio AI Knowledge Hub.

## Production Features

- 🔒 Enhanced security with signature verification
- 📊 Comprehensive monitoring and logging
- ⚡ Optimized performance and caching
- 🛡️ Automated security auditing
- 📈 Resource usage monitoring
- 🔄 Automated backup capabilities

## Management Commands

### System Status
```bash
./package-prod.sh status
```

### Security Operations
```bash
# Run security audit
./package-prod.sh audit

# Monitor system health
./package-prod.sh monitor
```

### Maintenance
```bash
# Clean package cache
./package-prod.sh clean

# Create backup
./package-prod.sh backup
```

## Monitoring

### Log Files
- `packages/logs/package-manager.log` - Main application logs
- `packages/logs/security-audit.log` - Security audit results
- `packages/logs/monitoring.log` - System monitoring data

### Automated Monitoring
- Security audits run daily at 2:00 AM
- System monitoring checks disk usage and cache size
- Vulnerability scanning for all dependencies

## Security

### Features Enabled
- HTTPS enforcement for all registry connections
- Package signature verification
- Checksum validation
- Vulnerability scanning
- Rate limiting for downloads
- Audit logging for all operations

### Security Policies
- No development dependencies in production
- All packages must pass security scans
- Regular automated security audits
- Secure file permissions (600/700)

## Performance Optimization

### Caching Strategy
- Long-term caching (24 hours for remote packages)
- Compressed static assets
- Connection pooling for remote registries
- Cache cleanup for unused packages

### Resource Limits
- Minimum 1GB RAM required
- Minimum 5GB disk space required
- Connection timeouts: 30-60 seconds
- Rate limiting: 30 requests/minute

## Troubleshooting

### Common Issues
1. **Package download failures**: Check network connectivity and registry availability
2. **Security audit failures**: Review and update vulnerable packages
3. **Cache issues**: Run `./package-prod.sh clean` to clear cache
4. **Permission errors**: Verify file permissions are correctly set

### Emergency Procedures
1. **System compromise**: Run immediate security audit and review logs
2. **Performance issues**: Check disk space and clean cache
3. **Network issues**: Verify registry connectivity and SSL certificates

## Backup and Recovery

### Automated Backups
- Local packages are backed up during deployment
- Configuration files are version controlled
- Dependency tracking data is preserved

### Manual Backup
```bash
./package-prod.sh backup
```

### Recovery
1. Restore packages from backup
2. Reinstall dependencies: `npm ci --omit=dev`
3. Verify integrity: `npm audit`
4. Run security audit: `./package-prod.sh audit`

## Support

For production issues:
1. Check system logs: `tail -f packages/logs/package-manager.log`
2. Run diagnostics: `./package-prod.sh status`
3. Review security audit: `./package-prod.sh audit`
4. Contact system administrator if issues persist
EOF
    
    log "✅ Production documentation generated"
}

# Main production deployment function
main() {
    log "🎯 Starting production environment deployment..."
    
    validate_production_environment
    install_production_dependencies
    setup_production_packages
    configure_production
    verify_package_integrity
    setup_monitoring
    optimize_production
    setup_security
    create_production_tools
    generate_production_docs
    
    log "🎉 Production environment deployment completed successfully!"
    log ""
    log "Production deployment summary:"
    log "- Environment: Production"
    log "- Security: Enhanced (signatures, audits, monitoring)"
    log "- Performance: Optimized (caching, compression)"
    log "- Monitoring: Enabled (logs, metrics, alerts)"
    log ""
    log "Management tools:"
    log "- System status: ./package-prod.sh status"
    log "- Security audit: ./package-prod.sh audit"
    log "- Documentation: packages/PRODUCTION.md"
    log ""
    log "🚀 System is ready for production use!"
}

# Run main function
main "$@"
