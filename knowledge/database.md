# Database Connectivity & Performance (KB-DB-01)

## Overview
Standard procedures for handling database-related alerts and user reports regarding the PostgreSQL clusters.

## Common Issues & Resolutions

### 1. Connection Pool Exhaustion (HTTP 500 errors)
- **Symptoms**: Application logs show `Timeout waiting for connection from pool` or `remaining connection slots are reserved for non-replication superuser connections`.
- **Resolution**:
  1. Check PgBouncer metrics.
  2. Identify the service leaking connections.
  3. Restart the offending application pods.
  4. **Escalation**: Create GitHub issue for engineering to fix the connection leak.

### 2. High CPU / Slow Queries
- **Symptoms**: Reports of application slowness, CPU alerts on RDS/Aurora.
- **Resolution**:
  1. Check `pg_stat_activity` for long-running transactions.
  2. Use `EXPLAIN ANALYZE` on the top offending queries.
  3. Terminate runaway analytical queries if they are blocking production inserts.
  4. Notify the Data Engineering team via Slack.

### 3. Read Replica Lag
- **Symptoms**: Stale data in read-heavy endpoints (e.g., reporting dashboard).
- **Resolution**:
  1. Verify replication delay in CloudWatch.
  2. If lag > 5 minutes, check for massive DML operations running on the primary.
  3. Suspend non-critical background jobs.
