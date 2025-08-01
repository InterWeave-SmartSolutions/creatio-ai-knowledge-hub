#!/bin/bash
set -e

# Deployment script for Creatio AI Knowledge Hub
# Usage: ./deploy.sh <environment> [image_uri]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check required tools
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local required_tools=("docker" "docker-compose" "curl")
    
    for tool in "${required_tools[@]}"; do
        if ! command_exists "$tool"; then
            log_error "$tool is not installed or not in PATH"
            exit 1
        fi
    done
    
    log_success "All prerequisites are available"
}

# Function to validate environment
validate_environment() {
    local env=$1
    local valid_envs=("development" "testing" "staging" "production")
    
    if [[ ! " ${valid_envs[@]} " =~ " ${env} " ]]; then
        log_error "Invalid environment: $env"
        log_error "Valid environments: ${valid_envs[*]}"
        exit 1
    fi
}

# Function to load environment configuration
load_environment_config() {
    local env=$1
    local config_file="${PROJECT_ROOT}/config/environments/${env}.env"
    
    if [[ -f "$config_file" ]]; then
        log_info "Loading environment configuration from $config_file"
        # Export environment variables from config file
        set -a
        source "$config_file"
        set +a
    else
        log_warning "No environment configuration file found at $config_file"
    fi
}

# Function to backup current deployment
backup_current_deployment() {
    local env=$1
    local backup_dir="${PROJECT_ROOT}/backups/deployment_$(date +%Y%m%d_%H%M%S)"
    
    log_info "Creating backup of current deployment..."
    
    mkdir -p "$backup_dir"
    
    # Backup database if it exists
    if [[ -f "${PROJECT_ROOT}/ai_knowledge_hub/knowledge_hub.db" ]]; then
        cp "${PROJECT_ROOT}/ai_knowledge_hub/knowledge_hub.db" "$backup_dir/"
        log_info "Database backed up"
    fi
    
    # Backup configuration files
    if [[ -d "${PROJECT_ROOT}/config" ]]; then
        cp -r "${PROJECT_ROOT}/config" "$backup_dir/"
        log_info "Configuration backed up"
    fi
    
    log_success "Backup created at $backup_dir"
}

# Function to deploy to development environment
deploy_development() {
    log_info "Deploying to development environment..."
    
    cd "$PROJECT_ROOT"
    
    # Build and start services
    docker-compose -f docker-compose.yml build
    docker-compose -f docker-compose.yml up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Run database migrations/initialization if needed
    docker-compose exec -T app python -c "
from ai_knowledge_hub_integration import AIKnowledgeHubIntegrator
integrator = AIKnowledgeHubIntegrator()
integrator.initialize_database()
print('Database initialized successfully')
" || log_warning "Database initialization failed or already exists"
    
    log_success "Development deployment completed"
}

# Function to deploy to staging environment
deploy_staging() {
    local image_uri=$1
    
    log_info "Deploying to staging environment..."
    
    # Update staging environment with new image
    if [[ -n "$image_uri" ]]; then
        log_info "Using image: $image_uri"
        export IMAGE_URI="$image_uri"
    fi
    
    cd "$PROJECT_ROOT"
    
    # Deploy using staging configuration
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml pull
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
    
    log_success "Staging deployment completed"
}

# Function to deploy to production environment
deploy_production() {
    local image_uri=$1
    
    log_info "Deploying to production environment..."
    
    # Additional safety checks for production
    if [[ -z "$image_uri" ]]; then
        log_error "Image URI is required for production deployment"
        exit 1
    fi
    
    # Confirm production deployment
    echo -n "Are you sure you want to deploy to production? (yes/no): "
    read -r confirm
    if [[ "$confirm" != "yes" ]]; then
        log_info "Production deployment cancelled"
        exit 0
    fi
    
    log_info "Using image: $image_uri"
    export IMAGE_URI="$image_uri"
    
    cd "$PROJECT_ROOT"
    
    # Deploy using production configuration
    docker-compose -f docker-compose.yml -f docker-compose.production.yml pull
    docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d --no-deps app
    
    # Rolling update strategy for zero-downtime deployment
    log_info "Performing rolling update..."
    docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d
    
    log_success "Production deployment completed"
}

# Function to run post-deployment checks
run_post_deployment_checks() {
    local env=$1
    
    log_info "Running post-deployment checks..."
    
    # Health check
    local health_url="http://localhost:8000/health"
    if [[ "$env" == "production" ]]; then
        health_url="${PRODUCTION_URL:-https://creatio-ai-hub.example.com}/health"
    elif [[ "$env" == "staging" ]]; then
        health_url="${STAGING_URL:-https://staging.creatio-ai-hub.example.com}/health"
    fi
    
    log_info "Checking health endpoint: $health_url"
    
    for i in {1..30}; do
        if curl -f -s "$health_url" > /dev/null; then
            log_success "Health check passed"
            break
        else
            log_info "Health check attempt $i/30 failed, retrying in 10 seconds..."
            sleep 10
        fi
        
        if [[ $i -eq 30 ]]; then
            log_error "Health check failed after 30 attempts"
            exit 1
        fi
    done
    
    # API endpoints check
    log_info "Testing API endpoints..."
    
    local api_base_url="http://localhost:8000/api/v1"
    if [[ "$env" == "production" ]]; then
        api_base_url="${PRODUCTION_URL:-https://creatio-ai-hub.example.com}/api/v1"
    elif [[ "$env" == "staging" ]]; then
        api_base_url="${STAGING_URL:-https://staging.creatio-ai-hub.example.com}/api/v1"
    fi
    
    # Test search endpoint
    if curl -f -s "${api_base_url}/search?query=test&limit=1" > /dev/null; then
        log_success "Search API endpoint is working"
    else
        log_warning "Search API endpoint test failed"
    fi
    
    # Test commands endpoint
    if curl -f -s "${api_base_url}/commands?limit=1" > /dev/null; then
        log_success "Commands API endpoint is working"
    else
        log_warning "Commands API endpoint test failed"
    fi
    
    log_success "Post-deployment checks completed"
}

# Function to rollback deployment
rollback_deployment() {
    local env=$1
    
    log_warning "Rolling back deployment for environment: $env"
    
    cd "$PROJECT_ROOT"
    
    case $env in
        "development")
            docker-compose -f docker-compose.yml down
            ;;
        "staging")
            docker-compose -f docker-compose.yml -f docker-compose.staging.yml down
            ;;
        "production")
            docker-compose -f docker-compose.yml -f docker-compose.production.yml down
            ;;
        *)
            log_error "Unknown environment for rollback: $env"
            exit 1
            ;;
    esac
    
    # Restore from latest backup if available
    local latest_backup=$(ls -t "${PROJECT_ROOT}/backups/deployment_"* 2>/dev/null | head -1)
    if [[ -n "$latest_backup" ]]; then
        log_info "Restoring from backup: $latest_backup"
        if [[ -f "$latest_backup/knowledge_hub.db" ]]; then
            cp "$latest_backup/knowledge_hub.db" "${PROJECT_ROOT}/ai_knowledge_hub/"
            log_success "Database restored from backup"
        fi
    else
        log_warning "No backup found for rollback"
    fi
    
    log_success "Rollback completed"
}

# Main deployment function
main() {
    local environment=$1
    local image_uri=$2
    
    if [[ -z "$environment" ]]; then
        log_error "Usage: $0 <environment> [image_uri]"
        log_error "Environments: development, testing, staging, production"
        exit 1
    fi
    
    # Validate inputs
    validate_environment "$environment"
    check_prerequisites
    
    # Load environment configuration
    load_environment_config "$environment"
    
    # Create backup (except for development)
    if [[ "$environment" != "development" ]]; then
        backup_current_deployment "$environment"
    fi
    
    # Deploy based on environment
    case $environment in
        "development")
            deploy_development
            ;;
        "testing")
            deploy_development  # Use same as development for now
            ;;
        "staging")
            deploy_staging "$image_uri"
            ;;
        "production")
            deploy_production "$image_uri"
            ;;
        *)
            log_error "Deployment not implemented for environment: $environment"
            exit 1
            ;;
    esac
    
    # Run post-deployment checks
    run_post_deployment_checks "$environment"
    
    log_success "Deployment to $environment completed successfully!"
}

# Handle script termination
trap 'log_error "Deployment interrupted"; exit 1' INT TERM

# Run main function with all arguments
main "$@"
