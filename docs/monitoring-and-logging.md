# Monitoring and Logging Setup Guide

This document provides comprehensive information about the monitoring and logging infrastructure for the Creatio AI Knowledge Hub.

## Overview

The monitoring system consists of:
- **Application Performance Monitoring (APM)** with Prometheus metrics
- **Centralized Logging** with structured JSON logs and log aggregation
- **Health Check Endpoints** for service health monitoring
- **Monitoring Dashboards** with Grafana visualization
- **Alert Configuration** with Prometheus alerting rules

## Components

### 1. Application Performance Monitoring

**Location**: `monitoring/monitoring.py`

#### Features:
- Real-time performance metrics collection
- Request duration and rate tracking
- Database query performance monitoring
- Search query performance tracking
- System resource monitoring (CPU, Memory, Disk)
- Custom Prometheus metrics

#### Key Metrics:
- `app_requests_total` - Total HTTP requests by method, endpoint, and status
- `app_request_duration_seconds` - Request duration histogram
- `app_active_connections` - Current active connections
- `database_query_duration_seconds` - Database query performance
- `search_queries_total` - Search query counters
- `system_cpu_usage_percent` - CPU usage percentage
- `system_memory_usage_bytes` - Memory usage in bytes
- `system_disk_usage_bytes` - Disk usage in bytes

### 2. Centralized Logging

**Location**: `monitoring/logging_config.py`

#### Log Types:
- **Application Logs** (`logs/application.json`) - Structured JSON logs
- **Error Logs** (`logs/errors.log`) - Error-specific logs with stack traces
- **Performance Logs** (`logs/performance.log`) - Performance metrics and timings
- **Access Logs** (`logs/access.log`) - HTTP request logs
- **Security Logs** (`logs/security.log`) - Security-related events

#### Features:
- Rotating log files with automatic cleanup
- Colored console output for development
- Structured JSON logging for production
- Log aggregation and analysis utilities
- Configurable log levels and formats

### 3. Health Check Endpoints

#### Available Endpoints:

**Basic Health Check**: `GET /api/v1/health`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "checks": {
    "database": {"status": "healthy", "response_time_ms": 5},
    "system": {
      "status": "healthy",
      "cpu_percent": 25.3,
      "memory_percent": 45.2,
      "disk_percent": 62.1
    },
    "search_index": {"status": "healthy"}
  }
}
```

**Deep Health Check**: `GET /api/v1/health/deep`
```json
{
  "health": {...},
  "metrics": {
    "timestamp": "2024-01-15T10:30:00Z",
    "system": {
      "cpu_usage": 25.3,
      "memory_usage": 45.2,
      "disk_usage": 62.1
    },
    "application": {
      "active_connections": 12,
      "total_requests": 1542,
      "database_connections": 3
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Prometheus Metrics**: `GET /metrics`
- Standard Prometheus format metrics endpoint
- Used by Prometheus for scraping metrics

### 4. Monitoring Dashboards

**Location**: `monitoring/grafana/dashboards/creatio-knowledge-hub.json`

#### Dashboard Panels:
1. **Application Health Status** - Real-time service status
2. **Request Rate** - HTTP requests per second
3. **Response Time (95th Percentile)** - Performance metrics
4. **Error Rate** - Error percentage over time
5. **System Resources** - CPU, Memory, Disk usage
6. **Database Performance** - Query times and connections
7. **Search Performance** - Search query metrics
8. **Active Connections** - Current connection count
9. **Total Requests (24h)** - Daily request volume
10. **Request Status Distribution** - Status code breakdown

### 5. Alert Configuration

**Location**: `monitoring/alert_rules.yml`

#### Alert Groups:

**Application Alerts:**
- High Error Rate (>10% for 5 minutes)
- High Response Time (>2s p95 for 5 minutes)
- Low Request Rate (<0.1 req/s for 10 minutes)
- Application Down (service unavailable)

**System Alerts:**
- High CPU Usage (>80% for 5 minutes)
- High Memory Usage (>3GB for 5 minutes)
- Disk Space Low (>20GB usage)

**Database Alerts:**
- Database Connections High (>50 connections)
- Database Slow Queries (>1s average)
- Database Unavailable

**Search Alerts:**
- Search Slow Queries (>2s average)
- Search High Error Rate (>10 errors in 5 minutes)

**Infrastructure Alerts:**
- Redis Down
- Redis High Memory Usage (>90%)
- Nginx Down
- Nginx High Error Rate

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements-monitoring.txt
```

### 2. Environment Setup

The monitoring system is integrated into the existing Docker Compose setup. Enable monitoring with:

```bash
docker-compose --profile monitoring up -d
```

This starts:
- Prometheus (port 9090)
- Grafana (port 3000)
- Application with metrics enabled

### 3. Access Points

- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Application Health**: http://localhost:8001/api/v1/health
- **Application Metrics**: http://localhost:8001/metrics

### 4. Configuration

#### Grafana Configuration:
1. Login to Grafana (admin/admin)
2. Import the dashboard from `monitoring/grafana/dashboards/creatio-knowledge-hub.json`
3. Configure data sources (automatically provisioned)

#### Prometheus Configuration:
- Configuration file: `monitoring/prometheus.yml`
- Alert rules: `monitoring/alert_rules.yml`
- Automatically discovers application metrics endpoint

## Usage

### Monitoring Application Performance

1. **View Real-time Metrics**: Access Grafana dashboard at http://localhost:3000
2. **Check Health Status**: 
   ```bash
   curl http://localhost:8001/api/v1/health
   ```
3. **View Prometheus Metrics**:
   ```bash
   curl http://localhost:8001/metrics
   ```

### Analyzing Logs

#### View Recent Errors:
```python
from monitoring.logging_config import log_aggregator
errors = log_aggregator.get_recent_errors(hours=24)
print(errors)
```

#### Performance Summary:
```python
perf_summary = log_aggregator.get_performance_summary(hours=24)
print(f"Average operation time: {perf_summary['avg_duration']:.3f}s")
```

#### Log File Statistics:
```python
stats = log_aggregator.get_log_stats()
for filename, info in stats.items():
    print(f"{filename}: {info['size_mb']}MB")
```

### Custom Monitoring

#### Adding Custom Metrics:
```python
from monitoring.monitoring import monitor
from prometheus_client import Counter

# Define custom metric
CUSTOM_COUNTER = Counter('custom_operations_total', 'Custom operations counter')

# Use in your code
CUSTOM_COUNTER.inc()
```

#### Performance Monitoring Decorator:
```python
@monitor.monitor_database_query('user_search')
def search_users(query):
    # Your database query code
    return results
```

## Troubleshooting

### Common Issues:

1. **Metrics Not Appearing in Grafana**:
   - Check Prometheus targets: http://localhost:9090/targets
   - Verify application metrics endpoint: http://localhost:8001/metrics
   - Ensure Grafana datasource is configured correctly

2. **High Memory Usage**:
   - Check log file sizes in `logs/` directory
   - Consider reducing log retention or increasing rotation limits
   - Monitor system resources via dashboard

3. **Database Connection Errors**:
   - Verify SQLite database path and permissions
   - Check database health endpoint
   - Review error logs for connection issues

4. **Missing Log Files**:
   - Ensure `logs/` directory exists and is writable
   - Check file permissions
   - Verify logging configuration is loaded

### Performance Optimization:

1. **Reduce Metrics Collection Frequency**:
   - Adjust Prometheus scrape intervals in `prometheus.yml`
   - Modify system metrics update frequency in monitoring code

2. **Log File Management**:
   - Configure appropriate rotation limits
   - Set up log cleanup cron jobs for production
   - Use log aggregation services for large deployments

3. **Database Query Optimization**:
   - Monitor slow queries via dashboard
   - Add database indexes for frequently queried fields
   - Implement query caching where appropriate

## Production Considerations

### Security:
- Change default Grafana credentials
- Configure proper authentication for Prometheus
- Secure metrics endpoints in production
- Use HTTPS for all monitoring interfaces

### Scalability:
- Consider using external time-series databases for large deployments
- Implement log forwarding to centralized logging systems
- Use load balancers for high-availability monitoring

### Backup:
- Regular backup of Grafana dashboards and configurations
- Archive historical metrics data
- Backup monitoring configurations and alert rules

### Compliance:
- Ensure log retention meets regulatory requirements
- Implement log anonymization for sensitive data
- Configure audit trails for monitoring system access

## Alert Management

### Setting Up Notifications:

1. **Email Notifications**:
   ```yaml
   # In alertmanager.yml
   route:
     receiver: 'email-notifications'
   receivers:
     - name: 'email-notifications'
       email_configs:
         - to: 'admin@company.com'
           subject: 'Alert: {{ .GroupLabels.alertname }}'
   ```

2. **Slack Integration**:
   ```yaml
   receivers:
     - name: 'slack-notifications'
       slack_configs:
         - api_url: 'YOUR_SLACK_WEBHOOK_URL'
           channel: '#alerts'
   ```

### Custom Alert Rules:

```yaml
# Custom alert example
- alert: CustomMetricHigh
  expr: custom_metric_value > 100
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Custom metric is high"
    description: "Custom metric value is {{ $value }}"
```

## Maintenance

### Regular Tasks:
- Review and update alert thresholds
- Clean up old log files
- Update monitoring dashboards
- Test alert notifications
- Monitor system resource usage
- Review and optimize slow queries

### Monitoring System Health:
- Set up monitoring for the monitoring system itself
- Create alerts for Prometheus/Grafana downtime
- Monitor disk space for metrics storage
- Track monitoring system performance impact
