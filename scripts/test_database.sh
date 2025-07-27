#!/bin/bash

# Creatio Database Connection Test Script

set -e

echo "=== Creatio Database Environment Test ==="
echo

# Test PostgreSQL service
echo "1. Testing PostgreSQL service status..."
if systemctl is-active --quiet postgresql; then
    echo "   ✓ PostgreSQL service is running"
else
    echo "   ✗ PostgreSQL service is not running"
    exit 1
fi

# Test admin connection
echo "2. Testing admin connection..."
if echo "SELECT 'Admin connection successful';" | sudo -u postgres psql -q > /dev/null 2>&1; then
    echo "   ✓ Admin connection successful"
else
    echo "   ✗ Admin connection failed"
    exit 1
fi

# Test development database connection
echo "3. Testing development database connection..."
if echo "SELECT 'Dev connection successful';" | PGPASSWORD=creatio123 psql -h localhost -U creatio_dev -d creatio_dev -q > /dev/null 2>&1; then
    echo "   ✓ Development database connection successful"
else
    echo "   ✗ Development database connection failed"
    exit 1
fi

# Test staging database connection
echo "4. Testing staging database connection..."
if echo "SELECT 'Staging connection successful';" | PGPASSWORD=creatio123 psql -h localhost -U creatio_dev -d creatio_staging -q > /dev/null 2>&1; then
    echo "   ✓ Staging database connection successful"
else
    echo "   ✗ Staging database connection failed"
    exit 1
fi

# Display database information
echo "5. Database information:"
echo "   Development Database: creatio_dev"
echo "   Staging Database: creatio_staging"
echo "   Database User: creatio_dev"
echo "   PostgreSQL Version: $(echo "SELECT version();" | sudo -u postgres psql -t | head -1 | xargs)"

echo
echo "=== All tests passed! Database environment is ready for Creatio development ==="
