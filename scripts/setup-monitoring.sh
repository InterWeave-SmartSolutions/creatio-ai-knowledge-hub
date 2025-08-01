#!/bin/bash

# Creatio AI Knowledge Hub - Monitoring and Logging Setup Script
# This script sets up the complete monitoring and logging infrastructure

set -e

echo "🚀 Setting up Monitoring and Logging for Creatio AI Knowledge Hub..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating directory structure..."
mkdir -p logs
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
chmod 755 logs

# Install Python monitoring dependencies
print_status "Installing Python monitoring dependencies..."
if [ -f "requirements-monitoring.txt" ]; then
    pip install -r requirements-monitoring.txt
else
    print_warning "requirements-monitoring.txt not found. Installing core dependencies..."
    pip install prometheus-client==0.17.1 psutil==5.9.5 python-json-logger==2.0.7
fi

# Create logs directory with proper permissions
print_status "Setting up log files..."
touch logs/application.json
touch logs/errors.log
touch logs/performance.log
touch logs/access.log
touch logs/security.log
chmod 664 logs/*.log logs/*.json

# Validate configuration files
print_status "Validating configuration files..."

# Check if monitoring configuration exists
if [ ! -f "monitoring/prometheus.yml" ]; then
    print_error "Prometheus configuration not found at monitoring/prometheus.yml"
    exit 1
fi

if [ ! -f "monitoring/alert_rules.yml" ]; then
    print_error "Alert rules not found at monitoring/alert_rules.yml"
    exit 1
fi

print_status "Configuration files validated successfully!"

# Start monitoring services
print_status "Starting monitoring services..."
docker-compose --profile monitoring up -d

# Wait for services to start
print_status "Waiting for services to start..."
sleep 10

# Health check for services
print_status "Performing health checks..."

# Check if Prometheus is running
if curl -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
    print_status "✅ Prometheus is healthy"
else
    print_warning "⚠️  Prometheus health check failed"
fi

# Check if Grafana is running
if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
    print_status "✅ Grafana is healthy"
else
    print_warning "⚠️  Grafana health check failed"
fi

# Check if application is running
if curl -f http://localhost:8001/api/v1/health > /dev/null 2>&1; then
    print_status "✅ Application health endpoint is responding"
else
    print_warning "⚠️  Application health check failed"
fi

# Check if metrics endpoint is working
if curl -f http://localhost:8001/metrics > /dev/null 2>&1; then
    print_status "✅ Application metrics endpoint is responding"
else
    print_warning "⚠️  Application metrics endpoint failed"
fi

# Display access information
print_status "Setup completed! Access points:"
echo ""
echo "📊 Grafana Dashboard: http://localhost:3000"
echo "   Username: admin"
echo "   Password: admin (change on first login)"
echo ""
echo "📈 Prometheus: http://localhost:9090"
echo ""
echo "🏥 Application Health: http://localhost:8001/api/v1/health"
echo "📊 Application Metrics: http://localhost:8001/metrics"
echo ""
echo "📁 Log Files Location: ./logs/"
echo "   - Application logs: ./logs/application.json"
echo "   - Error logs: ./logs/errors.log"
echo "   - Performance logs: ./logs/performance.log"
echo "   - Access logs: ./logs/access.log"
echo "   - Security logs: ./logs/security.log"
echo ""

# Grafana setup instructions
print_status "Grafana Dashboard Setup:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Login with admin/admin (change password when prompted)"
echo "3. Import the dashboard from monitoring/grafana/dashboards/creatio-knowledge-hub.json"
echo "4. Data sources should be automatically configured"
echo ""

# Test commands
print_status "Test Commands:"
echo "# Check application health:"
echo "curl http://localhost:8001/api/v1/health"
echo ""
echo "# Check detailed health with metrics:"
echo "curl http://localhost:8001/api/v1/health/deep"
echo ""
echo "# View Prometheus metrics:"
echo "curl http://localhost:8001/metrics"
echo ""
echo "# Monitor logs in real-time:"
echo "tail -f logs/application.json | jq ."
echo ""

# Optional: Test the monitoring system
read -p "Would you like to run a quick test of the monitoring system? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Running monitoring system test..."
    
    # Make some test requests to generate metrics
    for i in {1..10}; do
        curl -s http://localhost:8001/api/v1/health > /dev/null
        sleep 0.5
    done
    
    # Make a test search request if search endpoint exists
    curl -s "http://localhost:8001/api/v1/search?query=test&limit=5" > /dev/null || true
    
    print_status "Test requests completed. Check Grafana dashboard for metrics!"
fi

print_status "🎉 Monitoring and logging setup completed successfully!"
print_status "📖 For detailed documentation, see: docs/monitoring-and-logging.md"

# Optional: Show current system resources
if command -v free &> /dev/null && command -v df &> /dev/null; then
    echo ""
    print_status "Current System Resources:"
    echo "Memory usage:"
    free -h | grep -E "(Mem|Swap)"
    echo ""
    echo "Disk usage:"
    df -h | grep -vE '^Filesystem|tmpfs|cdrom'
fi
