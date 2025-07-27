#!/bin/bash
set -e

# Smoke tests for Creatio AI Knowledge Hub
# Usage: ./smoke-tests.sh <environment>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0
FAILED_TESTS=()

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

# Test result functions
test_passed() {
    local test_name=$1
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_success "✓ $test_name"
}

test_failed() {
    local test_name=$1
    local error_msg=$2
    TESTS_FAILED=$((TESTS_FAILED + 1))
    FAILED_TESTS+=("$test_name: $error_msg")
    log_error "✗ $test_name - $error_msg"
}

# Function to make HTTP request with timeout
make_request() {
    local url=$1
    local expected_status=${2:-200}
    local timeout=${3:-10}
    
    local response
    local status_code
    
    response=$(curl -s -w "\n%{http_code}" --max-time "$timeout" "$url" 2>/dev/null || echo -e "\n000")
    status_code=$(echo "$response" | tail -n1)
    
    if [[ "$status_code" == "$expected_status" ]]; then
        return 0
    else
        return 1
    fi
}

# Function to test API endpoint with JSON response
test_api_endpoint() {
    local test_name=$1
    local url=$2
    local expected_status=${3:-200}
    
    if make_request "$url" "$expected_status"; then
        # Additional JSON validation
        local response_body
        response_body=$(curl -s --max-time 10 "$url" 2>/dev/null)
        
        if echo "$response_body" | python3 -m json.tool >/dev/null 2>&1; then
            test_passed "$test_name"
        else
            test_failed "$test_name" "Invalid JSON response"
        fi
    else
        test_failed "$test_name" "HTTP request failed or wrong status code"
    fi
}

# Function to set base URL based on environment
set_base_url() {
    local environment=$1
    
    case $environment in
        "development"|"testing")
            BASE_URL="http://localhost:8000"
            ;;
        "staging")
            BASE_URL="${STAGING_URL:-https://staging.creatio-ai-hub.example.com}"
            ;;
        "production")
            BASE_URL="${PRODUCTION_URL:-https://creatio-ai-hub.example.com}"
            ;;
        *)
            log_error "Unknown environment: $environment"
            exit 1
            ;;
    esac
    
    log_info "Testing against: $BASE_URL"
}

# Basic connectivity tests
test_basic_connectivity() {
    log_info "Running basic connectivity tests..."
    
    # Test if the application is responding
    if make_request "$BASE_URL" 200 30; then
        test_passed "Application is responding"
    else
        test_failed "Application connectivity" "Service is not responding"
        return 1
    fi
    
    # Test health endpoint
    if make_request "$BASE_URL/health" 200; then
        test_passed "Health endpoint"
    else
        test_failed "Health endpoint" "Health check failed"
    fi
}

# API endpoint tests
test_api_endpoints() {
    log_info "Running API endpoint tests..."
    
    local api_base="$BASE_URL/api/v1"
    
    # Test search endpoint with basic query
    test_api_endpoint "Search API - basic query" "$api_base/search?query=test&limit=5"
    
    # Test search endpoint with content type filter
    test_api_endpoint "Search API - content type filter" "$api_base/search?query=creatio&content_type=all&limit=10"
    
    # Test commands endpoint
    test_api_endpoint "Commands API - all commands" "$api_base/commands"
    
    # Test commands endpoint with category filter
    test_api_endpoint "Commands API - category filter" "$api_base/commands?category=Development"
    
    # Test commands endpoint with search term
    test_api_endpoint "Commands API - search term" "$api_base/commands?search_term=Create"
}

# Database connectivity tests
test_database_functionality() {
    log_info "Running database functionality tests..."
    
    # Test that search returns some results (assuming there's test data)
    local search_response
    search_response=$(curl -s --max-time 10 "$BASE_URL/api/v1/search?query=creatio&limit=1" 2>/dev/null)
    
    if echo "$search_response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'results' in data and isinstance(data['results'], list):
        print('OK')
    else:
        print('FAIL')
except:
    print('FAIL')
" | grep -q "OK"; then
        test_passed "Database search functionality"
    else
        test_failed "Database search functionality" "Search results format invalid"
    fi
    
    # Test commands retrieval
    local commands_response
    commands_response=$(curl -s --max-time 10 "$BASE_URL/api/v1/commands?limit=1" 2>/dev/null)
    
    if echo "$commands_response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'commands' in data and isinstance(data['commands'], list):
        print('OK')
    else:
        print('FAIL')
except:
    print('FAIL')
" | grep -q "OK"; then
        test_passed "Database commands functionality"
    else
        test_failed "Database commands functionality" "Commands results format invalid"
    fi
}

# Performance tests (basic response time checks)
test_basic_performance() {
    log_info "Running basic performance tests..."
    
    # Test response time for health endpoint (should be very fast)
    local start_time
    local end_time
    local response_time
    
    start_time=$(date +%s%N)
    if make_request "$BASE_URL/health" 200 5; then
        end_time=$(date +%s%N)
        response_time=$(((end_time - start_time) / 1000000)) # Convert to milliseconds
        
        if [[ $response_time -lt 1000 ]]; then # Less than 1 second
            test_passed "Health endpoint response time (${response_time}ms)"
        else
            test_failed "Health endpoint response time" "Too slow: ${response_time}ms"
        fi
    else
        test_failed "Health endpoint performance" "Request failed"
    fi
    
    # Test response time for search API
    start_time=$(date +%s%N)
    if make_request "$BASE_URL/api/v1/search?query=test&limit=5" 200 10; then
        end_time=$(date +%s%N)
        response_time=$(((end_time - start_time) / 1000000))
        
        if [[ $response_time -lt 5000 ]]; then # Less than 5 seconds
            test_passed "Search API response time (${response_time}ms)"
        else
            test_failed "Search API response time" "Too slow: ${response_time}ms"
        fi
    else
        test_failed "Search API performance" "Request failed"
    fi
}

# Security tests (basic checks)
test_basic_security() {
    log_info "Running basic security tests..."
    
    # Test that server headers don't reveal too much information
    local server_header
    server_header=$(curl -s -I "$BASE_URL" | grep -i "server:" || echo "")
    
    if [[ -z "$server_header" ]] || [[ ! "$server_header" =~ "uvicorn" ]]; then
        test_passed "Server header security"
    else
        test_failed "Server header security" "Server information exposed: $server_header"
    fi
    
    # Test for common security headers
    local headers
    headers=$(curl -s -I "$BASE_URL")
    
    if echo "$headers" | grep -i "x-content-type-options" >/dev/null; then
        test_passed "X-Content-Type-Options header present"
    else
        test_failed "X-Content-Type-Options header" "Security header missing"
    fi
    
    # Test for HTTPS in production
    if [[ "$1" == "production" ]] && [[ "$BASE_URL" =~ ^https:// ]]; then
        test_passed "HTTPS enabled in production"
    elif [[ "$1" == "production" ]]; then
        test_failed "HTTPS in production" "Production should use HTTPS"
    else
        log_info "Skipping HTTPS check for non-production environment"
    fi
}

# Error handling tests
test_error_handling() {
    log_info "Running error handling tests..."
    
    # Test 404 for non-existent endpoint
    if make_request "$BASE_URL/api/v1/nonexistent" 404; then
        test_passed "404 error handling"
    else
        test_failed "404 error handling" "Should return 404 for non-existent endpoints"
    fi
    
    # Test validation error for invalid search parameters
    if make_request "$BASE_URL/api/v1/search" 422; then
        test_passed "Validation error handling"
    else
        test_failed "Validation error handling" "Should return 422 for missing required parameters"
    fi
}

# Integration tests (if applicable)
test_integrations() {
    log_info "Running integration tests..."
    
    # Test Redis connectivity (if Redis is available)
    # This would typically be done by checking if caching works
    # For now, we'll just verify the app is working, which implies Redis is working if configured
    
    # Test that multiple requests work (session handling, etc.)
    for i in {1..3}; do
        if ! make_request "$BASE_URL/api/v1/search?query=integration_test_$i&limit=1" 200; then
            test_failed "Multiple requests handling" "Request $i failed"
            return
        fi
    done
    test_passed "Multiple requests handling"
}

# Main test execution
run_all_tests() {
    local environment=$1
    
    log_info "Starting smoke tests for environment: $environment"
    log_info "=========================================="
    
    set_base_url "$environment"
    
    # Run test suites
    test_basic_connectivity || {
        log_error "Basic connectivity failed - aborting remaining tests"
        return 1
    }
    
    test_api_endpoints
    test_database_functionality
    test_basic_performance
    test_basic_security "$environment"
    test_error_handling
    test_integrations
    
    # Report results
    log_info ""
    log_info "=========================================="
    log_info "Test Results:"
    log_info "  Passed: $TESTS_PASSED"
    log_info "  Failed: $TESTS_FAILED"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        log_success "All smoke tests passed! ✓"
        return 0
    else
        log_error "Some tests failed:"
        for failed_test in "${FAILED_TESTS[@]}"; do
            log_error "  - $failed_test"
        done
        return 1
    fi
}

# Main function
main() {
    local environment=$1
    
    if [[ -z "$environment" ]]; then
        log_error "Usage: $0 <environment>"
        log_error "Environments: development, testing, staging, production"
        exit 1
    fi
    
    # Check if required tools are available
    if ! command -v curl >/dev/null 2>&1; then
        log_error "curl is required but not installed"
        exit 1
    fi
    
    if ! command -v python3 >/dev/null 2>&1; then
        log_error "python3 is required but not installed"
        exit 1
    fi
    
    # Run tests
    if run_all_tests "$environment"; then
        exit 0
    else
        exit 1
    fi
}

# Handle script termination
trap 'log_warning "Smoke tests interrupted"; exit 1' INT TERM

# Run main function
main "$@"
