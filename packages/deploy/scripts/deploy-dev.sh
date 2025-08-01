#!/bin/bash

# Development Environment Deployment Script
# Deploys packages with development configurations and tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PACKAGES_DIR="$PROJECT_ROOT/packages"
DEPLOY_ENV="development"

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

# Validate environment
validate_environment() {
    log "📋 Validating development environment..."
    
    # Check required tools
    command -v node >/dev/null 2>&1 || handle_error "Node.js is required"
    command -v npm >/dev/null 2>&1 || handle_error "npm is required"
    command -v python3 >/dev/null 2>&1 || handle_error "Python 3 is required"
    command -v pip >/dev/null 2>&1 || handle_error "pip is required"
    
    # Check Node.js version
    NODE_VERSION=$(node --version | cut -d'v' -f2)
    if ! node -e "process.exit(process.version.match(/^v(\d+)/)[1] >= 18 ? 0 : 1)" 2>/dev/null; then
        handle_error "Node.js 18 or higher is required (current: $NODE_VERSION)"
    fi
    
    log "✅ Environment validation passed"
}

# Install dependencies
install_dependencies() {
    log "📦 Installing dependencies..."
    
    cd "$PROJECT_ROOT"
    
    # Install Node.js dependencies
    log "Installing Node.js dependencies..."
    npm ci --include=dev
    
    # Install Python dependencies
    log "Installing Python dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    # Install development tools
    log "Installing development tools..."
    npm install -g typescript ts-node nodemon
    
    log "✅ Dependencies installed successfully"
}

# Setup local packages
setup_local_packages() {
    log "🔧 Setting up local packages..."
    
    cd "$PACKAGES_DIR"
    
    # Initialize package directories if they don't exist
    mkdir -p local/{core,plugins,utilities,themes,templates,integrations}
    mkdir -p remote/{npm,python,creatio}
    mkdir -p cache
    mkdir -p deploy/environments/development
    
    # Create symlinks for development
    if [ ! -L "$PROJECT_ROOT/node_modules/local-packages" ]; then
        ln -sf "$PACKAGES_DIR/local" "$PROJECT_ROOT/node_modules/local-packages"
    fi
    
    log "✅ Local packages setup completed"
}

# Configure development settings
configure_development() {
    log "⚙️ Configuring development settings..."
    
    # Update package registry for development
    cat > "$PACKAGES_DIR/package-registry.json" << EOF
{
  "name": "creatio-ai-knowledge-hub-registry",
  "version": "1.0.0",
  "description": "Local package registry for Creatio AI Knowledge Hub",
  "environment": "development",
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
      "cache_ttl": 3600
    },
    "pypi": {
      "type": "remote", 
      "url": "https://pypi.org/simple/",
      "enabled": true,
      "priority": 2,
      "cache": true,
      "cache_ttl": 3600
    }
  },
  "environments": {
    "development": {
      "auto_update": true,
      "use_cache": true,
      "install_dev_dependencies": true,
      "hot_reload": true,
      "debug_mode": true
    }
  },
  "dependency_tracking": {
    "enabled": true,
    "track_usage": true,
    "security_scanning": false,
    "license_compliance": false
  }
}
EOF
    
    # Create development configuration
    cat > "$PACKAGES_DIR/deploy/environments/development/config.json" << EOF
{
  "environment": "development",
  "debug": true,
  "hot_reload": true,
  "auto_restart": true,
  "logging": {
    "level": "debug",
    "console": true,
    "file": false
  },
  "package_management": {
    "auto_update": true,
    "use_cache": true,
    "install_dev_deps": true
  },
  "features": {
    "live_reload": true,
    "source_maps": true,
    "verbose_errors": true
  }
}
EOF
    
    log "✅ Development configuration completed"
}

# Start development services
start_development_services() {
    log "🔄 Starting development services..."
    
    cd "$PROJECT_ROOT"
    
    # Start package download automation in background
    if [ ! -f "$PACKAGES_DIR/scripts/download-packages.js" ]; then
        handle_error "Package download script not found"
    fi
    
    # Make scripts executable
    chmod +x "$PACKAGES_DIR/scripts"/*.js
    chmod +x "$PACKAGES_DIR/scripts"/*.py
    
    # Start dependency tracker
    log "Starting dependency tracking service..."
    node "$PACKAGES_DIR/scripts/dependency-tracker.js" analyze > /dev/null 2>&1 &
    
    log "✅ Development services started"
}

# Run tests
run_tests() {
    log "🧪 Running tests..."
    
    cd "$PROJECT_ROOT"
    
    # Run linting
    npm run lint:check
    
    # Run formatting check
    npm run format:check
    
    # Run type checking
    npm run type-check
    
    # Run unit tests
    npm run test
    
    log "✅ All tests passed"
}

# Create development shortcuts
create_shortcuts() {
    log "🔗 Creating development shortcuts..."
    
    # Create package management shortcuts
    cat > "$PROJECT_ROOT/package-dev.sh" << 'EOF'
#!/bin/bash
# Development package management shortcuts

case "$1" in
    "download")
        node packages/scripts/download-packages.js download "$2" "$3" "$4"
        ;;
    "track")
        node packages/scripts/dependency-tracker.js analyze
        ;;
    "clean")
        node packages/scripts/dependency-tracker.js cleanup
        ;;
    "install")
        python3 packages/scripts/download-packages.py install "$2"
        ;;
    *)
        echo "Usage: $0 {download|track|clean|install} [args...]"
        echo "  download <package> [version] [registry] - Download package"
        echo "  track                                   - Track dependencies"
        echo "  clean                                   - Clean unused packages"
        echo "  install <requirements_file>             - Install Python packages"
        ;;
esac
EOF
    
    chmod +x "$PROJECT_ROOT/package-dev.sh"
    
    log "✅ Development shortcuts created"
}

# Generate development documentation
generate_docs() {
    log "📚 Generating development documentation..."
    
    cat > "$PACKAGES_DIR/README.md" << 'EOF'
# Package Management System - Development Environment

This package management system provides automated package downloading, dependency tracking, and deployment capabilities for the Creatio AI Knowledge Hub.

## Quick Start

### Node.js Packages
```bash
# Download a package
./package-dev.sh download lodash latest npm

# Track dependencies
./package-dev.sh track
```

### Python Packages
```bash
# Install from requirements
./package-dev.sh install requirements.txt

# Download specific package
python3 packages/scripts/download-packages.py download requests latest pypi
```

### Dependency Management
```bash
# Analyze dependencies
node packages/scripts/dependency-tracker.js analyze

# Generate security report
node packages/scripts/dependency-tracker.js security

# Export dependency graph
node packages/scripts/dependency-tracker.js export json
```

## Development Features

- 🔄 Hot reload enabled
- 🐛 Debug mode active
- 📦 Auto-update packages
- 🧪 Development dependencies included
- 📊 Detailed logging and monitoring

## Directory Structure

```
packages/
├── local/          # Local packages
├── remote/         # Downloaded packages
├── cache/          # Package cache
├── scripts/        # Management scripts
└── deploy/         # Deployment configurations
```

## Configuration

Development settings are stored in:
- `packages/package-registry.json` - Main configuration
- `packages/deploy/environments/development/config.json` - Environment config

## Support

For issues and questions, check the main project documentation or create an issue.
EOF
    
    log "✅ Development documentation generated"
}

# Main deployment function
main() {
    log "🎯 Starting development environment deployment..."
    
    validate_environment
    install_dependencies
    setup_local_packages
    configure_development
    start_development_services
    run_tests
    create_shortcuts
    generate_docs
    
    log "🎉 Development environment deployment completed successfully!"
    log ""
    log "Next steps:"
    log "1. Use './package-dev.sh' for package management"
    log "2. Check 'packages/README.md' for detailed documentation"
    log "3. Monitor dependencies with: node packages/scripts/dependency-tracker.js analyze"
    log ""
    log "Happy coding! 🚀"
}

# Run main function
main "$@"
