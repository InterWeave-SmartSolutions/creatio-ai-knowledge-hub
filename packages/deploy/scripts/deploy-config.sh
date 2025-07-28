#!/bin/bash

# Common Deployment Configuration
# Shared configuration variables and functions for all deployment environments

# Project information
PROJECT_NAME="creatio-ai-knowledge-hub"
PROJECT_VERSION="1.0.0"
ORGANIZATION="creatio-development-team"

# Common paths
export SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
export PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
export PACKAGES_DIR="${PACKAGES_DIR:-$PROJECT_ROOT/packages}"
export DEPLOY_DIR="${DEPLOY_DIR:-$PACKAGES_DIR/deploy}"

# Node.js configuration
NODE_MIN_VERSION="18"
NPM_MIN_VERSION="9"

# Python configuration
PYTHON_MIN_VERSION="3.8"
PIP_MIN_VERSION="20"

# Package registry configuration
DEFAULT_NPM_REGISTRY="https://registry.npmjs.org/"
DEFAULT_PYPI_REGISTRY="https://pypi.org/simple/"
DEFAULT_CREATIO_REGISTRY="https://marketplace.creatio.com/"

# Cache configuration
DEFAULT_CACHE_TTL_DEV=3600      # 1 hour for development
DEFAULT_CACHE_TTL_PROD=86400    # 24 hours for production
MAX_CACHE_SIZE_MB=1024          # 1GB maximum cache size

# Security configuration
REQUIRE_HTTPS=true
VERIFY_SIGNATURES=true
SECURITY_SCAN_ENABLED=true
VULNERABILITY_SCAN_ENABLED=true

# Logging configuration
LOG_RETENTION_DAYS=30
MAX_LOG_SIZE_MB=10
MAX_LOG_FILES=5

# Performance configuration
CONNECTION_TIMEOUT=30000        # 30 seconds
REQUEST_TIMEOUT=60000          # 60 seconds
MAX_CONCURRENT_DOWNLOADS=5
RATE_LIMIT_RPM=30              # Requests per minute

# Environment-specific settings
case "${DEPLOY_ENV:-development}" in
    "development")
        DEBUG_MODE=true
        HOT_RELOAD=true
        AUTO_UPDATE=true
        INSTALL_DEV_DEPS=true
        SECURITY_SCAN_LEVEL="basic"
        LOG_LEVEL="debug"
        CACHE_TTL=$DEFAULT_CACHE_TTL_DEV
        ;;
    "staging")
        DEBUG_MODE=false
        HOT_RELOAD=false
        AUTO_UPDATE=false
        INSTALL_DEV_DEPS=false
        SECURITY_SCAN_LEVEL="standard"
        LOG_LEVEL="info"
        CACHE_TTL=$DEFAULT_CACHE_TTL_PROD
        ;;
    "production")
        DEBUG_MODE=false
        HOT_RELOAD=false
        AUTO_UPDATE=false
        INSTALL_DEV_DEPS=false
        SECURITY_SCAN_LEVEL="strict"
        LOG_LEVEL="error"
        CACHE_TTL=$DEFAULT_CACHE_TTL_PROD
        ;;
    *)
        echo "Warning: Unknown environment '${DEPLOY_ENV}', using development defaults"
        DEPLOY_ENV="development"
        DEBUG_MODE=true
        HOT_RELOAD=true
        AUTO_UPDATE=true
        INSTALL_DEV_DEPS=true
        SECURITY_SCAN_LEVEL="basic"
        LOG_LEVEL="debug"
        CACHE_TTL=$DEFAULT_CACHE_TTL_DEV
        ;;
esac

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Common utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [ "$DEBUG_MODE" = true ]; then
        echo -e "${PURPLE}[DEBUG]${NC} $1"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check version compatibility
check_version() {
    local current_version="$1"
    local required_version="$2"
    local package_name="$3"
    
    if [ -z "$current_version" ] || [ -z "$required_version" ]; then
        log_error "Version check failed for $package_name: missing version information"
        return 1
    fi
    
    # Simple version comparison (works for major.minor format)
    if [ "$(printf '%s\n' "$required_version" "$current_version" | sort -V | head -n1)" = "$required_version" ]; then
        return 0
    else
        log_error "$package_name version $current_version is below required version $required_version"
        return 1
    fi
}

# Validate system requirements
validate_system_requirements() {
    local errors=0
    
    log_info "Validating system requirements for $DEPLOY_ENV environment..."
    
    # Check Node.js
    if command_exists node; then
        local node_version=$(node --version | sed 's/v//')
        if check_version "$node_version" "$NODE_MIN_VERSION" "Node.js"; then
            log_success "Node.js $node_version (>= $NODE_MIN_VERSION required)"
        else
            errors=$((errors + 1))
        fi
    else
        log_error "Node.js is not installed"
        errors=$((errors + 1))
    fi
    
    # Check npm
    if command_exists npm; then
        local npm_version=$(npm --version)
        if check_version "$npm_version" "$NPM_MIN_VERSION" "npm"; then
            log_success "npm $npm_version (>= $NPM_MIN_VERSION required)"
        else
            errors=$((errors + 1))
        fi
    else
        log_error "npm is not installed"
        errors=$((errors + 1))
    fi
    
    # Check Python
    if command_exists python3; then
        local python_version=$(python3 --version 2>&1 | awk '{print $2}')
        if check_version "$python_version" "$PYTHON_MIN_VERSION" "Python"; then
            log_success "Python $python_version (>= $PYTHON_MIN_VERSION required)"
        else
            errors=$((errors + 1))
        fi
    else
        log_error "Python 3 is not installed"
        errors=$((errors + 1))
    fi
    
    # Check pip
    if command_exists pip; then
        local pip_version=$(pip --version | awk '{print $2}')
        if check_version "$pip_version" "$PIP_MIN_VERSION" "pip"; then
            log_success "pip $pip_version (>= $PIP_MIN_VERSION required)"
        else
            errors=$((errors + 1))
        fi
    else
        log_error "pip is not installed"
        errors=$((errors + 1))
    fi
    
    # Check system resources for production
    if [ "$DEPLOY_ENV" = "production" ]; then
        # Check available memory
        if command_exists free; then
            local available_memory=$(free -m | awk 'NR==2{printf "%d", $7}')
            if [ "$available_memory" -lt 1024 ]; then
                log_error "Insufficient memory: ${available_memory}MB available, 1024MB required"
                errors=$((errors + 1))
            else
                log_success "Memory: ${available_memory}MB available"
            fi
        fi
        
        # Check available disk space
        local available_disk=$(df "$PROJECT_ROOT" | tail -1 | awk '{print int($4/1024)}')
        if [ "$available_disk" -lt 5120 ]; then # 5GB in MB
            log_error "Insufficient disk space: ${available_disk}MB available, 5120MB required"
            errors=$((errors + 1))
        else
            log_success "Disk space: ${available_disk}MB available"
        fi
    fi
    
    return $errors
}

# Create directory structure
create_directory_structure() {
    log_info "Creating directory structure..."
    
    local directories=(
        "$PACKAGES_DIR/local/core"
        "$PACKAGES_DIR/local/plugins"
        "$PACKAGES_DIR/local/utilities"
        "$PACKAGES_DIR/local/themes"
        "$PACKAGES_DIR/local/templates"
        "$PACKAGES_DIR/local/integrations"
        "$PACKAGES_DIR/remote/npm"
        "$PACKAGES_DIR/remote/python"
        "$PACKAGES_DIR/remote/creatio"
        "$PACKAGES_DIR/cache"
        "$PACKAGES_DIR/logs"
        "$PACKAGES_DIR/deploy/environments/$DEPLOY_ENV"
        "$PACKAGES_DIR/scripts"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_debug "Created directory: $dir"
        fi
    done
    
    log_success "Directory structure created"
}

# Set file permissions
set_file_permissions() {
    log_info "Setting file permissions for $DEPLOY_ENV environment..."
    
    if [ "$DEPLOY_ENV" = "production" ]; then
        # Production: More restrictive permissions
        chmod 755 "$PACKAGES_DIR/local" "$PACKAGES_DIR/remote" "$PACKAGES_DIR/cache"
        chmod 700 "$PACKAGES_DIR/deploy/environments/production"
        chmod 640 "$PACKAGES_DIR/package-registry.json" 2>/dev/null || true
        find "$PACKAGES_DIR/scripts" -name "*.sh" -exec chmod 750 {} \;
        find "$PACKAGES_DIR/scripts" -name "*.js" -exec chmod 640 {} \;
        find "$PACKAGES_DIR/scripts" -name "*.py" -exec chmod 640 {} \;
    else
        # Development/Staging: More permissive permissions
        chmod 755 "$PACKAGES_DIR/local" "$PACKAGES_DIR/remote" "$PACKAGES_DIR/cache"
        chmod 755 "$PACKAGES_DIR/deploy/environments/$DEPLOY_ENV"
        chmod 644 "$PACKAGES_DIR/package-registry.json" 2>/dev/null || true
        find "$PACKAGES_DIR/scripts" -name "*.sh" -exec chmod 755 {} \;
        find "$PACKAGES_DIR/scripts" -name "*.js" -exec chmod 644 {} \;
        find "$PACKAGES_DIR/scripts" -name "*.py" -exec chmod 644 {} \;
    fi
    
    log_success "File permissions set for $DEPLOY_ENV environment"
}

# Generate deployment summary
generate_deployment_summary() {
    local environment="$1"
    local status="$2"
    
    echo ""
    echo "======================================"
    echo "Deployment Summary"
    echo "======================================"
    echo "Project: $PROJECT_NAME"
    echo "Version: $PROJECT_VERSION"
    echo "Environment: $environment"
    echo "Status: $status"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "Configuration:"
    echo "- Debug Mode: $DEBUG_MODE"
    echo "- Hot Reload: $HOT_RELOAD"
    echo "- Auto Update: $AUTO_UPDATE"
    echo "- Dev Dependencies: $INSTALL_DEV_DEPS"
    echo "- Security Scan: $SECURITY_SCAN_LEVEL"
    echo "- Log Level: $LOG_LEVEL"
    echo "- Cache TTL: ${CACHE_TTL}s"
    echo ""
    echo "Paths:"
    echo "- Project Root: $PROJECT_ROOT"
    echo "- Packages Dir: $PACKAGES_DIR"
    echo "- Deploy Dir: $DEPLOY_DIR"
    echo ""
    echo "======================================"
}

# Initialize configuration
initialize_config() {
    log_info "Initializing deployment configuration..."
    
    # Export all configuration variables
    export PROJECT_NAME PROJECT_VERSION ORGANIZATION
    export NODE_MIN_VERSION NPM_MIN_VERSION PYTHON_MIN_VERSION PIP_MIN_VERSION
    export DEFAULT_NPM_REGISTRY DEFAULT_PYPI_REGISTRY DEFAULT_CREATIO_REGISTRY
    export DEFAULT_CACHE_TTL_DEV DEFAULT_CACHE_TTL_PROD MAX_CACHE_SIZE_MB
    export REQUIRE_HTTPS VERIFY_SIGNATURES SECURITY_SCAN_ENABLED VULNERABILITY_SCAN_ENABLED
    export LOG_RETENTION_DAYS MAX_LOG_SIZE_MB MAX_LOG_FILES
    export CONNECTION_TIMEOUT REQUEST_TIMEOUT MAX_CONCURRENT_DOWNLOADS RATE_LIMIT_RPM
    export DEBUG_MODE HOT_RELOAD AUTO_UPDATE INSTALL_DEV_DEPS SECURITY_SCAN_LEVEL LOG_LEVEL CACHE_TTL
    
    log_success "Configuration initialized for $DEPLOY_ENV environment"
}

# Auto-initialize when sourced
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    initialize_config
fi
