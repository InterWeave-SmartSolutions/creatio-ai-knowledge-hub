#!/bin/bash

# Creatio Database Backup Script
# Usage: ./backup_database.sh [database_name]

set -e

# Configuration
DB_USER="creatio_dev"
DB_HOST="localhost"
DB_PORT="5432"
BACKUP_DIR="/home/andrewwork/creatio-ai-knowledge-hub/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Default to development database if no argument provided
DB_NAME="${1:-creatio_dev}"

# Validate database name
if [[ "$DB_NAME" != "creatio_dev" && "$DB_NAME" != "creatio_staging" ]]; then
    echo "Error: Invalid database name. Use 'creatio_dev' or 'creatio_staging'"
    exit 1
fi

BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_${TIMESTAMP}.backup"

echo "Starting backup of database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"

# Perform backup
PGPASSWORD="creatio123" pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -F c \
    -b \
    -v \
    -f "$BACKUP_FILE" \
    "$DB_NAME"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully!"
    echo "File size: $(du -h "$BACKUP_FILE" | cut -f1)"
    
    # Keep only last 10 backups
    ls -t "$BACKUP_DIR"/${DB_NAME}_backup_*.backup | tail -n +11 | xargs -r rm
    echo "Old backups cleaned up (keeping latest 10)"
else
    echo "Backup failed!"
    exit 1
fi
