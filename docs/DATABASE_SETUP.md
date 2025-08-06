---
title: 'Creatio Database Environment Setup'
tags: [docs]
description:
  'Auto-generated front matter for AI indexing. Improve this description.'
source_path: 'docs/DATABASE_SETUP.md'
last_updated: '2025-08-06'
---

# Creatio Database Environment Setup

This document outlines the database environment setup for local Creatio
development.

## Overview

- **Database System**: PostgreSQL 16.9
- **Development Database**: `creatio_dev`
- **Staging Database**: `creatio_staging`
- **Database User**: `creatio_dev`
- **Admin User**: `postgres`

## Database Configuration

### Connection Details

| Environment | Database        | User        | Password    | Host      | Port |
| ----------- | --------------- | ----------- | ----------- | --------- | ---- |
| Development | creatio_dev     | creatio_dev | creatio123  | localhost | 5432 |
| Staging     | creatio_staging | creatio_dev | creatio123  | localhost | 5432 |
| Admin       | postgres        | postgres    | postgres123 | localhost | 5432 |

### Connection Strings

**Development (.NET/Npgsql):**

```
Host=localhost;Port=5432;Database=creatio_dev;Username=creatio_dev;Password=creatio123;
```

**Staging (.NET/Npgsql):**

```
Host=localhost;Port=5432;Database=creatio_staging;Username=creatio_dev;Password=creatio123;
```

**Node.js (postgresql://):**

```
postgresql://creatio_dev:creatio123@localhost:5432/creatio_dev
```

## Available Scripts

### Testing Database Connection

```bash
./scripts/test_database.sh
```

Verifies all database connections and displays environment status.

### Database Backup

```bash
./scripts/backup_database.sh [database_name]
```

- Creates timestamped backups in
  `/home/andrewwork/creatio-ai-knowledge-hub/backups/`
- Keeps latest 10 backups automatically
- Defaults to `creatio_dev` if no database specified
- Supports both `creatio_dev` and `creatio_staging`

**Examples:**

```bash
./scripts/backup_database.sh                    # Backup development database
./scripts/backup_database.sh creatio_staging    # Backup staging database
```

### Database Restore

```bash
./scripts/restore_database.sh <backup_file> [target_database]
```

- Restores from backup file to specified database
- Prompts for confirmation before overwriting
- Defaults to `creatio_dev` if no target specified

**Examples:**

```bash
./scripts/restore_database.sh backups/creatio_dev_backup_20250724_163000.backup
./scripts/restore_database.sh backups/backup.backup creatio_staging
```

## Manual Database Operations

### Backup Commands

```bash
# Development database
PGPASSWORD="creatio123" pg_dump -h localhost -U creatio_dev -F c -b -v -f backup.backup creatio_dev

# Staging database
PGPASSWORD="creatio123" pg_dump -h localhost -U creatio_dev -F c -b -v -f backup.backup creatio_staging
```

### Restore Commands

```bash
# Drop and recreate database
PGPASSWORD="creatio123" dropdb -h localhost -U creatio_dev creatio_dev
PGPASSWORD="creatio123" createdb -h localhost -U creatio_dev creatio_dev

# Restore from backup
PGPASSWORD="creatio123" pg_restore -h localhost -U creatio_dev -d creatio_dev -v --no-owner --no-privileges backup.backup
```

### Direct Database Access

```bash
# Connect to development database
PGPASSWORD="creatio123" psql -h localhost -U creatio_dev -d creatio_dev

# Connect to staging database
PGPASSWORD="creatio123" psql -h localhost -U creatio_dev -d creatio_staging

# Connect as admin
sudo -u postgres psql
```

## PostgreSQL Service Management

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Stop PostgreSQL
sudo systemctl stop postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Check status
sudo systemctl status postgresql

# Enable auto-start on boot
sudo systemctl enable postgresql
```

## Security Notes

- Default passwords are used for local development only
- For production environments, use strong passwords and proper authentication
- The `pg_hba.conf` has been configured for local development access
- Backup files contain sensitive data and should be secured appropriately

## Troubleshooting

### Connection Issues

1. Verify PostgreSQL service is running: `sudo systemctl status postgresql`
2. Check if databases exist: `sudo -u postgres psql -l`
3. Test connection: `./scripts/test_database.sh`

### Authentication Issues

1. Verify user exists: `sudo -u postgres psql -c "\du"`
2. Check `pg_hba.conf` configuration:
   `sudo cat /etc/postgresql/16/main/pg_hba.conf`
3. Reload PostgreSQL config: `sudo systemctl reload postgresql`

### Permission Issues

1. Grant permissions:
   `sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE creatio_dev TO creatio_dev;"`
2. Check database ownership: `sudo -u postgres psql -l`

## Directory Structure

```
creatio-ai-knowledge-hub/
├── scripts/
│   ├── backup_database.sh      # Database backup script
│   ├── restore_database.sh     # Database restore script
│   └── test_database.sh        # Connection test script
├── config/
│   └── database.config         # Database configuration file
├── backups/                    # Backup files directory
└── docs/
    └── DATABASE_SETUP.md       # This documentation
```
