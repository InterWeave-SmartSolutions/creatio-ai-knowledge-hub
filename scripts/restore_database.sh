#!/bin/bash

# Creatio Database Restore Script
# Usage: ./restore_database.sh <backup_file> [target_database]

set -e

# Configuration
DB_USER="creatio_dev"
DB_HOST="localhost"
DB_PORT="5432"

# Check if backup file is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <backup_file> [target_database]"
    echo "Example: $0 /path/to/backup.backup creatio_dev"
    exit 1
fi

BACKUP_FILE="$1"
DB_NAME="${2:-creatio_dev}"

# Validate backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file '$BACKUP_FILE' does not exist"
    exit 1
fi

# Validate database name
if [[ "$DB_NAME" != "creatio_dev" && "$DB_NAME" != "creatio_staging" ]]; then
    echo "Error: Invalid database name. Use 'creatio_dev' or 'creatio_staging'"
    exit 1
fi

echo "Starting restore of database: $DB_NAME"
echo "From backup file: $BACKUP_FILE"

# Confirm restore operation
read -p "This will overwrite the existing database '$DB_NAME'. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled."
    exit 0
fi

# Drop and recreate database
echo "Dropping existing database..."
PGPASSWORD="creatio123" dropdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" 2>/dev/null || true

echo "Creating new database..."
PGPASSWORD="creatio123" createdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME"

# Restore from backup
echo "Restoring from backup..."
PGPASSWORD="creatio123" pg_restore \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -v \
    --no-owner \
    --no-privileges \
    "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Database restore completed successfully!"
else
    echo "Database restore failed!"
    exit 1
fi
