# Dashboard Notes

## Grafana Setup

1. Access Grafana at `http://localhost:3000`
2. Login with `admin / admin`
3. Add PostgreSQL as a data source:
   - Host: `postgres`
   - DB: `crypto_db`
   - User: `admin`, Password: `admin`
4. Create panels using queries like:
   ```sql
   SELECT timestamp AS time, symbol, price_usd
   FROM crypto_prices
   WHERE $__timeFilter(timestamp)
   ORDER BY timestamp ASC
