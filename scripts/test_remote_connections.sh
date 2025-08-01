#!/bin/bash

# Creatio Remote Connection Testing and Troubleshooting Script
# Tests connections to mkpdev-interweave.creatio.com and other environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$PROJECT_ROOT/config/remote_connections.yaml"
CONNECTION_MANAGER="$SCRIPT_DIR/utilities/remote_connection_manager.py"
CREDENTIAL_MANAGER="$SCRIPT_DIR/utilities/credential_manager.py"
LOG_FILE="$PROJECT_ROOT/logs/connection_test.log"

# Create logs directory
mkdir -p "$(dirname "$LOG_FILE")"

# Functions
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    log "SUCCESS: $1"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    log "ERROR: $1"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    log "WARNING: $1"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
    log "INFO: $1"
}

check_dependencies() {
    print_header "Checking Dependencies"
    
    # Check Python
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        print_success "Python found: $python_version"
    else
        print_error "Python 3 not found. Please install Python 3."
        exit 1
    fi
    
    # Check required Python packages
    local required_packages=("requests" "pyyaml" "keyring")
    for package in "${required_packages[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            print_success "Python package '$package' found"
        else
            print_error "Python package '$package' not found. Install with: pip install $package"
            exit 1
        fi
    done
    
    # Check curl
    if command -v curl &> /dev/null; then
        print_success "curl found"
    else
        print_warning "curl not found. Some network tests may not work."
    fi
    
    # Check openssl
    if command -v openssl &> /dev/null; then
        openssl_version=$(openssl version)
        print_success "OpenSSL found: $openssl_version"
    else
        print_warning "OpenSSL not found. SSL certificate checks may not work."
    fi
}

check_configuration() {
    print_header "Checking Configuration Files"
    
    if [[ -f "$CONFIG_FILE" ]]; then
        print_success "Configuration file found: $CONFIG_FILE"
        
        # Validate YAML syntax
        if python3 -c "import yaml; yaml.safe_load(open('$CONFIG_FILE'))" 2>/dev/null; then
            print_success "Configuration file is valid YAML"
        else
            print_error "Configuration file has invalid YAML syntax"
            return 1
        fi
    else
        print_error "Configuration file not found: $CONFIG_FILE"
        return 1
    fi
    
    if [[ -f "$CONNECTION_MANAGER" ]]; then
        print_success "Connection manager script found"
    else
        print_error "Connection manager script not found: $CONNECTION_MANAGER"
        return 1
    fi
    
    if [[ -f "$CREDENTIAL_MANAGER" ]]; then
        print_success "Credential manager script found"
    else
        print_error "Credential manager script not found: $CREDENTIAL_MANAGER"
        return 1
    fi
}

test_dns_resolution() {
    print_header "Testing DNS Resolution"
    
    local hosts=("mkpdev-interweave.creatio.com" "staging-mkpdev-interweave.creatio.com")
    
    for host in "${hosts[@]}"; do
        if nslookup "$host" &> /dev/null; then
            ip=$(nslookup "$host" | grep -A1 "Name:" | grep "Address:" | awk '{print $2}' | head -1)
            print_success "DNS resolution for $host: $ip"
        else
            print_error "DNS resolution failed for $host"
        fi
    done
}

test_network_connectivity() {
    print_header "Testing Network Connectivity"
    
    local test_urls=("https://mkpdev-interweave.creatio.com" "https://staging-mkpdev-interweave.creatio.com")
    
    for url in "${test_urls[@]}"; do
        print_info "Testing connectivity to $url"
        
        if command -v curl &> /dev/null; then
            # Test with curl
            if curl -s --connect-timeout 10 --max-time 30 -I "$url" &> /dev/null; then
                status_code=$(curl -s --connect-timeout 10 --max-time 30 -I "$url" | head -n1 | cut -d' ' -f2)
                print_success "HTTP connectivity to $url (Status: $status_code)"
            else
                print_error "HTTP connectivity failed to $url"
            fi
        else
            # Fallback to wget
            if wget --spider --timeout=30 "$url" &> /dev/null; then
                print_success "HTTP connectivity to $url"
            else
                print_error "HTTP connectivity failed to $url"
            fi
        fi
    done
}

test_ssl_certificates() {
    print_header "Testing SSL Certificates"
    
    local hosts=("mkpdev-interweave.creatio.com:443" "staging-mkpdev-interweave.creatio.com:443")
    
    if command -v openssl &> /dev/null; then
        for host in "${hosts[@]}"; do
            print_info "Checking SSL certificate for $host"
            
            cert_info=$(echo | openssl s_client -servername "${host%:*}" -connect "$host" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
            
            if [[ $? -eq 0 ]]; then
                not_after=$(echo "$cert_info" | grep "notAfter" | cut -d= -f2)
                print_success "SSL certificate valid for $host (Expires: $not_after)"
            else
                print_error "SSL certificate check failed for $host"
            fi
        done
    else
        print_warning "OpenSSL not available, skipping SSL certificate checks"
    fi
}

check_credentials() {
    print_header "Checking Stored Credentials"
    
    if python3 "$CREDENTIAL_MANAGER" list &> /dev/null; then
        python3 "$CREDENTIAL_MANAGER" list
    else
        print_error "Failed to check stored credentials"
    fi
}

test_authentication() {
    print_header "Testing Authentication"
    
    local environments=("production" "staging" "development")
    
    for env in "${environments[@]}"; do
        print_info "Testing authentication for $env environment"
        
        if python3 "$CONNECTION_MANAGER" test --environment "$env" &> /dev/null; then
            print_success "Authentication test passed for $env"
        else
            print_error "Authentication test failed for $env"
        fi
    done
}

test_package_operations() {
    print_header "Testing Package Operations"
    
    local environments=("production" "staging")
    
    for env in "${environments[@]}"; do
        print_info "Testing package listing for $env environment"
        
        if python3 "$CONNECTION_MANAGER" list --environment "$env" &> /dev/null; then
            package_count=$(python3 "$CONNECTION_MANAGER" list --environment "$env" 2>/dev/null | python3 -c "import json, sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "unknown")
            print_success "Package listing successful for $env ($package_count packages)"
        else
            print_error "Package listing failed for $env"
        fi
    done
}

run_diagnostics() {
    print_header "Running Network Diagnostics"
    
    # Test internet connectivity
    if ping -c 1 8.8.8.8 &> /dev/null; then
        print_success "Internet connectivity available"
    else
        print_error "No internet connectivity"
    fi
    
    # Check proxy settings
    if [[ -n "$HTTP_PROXY" || -n "$HTTPS_PROXY" ]]; then
        print_info "Proxy settings detected:"
        [[ -n "$HTTP_PROXY" ]] && echo "  HTTP_PROXY: $HTTP_PROXY"
        [[ -n "$HTTPS_PROXY" ]] && echo "  HTTPS_PROXY: $HTTPS_PROXY"
    else
        print_info "No proxy settings detected"
    fi
    
    # Check system time
    current_time=$(date)
    print_info "System time: $current_time"
    
    # Check disk space
    disk_usage=$(df -h . | tail -1 | awk '{print $5}')
    print_info "Disk usage in current directory: $disk_usage"
}

generate_report() {
    print_header "Generating Connection Report"
    
    local report_file="$PROJECT_ROOT/logs/connection_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "Creatio Remote Connection Test Report"
        echo "Generated: $(date)"
        echo "======================================="
        echo
        
        echo "Configuration:"
        echo "- Config file: $CONFIG_FILE"
        echo "- Log file: $LOG_FILE"
        echo
        
        echo "Test Results:"
        echo "- Dependencies: See log for details"
        echo "- DNS Resolution: See log for details"
        echo "- Network Connectivity: See log for details"
        echo "- SSL Certificates: See log for details"
        echo "- Authentication: See log for details"
        echo "- Package Operations: See log for details"
        echo
        
        echo "System Information:"
        echo "- OS: $(uname -a)"
        echo "- Python: $(python3 --version 2>&1)"
        echo "- Current directory: $(pwd)"
        echo "- User: $(whoami)"
        echo
        
        echo "Environment Variables:"
        env | grep -E "(PROXY|CREATIO)" | sort
        
    } > "$report_file"
    
    print_success "Report generated: $report_file"
}

show_troubleshooting_tips() {
    print_header "Troubleshooting Tips"
    
    cat << EOF
Common Issues and Solutions:

1. DNS Resolution Failures:
   - Check your network connection
   - Try using a different DNS server (8.8.8.8, 1.1.1.1)
   - Check if you're behind a corporate firewall

2. SSL Certificate Errors:
   - Ensure system time is correct
   - Update your CA certificates bundle
   - Check if corporate proxy is intercepting SSL

3. Authentication Failures:
   - Verify credentials with: python3 $CREDENTIAL_MANAGER list
   - Re-setup credentials with: python3 $CREDENTIAL_MANAGER setup production
   - Check if credentials have expired

4. Connection Timeouts:
   - Check proxy settings in $CONFIG_FILE
   - Increase timeout values in configuration
   - Test with a different network connection

5. Package Operation Failures:
   - Ensure you have proper permissions
   - Check API endpoint URLs in configuration
   - Verify the remote service is operational

For more help, check the log file: $LOG_FILE
EOF
}

# Main execution
main() {
    local test_type="all"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --quick     Run quick connectivity tests only"
                echo "  --auth      Test authentication only"
                echo "  --network   Test network connectivity only"
                echo "  --all       Run all tests (default)"
                echo "  --report    Generate detailed report"
                echo "  --help      Show this help message"
                exit 0
                ;;
            --quick)
                test_type="quick"
                shift
                ;;
            --auth)
                test_type="auth"
                shift
                ;;
            --network)
                test_type="network"
                shift
                ;;
            --all)
                test_type="all"
                shift
                ;;
            --report)
                test_type="report"
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    print_header "Creatio Remote Connection Tester"
    log "Starting connection tests (type: $test_type)"
    
    case $test_type in
        "quick")
            check_dependencies
            test_dns_resolution
            test_network_connectivity
            ;;
        "auth")
            check_dependencies
            check_configuration
            check_credentials
            test_authentication
            ;;
        "network")
            test_dns_resolution
            test_network_connectivity
            test_ssl_certificates
            run_diagnostics
            ;;
        "report")
            check_dependencies
            check_configuration
            test_dns_resolution
            test_network_connectivity
            test_ssl_certificates
            check_credentials
            test_authentication
            test_package_operations
            run_diagnostics
            generate_report
            ;;
        "all"|*)
            check_dependencies
            check_configuration
            test_dns_resolution
            test_network_connectivity
            test_ssl_certificates
            check_credentials
            test_authentication
            test_package_operations
            run_diagnostics
            show_troubleshooting_tips
            ;;
    esac
    
    print_header "Connection Testing Complete"
    log "Connection tests completed"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
