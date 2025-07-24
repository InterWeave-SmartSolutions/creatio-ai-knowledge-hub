#!/bin/bash

# Creatio Linux Development Environment Setup Script
# This script sets up a complete Creatio development environment on Linux

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CREATIO_HOME="/home/$USER/creatio-local"
DB_NAME="CreatioStudio"
DB_USER="creatio_user"
DB_PASS="creatio_pass"
REDIS_DB="1"

print_header() {
    echo -e "${BLUE}"
    echo "=================================="
    echo "  Creatio Linux Setup Script"
    echo "=================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_step "Checking prerequisites..."
    
    # Check if running on Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        print_error "This script is designed for Linux systems"
        exit 1
    fi
    
    # Check for required commands
    local required_commands=("docker" "psql" "redis-cli" "dotnet")
    for cmd in "${required_commands[@]}"; do
        if ! command -v $cmd &> /dev/null; then
            print_error "$cmd is not installed or not in PATH"
            exit 1
        fi
    done
    
    print_info "All prerequisites met ✓"
}

setup_directories() {
    print_step "Setting up directory structure..."
    
    mkdir -p $CREATIO_HOME/{application,database,logs,config,backups}
    mkdir -p $CREATIO_HOME/application/{files,packages}
    
    print_info "Directory structure created at $CREATIO_HOME"
}

configure_postgresql() {
    print_step "Configuring PostgreSQL database..."
    
    # Check if PostgreSQL is running
    if ! sudo systemctl is-active --quiet postgresql; then
        print_info "Starting PostgreSQL service..."
        sudo systemctl start postgresql
    fi
    
    # Create database user if it doesn't exist
    if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
        print_info "Creating database user: $DB_USER"
        sudo -u postgres createuser $DB_USER
        sudo -u postgres psql -c "ALTER USER $DB_USER PASSWORD '$DB_PASS';"
        sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"
    fi
    
    # Create database if it doesn't exist
    if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
        print_info "Creating database: $DB_NAME"
        sudo -u postgres createdb $DB_NAME -O $DB_USER
    fi
    
    # Test connection
    if PGPASSWORD=$DB_PASS psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT version();" &> /dev/null; then
        print_info "Database connection successful ✓"
    else
        print_error "Database connection failed"
        exit 1
    fi
}

configure_redis() {
    print_step "Configuring Redis cache server..."
    
    # Check if Redis is running
    if ! sudo systemctl is-active --quiet redis-server; then
        print_info "Starting Redis service..."
        sudo systemctl start redis-server
    fi
    
    # Test Redis connection
    if redis-cli ping &> /dev/null; then
        print_info "Redis connection successful ✓"
    else
        print_error "Redis connection failed"
        exit 1
    fi
    
    # Configure Redis for Docker access if needed
    local redis_conf="/etc/redis/redis.conf"
    if [[ -f $redis_conf ]]; then
        if ! grep -q "bind 0.0.0.0" $redis_conf; then
            print_info "Configuring Redis for Docker access..."
            sudo sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/' $redis_conf
            sudo systemctl restart redis-server
        fi
    fi
}

create_configuration_files() {
    print_step "Creating configuration files..."
    
    # Connection strings configuration
    cat > $CREATIO_HOME/config/ConnectionStrings.config << EOF
<?xml version="1.0" encoding="utf-8"?>
<connectionStrings>
  <add name="db" 
       connectionString="Server=localhost;Port=5432;Database=$DB_NAME;User Id=$DB_USER;Password=$DB_PASS;Timeout=500;CommandTimeout=400" 
       providerName="Npgsql" />
  
  <add name="redis" 
       connectionString="host=localhost;db=$REDIS_DB;port=6379;maxReadPoolSize=10;maxWritePoolSize=500" />
  
  <add name="session" 
       connectionString="host=localhost;db=2;port=6379;maxReadPoolSize=10;maxWritePoolSize=500" />
  
  <add name="defConnectionString" 
       connectionString="Server=localhost;Port=5432;Database=$DB_NAME;User Id=$DB_USER;Password=$DB_PASS;Timeout=500;CommandTimeout=400" 
       providerName="Npgsql" />
</connectionStrings>
EOF

    # App settings for development
    cat > $CREATIO_HOME/config/appsettings.json << EOF
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Https": {
    "Url": "https://localhost:5002"
  }
}
EOF

    # Docker Compose for easy orchestration
    cat > $CREATIO_HOME/docker-compose.yml << EOF
version: '3.8'

services:
  creatio:
    build: .
    ports:
      - "5000:5000"
      - "5002:5002"
    volumes:
      - ./application:/app
      - ./logs:/app/Logs
      - ./config/ConnectionStrings.config:/app/ConnectionStrings.config
      - ./config/appsettings.json:/app/appsettings.json
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - TZ=US/Eastern
      - COMPlus_ThreadPool_ForceMinWorkerThreads=100
    depends_on:
      - redis
      - postgres
    networks:
      - creatio-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - creatio-network

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: $DB_NAME
      POSTGRES_USER: $DB_USER
      POSTGRES_PASSWORD: $DB_PASS
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    networks:
      - creatio-network

volumes:
  redis-data:
  postgres-data:

networks:
  creatio-network:
    driver: bridge
EOF

    print_info "Configuration files created ✓"
}

create_dockerfile() {
    print_step "Creating Dockerfile..."
    
    cat > $CREATIO_HOME/Dockerfile << EOF
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base
EXPOSE 5000 5002

RUN apt-get update && \\
    apt-get -y --no-install-recommends install \\
    libgdiplus \\
    libc6-dev && \\
    apt-get clean all && \\
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /app

# Copy application files when available
# COPY . ./

FROM base AS final
WORKDIR /app

ENV ASPNETCORE_ENVIRONMENT Development
ENV TZ US/Eastern
ENV COMPlus_ThreadPool_ForceMinWorkerThreads 100

# Entry point for Creatio application
# ENTRYPOINT ["dotnet", "Terrasoft.WebHost.dll"]

# Keep container running for development
CMD ["tail", "-f", "/dev/null"]
EOF

    print_info "Dockerfile created ✓"
}

setup_clio() {
    print_step "Setting up Clio development tool..."
    
    if ! command -v clio &> /dev/null; then
        if command -v npm &> /dev/null; then
            print_info "Installing Clio via npm..."
            npm install -g clio
        else
            print_warning "npm not found. Clio installation skipped."
            return
        fi
    fi
    
    # Create Clio configuration directory
    mkdir -p ~/.clio
    
    print_info "Clio setup completed ✓"
}

create_startup_script() {
    print_step "Creating startup script..."
    
    cat > $CREATIO_HOME/start-creatio.sh << 'EOF'
#!/bin/bash

# Creatio Development Environment Startup Script

CREATIO_HOME="/home/$USER/creatio-local"
cd $CREATIO_HOME

echo "🚀 Starting Creatio Development Environment..."

# Start services using Docker Compose
if [[ -f docker-compose.yml ]]; then
    echo "Starting services with Docker Compose..."
    docker-compose up -d
    
    echo "Waiting for services to be ready..."
    sleep 10
    
    echo "Services status:"
    docker-compose ps
    
    echo ""
    echo "✅ Creatio Development Environment is ready!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   HTTP:  http://localhost:5000"
    echo "   HTTPS: https://localhost:5002"
    echo ""
    echo "🗄️  Database: PostgreSQL on localhost:5432"
    echo "⚡ Redis: localhost:6379"
    echo ""
    echo "📊 To view logs: docker-compose logs -f creatio"
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ docker-compose.yml not found. Please run setup first."
    exit 1
fi
EOF

    chmod +x $CREATIO_HOME/start-creatio.sh
    
    print_info "Startup script created ✓"
}

create_installation_guide() {
    print_step "Creating installation guide..."
    
    cat > $CREATIO_HOME/README.md << EOF
# Creatio Local Development Environment

## Overview
This directory contains a complete Creatio development environment setup for Linux.

## Directory Structure
- \`application/\` - Creatio application files (place extracted files here)
- \`config/\` - Configuration files
- \`database/\` - Database initialization scripts
- \`logs/\` - Application logs
- \`backups/\` - Database and configuration backups

## Prerequisites Installed
- ✅ PostgreSQL 16
- ✅ Redis 7
- ✅ .NET 8 SDK
- ✅ Docker & Docker Compose

## Database Configuration
- **Database**: $DB_NAME
- **User**: $DB_USER
- **Password**: $DB_PASS
- **Port**: 5432

## Redis Configuration
- **Host**: localhost
- **Port**: 6379
- **Database**: $REDIS_DB

## Next Steps

### 1. Obtain Creatio Installation Files
Contact Creatio support to get the Linux installation package and extract it to the \`application/\` directory.

### 2. Start the Environment
\`\`\`bash
./start-creatio.sh
\`\`\`

### 3. Access Creatio
- HTTP: http://localhost:5000
- HTTPS: https://localhost:5002
- Default credentials: Supervisor / Supervisor

### 4. Development Tools
- Use Clio for package management
- Configure your IDE to point to the application directory
- Enable file system development mode in Creatio

## Troubleshooting
- Check service status: \`docker-compose ps\`
- View logs: \`docker-compose logs -f creatio\`
- Restart services: \`docker-compose restart\`

## File System Development Mode
Once Creatio is running:
1. Go to System Designer → Advanced Settings
2. Click "Actions" → "Download packages to file system"
3. Configure your IDE to work with the package files

EOF

    print_info "Installation guide created ✓"
}

print_summary() {
    print_step "Setup Summary"
    
    echo -e "${GREEN}"
    echo "✅ Creatio development environment setup completed!"
    echo ""
    echo "📁 Installation directory: $CREATIO_HOME"
    echo "🗄️  Database: $DB_NAME (PostgreSQL)"
    echo "⚡ Cache: Redis on localhost:6379"
    echo "🐳 Docker: Ready for containerized deployment"
    echo ""
    echo "Next steps:"
    echo "1. Obtain Creatio installation files from support"
    echo "2. Extract files to $CREATIO_HOME/application/"
    echo "3. Run: cd $CREATIO_HOME && ./start-creatio.sh"
    echo ""
    echo "📖 Full documentation: $CREATIO_HOME/README.md"
    echo -e "${NC}"
}

# Main execution
main() {
    print_header
    
    check_prerequisites
    setup_directories
    configure_postgresql
    configure_redis
    create_configuration_files
    create_dockerfile
    setup_clio
    create_startup_script
    create_installation_guide
    
    print_summary
}

# Run the main setup
main "$@"
