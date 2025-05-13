import psycopg2
from config_app.db_config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def insert_price_record(data):
    """
    Inserts a single crypto price record into the database.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

        cur = conn.cursor()

        insert_query = """
        INSERT INTO crypto_prices (symbol, name, price_usd, market_cap, volume, timestamp, change_1h, change_24h)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(insert_query, (
            data['symbol'],
            data['name'],
            data['price_usd'],
            data['market_cap'],
            data['volume'],
            data['timestamp'],
            data.get('change_1h'),
            data.get('change_24h'),
        ))

        conn.commit()
        cur.close()

    except Exception as e:
        print(f"Database insertion error: {e}")
    finally:
        if conn:
            conn.close()
