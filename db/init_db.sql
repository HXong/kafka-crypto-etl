CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(50),
    price_usd NUMERIC,
    market_cap NUMERIC,
    volume NUMERIC,
    timestamp TIMESTAMP,
    change_1h NUMERIC,
    change_24h NUMERIC,
);