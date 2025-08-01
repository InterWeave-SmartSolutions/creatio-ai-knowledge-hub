#!/bin/bash

# Test execution script for Creatio AI Knowledge Hub
# This script runs different types of tests based on the provided arguments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test result tracking
TESTS_PASSED=0
TESTS_FAILED=0
TEST_RESULTS=()

# Default configuration
DEFAULT_COVERAGE_THRESHOLD=80
DEFAULT_PARALLEL_WORKERS=4
DEFAULT_TIMEOUT=300

# Configuration
COVERAGE_THRESHOLD=${COVERAGE_THRESHOLD:-$DEFAULT_COVERAGE_THRESHOLD}
PARALLEL_WORKERS=${PARALLEL_WORKERS:-$DEFAULT_PARALLEL_WORKERS}
TEST_TIMEOUT=${TEST_TIMEOUT:-$DEFAULT_TIMEOUT}

# Directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTS_DIR="${PROJECT_ROOT}/test-reports"
COVERAGE_DIR="${PROJECT_ROOT}/coverage"

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Setup test environment
setup_test_environment() {
    print_header "Setting up test environment"
    
    # Create necessary directories
    mkdir -p "${REPORTS_DIR}"
    mkdir -p "${COVERAGE_DIR}"
    
    # Set test environment variables
    export NODE_ENV=test
    export ENVIRONMENT=test
    export DATABASE_URL=sqlite:///test_knowledge_hub.db
    export REDIS_URL=redis://localhost:6379/1
    
    print_success "Test environment setup complete"
}

# Generate test data
generate_test_data() {
    print_header "Generating test data"
    
    # Generate Python test data
    if command -v python3 &> /dev/null; then
        print_info "Generating Python test data..."
        python3 "${PROJECT_ROOT}/tests/generators/test_data_generator.py"
        print_success "Python test data generated"
    fi
    
    # Generate JavaScript test data
    if command -v npm &> /dev/null; then
        print_info "Generating JavaScript test data..."
        cd "${PROJECT_ROOT}"
        npm run ts-node tests/generators/test-data-generator.ts
        print_success "JavaScript test data generated"
    fi
}

# Run Python unit tests
run_python_unit_tests() {
    print_header "Running Python Unit Tests"
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 not found, skipping Python tests"
        return 1
    fi
    
    cd "${PROJECT_ROOT}"
    
    # Install dependencies if needed
    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    else
        source venv/bin/activate
    fi
    
    # Run tests with coverage
    pytest tests/unit/ \
        --verbose \
        --cov=. \
        --cov-report=html:"${COVERAGE_DIR}/python-html" \
        --cov-report=xml:"${COVERAGE_DIR}/python-coverage.xml" \
        --cov-report=term-missing \
        --cov-fail-under="${COVERAGE_THRESHOLD}" \
        --junit-xml="${REPORTS_DIR}/python-unit-results.xml" \
        --maxfail=5 \
        --tb=short
    
    local result=$?
    if [ $result -eq 0 ]; then
        print_success "Python unit tests passed"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("Python Unit Tests: PASSED")
    else
        print_error "Python unit tests failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("Python Unit Tests: FAILED")
    fi
    
    deactivate
    return $result
}

# Run JavaScript unit tests
run_javascript_unit_tests() {
    print_header "Running JavaScript/TypeScript Unit Tests"
    
    if ! command -v npm &> /dev/null; then
        print_error "npm not found, skipping JavaScript tests"
        return 1
    fi
    
    cd "${PROJECT_ROOT}"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_info "Installing npm dependencies..."
        npm ci
    fi
    
    # Run TypeScript checks
    print_info "Running TypeScript type checks..."
    npm run type-check
    
    # Run linting
    print_info "Running ESLint..."
    npm run lint:check
    
    # Run unit tests
    npm run test:unit -- \
        --coverage \
        --watchAll=false \
        --ci \
        --maxWorkers="${PARALLEL_WORKERS}" \
        --coverageDirectory="${COVERAGE_DIR}/javascript" \
        --coverageReporters=html,xml,text,lcov \
        --coverageThreshold='{"global":{"branches":'"${COVERAGE_THRESHOLD}"',"functions":'"${COVERAGE_THRESHOLD}"',"lines":'"${COVERAGE_THRESHOLD}"',"statements":'"${COVERAGE_THRESHOLD}"'}}'
    
    local result=$?
    if [ $result -eq 0 ]; then
        print_success "JavaScript unit tests passed"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("JavaScript Unit Tests: PASSED")
    else
        print_error "JavaScript unit tests failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("JavaScript Unit Tests: FAILED")
    fi
    
    return $result
}

# Run integration tests
run_integration_tests() {
    print_header "Running Integration Tests"
    
    # Start Redis if not running
    if ! pgrep -x "redis-server" > /dev/null; then
        print_info "Starting Redis server..."
        redis-server --daemonize yes --port 6379
        sleep 2
    fi
    
    # Run Python integration tests
    if command -v python3 &> /dev/null; then
        print_info "Running Python integration tests..."
        cd "${PROJECT_ROOT}"
        source venv/bin/activate
        
        pytest tests/integration/ \
            --verbose \
            --junit-xml="${REPORTS_DIR}/python-integration-results.xml" \
            --maxfail=3 \
            --tb=short
        
        local python_result=$?
        deactivate
    fi
    
    # Run JavaScript integration tests
    if command -v npm &> /dev/null; then
        print_info "Running JavaScript integration tests..."
        cd "${PROJECT_ROOT}"
        
        npm run test:integration -- \
            --watchAll=false \
            --ci \
            --maxWorkers=2
        
        local js_result=$?
    fi
    
    local result=0
    if [ ${python_result:-0} -ne 0 ] || [ ${js_result:-0} -ne 0 ]; then
        result=1
    fi
    
    if [ $result -eq 0 ]; then
        print_success "Integration tests passed"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("Integration Tests: PASSED")
    else
        print_error "Integration tests failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("Integration Tests: FAILED")
    fi
    
    return $result
}

# Run end-to-end tests
run_e2e_tests() {
    print_header "Running End-to-End Tests"
    
    if ! command -v npm &> /dev/null; then
        print_error "npm not found, skipping E2E tests"
        return 1
    fi
    
    cd "${PROJECT_ROOT}"
    
    # Install Playwright browsers if needed
    if [ ! -d "~/.cache/ms-playwright" ]; then
        print_info "Installing Playwright browsers..."
        npx playwright install --with-deps
    fi
    
    # Start the application server
    print_info "Starting application server..."
    if command -v python3 &> /dev/null; then
        source venv/bin/activate
        python3 -m uvicorn ai_knowledge_hub.enhanced_mcp_server:app --port 3000 &
        SERVER_PID=$!
        deactivate
        sleep 10
    fi
    
    # Run Playwright tests
    TEST_BASE_URL=http://localhost:3000 npx playwright test \
        --reporter=html \
        --output-dir="${REPORTS_DIR}/playwright"
    
    local result=$?
    
    # Stop the server
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null || true
    fi
    
    if [ $result -eq 0 ]; then
        print_success "E2E tests passed"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("E2E Tests: PASSED")
    else
        print_error "E2E tests failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("E2E Tests: FAILED")
    fi
    
    return $result
}

# Run performance tests
run_performance_tests() {
    print_header "Running Performance Tests"
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 not found, skipping performance tests"
        return 1
    fi
    
    cd "${PROJECT_ROOT}"
    source venv/bin/activate
    
    # Start the application server
    print_info "Starting application server for performance testing..."
    python3 -m uvicorn ai_knowledge_hub.enhanced_mcp_server:app --port 3000 &
    SERVER_PID=$!
    sleep 10
    
    # Run Locust performance tests
    locust -f tests/performance/locustfile.py \
        --host=http://localhost:3000 \
        --users=10 \
        --spawn-rate=2 \
        --run-time=60s \
        --headless \
        --html="${REPORTS_DIR}/performance-report.html" \
        --csv="${REPORTS_DIR}/performance"
    
    local result=$?
    
    # Stop the server
    kill $SERVER_PID 2>/dev/null || true
    deactivate
    
    if [ $result -eq 0 ]; then
        print_success "Performance tests completed"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        TEST_RESULTS+=("Performance Tests: PASSED")
    else
        print_error "Performance tests failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        TEST_RESULTS+=("Performance Tests: FAILED")
    fi
    
    return $result
}

# Generate test report
generate_test_report() {
    print_header "Test Execution Summary"
    
    local total_tests=$((TESTS_PASSED + TESTS_FAILED))
    
    echo "Test Results:"
    for result in "${TEST_RESULTS[@]}"; do
        if [[ $result == *"PASSED"* ]]; then
            print_success "$result"
        else
            print_error "$result"
        fi
    done
    
    echo ""
    echo "Summary:"
    print_info "Total test suites: $total_tests"
    print_success "Passed: $TESTS_PASSED"
    print_error "Failed: $TESTS_FAILED"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        print_success "All tests passed! 🎉"
        return 0
    else
        print_error "Some tests failed. Check the reports in ${REPORTS_DIR}"
        return 1
    fi
}

# Display help
show_help() {
    echo "Usage: $0 [OPTIONS] [TEST_TYPE]"
    echo ""
    echo "Test execution script for Creatio AI Knowledge Hub"
    echo ""
    echo "TEST_TYPE:"
    echo "  unit           Run unit tests only"
    echo "  integration    Run integration tests only"
    echo "  e2e           Run end-to-end tests only"
    echo "  performance   Run performance tests only"
    echo "  all           Run all tests (default)"
    echo ""
    echo "OPTIONS:"
    echo "  --coverage-threshold N    Set minimum coverage threshold (default: 80)"
    echo "  --parallel-workers N      Set number of parallel test workers (default: 4)"
    echo "  --timeout N              Set test timeout in seconds (default: 300)"
    echo "  --skip-data-generation   Skip test data generation"
    echo "  --clean                  Clean test artifacts before running"
    echo "  --help                   Show this help message"
    echo ""
    echo "ENVIRONMENT VARIABLES:"
    echo "  COVERAGE_THRESHOLD       Override coverage threshold"
    echo "  PARALLEL_WORKERS         Override parallel workers"
    echo "  TEST_TIMEOUT            Override test timeout"
    echo ""
    echo "Examples:"
    echo "  $0 unit                  Run only unit tests"
    echo "  $0 --coverage-threshold 90 all    Run all tests with 90% coverage requirement"
    echo "  $0 --clean integration   Clean and run integration tests"
}

# Clean test artifacts
clean_test_artifacts() {
    print_info "Cleaning test artifacts..."
    rm -rf "${REPORTS_DIR}"
    rm -rf "${COVERAGE_DIR}"
    rm -rf playwright-report/
    rm -rf test-results/
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -delete
    print_success "Test artifacts cleaned"
}

# Main execution
main() {
    local test_type="all"
    local skip_data_generation=false
    local clean_first=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --coverage-threshold)
                COVERAGE_THRESHOLD="$2"
                shift 2
                ;;
            --parallel-workers)
                PARALLEL_WORKERS="$2"
                shift 2
                ;;
            --timeout)
                TEST_TIMEOUT="$2"
                shift 2
                ;;
            --skip-data-generation)
                skip_data_generation=true
                shift
                ;;
            --clean)
                clean_first=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            unit|integration|e2e|performance|all)
                test_type="$1"
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    print_header "Creatio AI Knowledge Hub Test Runner"
    print_info "Test type: $test_type"
    print_info "Coverage threshold: ${COVERAGE_THRESHOLD}%"
    print_info "Parallel workers: $PARALLEL_WORKERS"
    print_info "Test timeout: ${TEST_TIMEOUT}s"
    
    # Clean if requested
    if [ "$clean_first" = true ]; then
        clean_test_artifacts
    fi
    
    # Setup environment
    setup_test_environment
    
    # Generate test data unless skipped
    if [ "$skip_data_generation" = false ]; then
        generate_test_data
    fi
    
    # Run tests based on type
    case $test_type in
        unit)
            run_python_unit_tests
            run_javascript_unit_tests
            ;;
        integration)
            run_integration_tests
            ;;
        e2e)
            run_e2e_tests
            ;;
        performance)
            run_performance_tests
            ;;
        all)
            run_python_unit_tests
            run_javascript_unit_tests
            run_integration_tests
            run_e2e_tests
            ;;
    esac
    
    # Generate report
    generate_test_report
}

# Execute main function with all arguments
main "$@"
