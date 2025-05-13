import json
import time
import requests
from kafka import KafkaProducer
from config_app.kafka_config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

producer = KafkaProducer(
    bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS,
    value_serializer = lambda x: json.dumps(x).encode('utf-8'),
)

CRYPTOCURRENCIES = ['bitcoin', 'ethereum', 'solana']
last_sent_prices = {}

# Function to fetch data from CoinGecko API
def fetch_crypto_data():
    """
    Fetch current market data for selected cryptocurrencies from CoinGecko API.
    Returns a list of dictionaries, one per cryptocurrency.
    """
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'ids': ','.join(CRYPTOCURRENCIES),
        'order': 'market_cap_desc',
        'per_page': len(CRYPTOCURRENCIES),
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '1h,24h',
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return []

# Main loop to send data to Kafka
def stream_to_kafka(interval_sec=10):
    """
    Fetches data from API and sends it to Kafka at fixed intervals.
    """
    print(f"Starting producer... sending data every {interval_sec} seconds")
    while True:
        crypto_data = fetch_crypto_data()
        for item in crypto_data:
            symbol = item['symbol']
            current_price = item['current_price']
            
            if abs(last_sent_prices.get(symbol, 0) - current_price) < 0.01:
                continue

            last_sent_prices[symbol] = current_price
        
            record = {
                'symbol': symbol,
                'name': item['name'],
                'price_usd': current_price,
                'market_cap': item['market_cap'],
                'volume': item['total_volume'],
                'timestamp': item['last_updated'],
                'change_1h': item.get('price_change_percentage_1h_in_currency'),
                'change_24h': item.get('price_change_percentage_24h_in_currency'),
            }

            producer.send(KAFKA_TOPIC, value=record)
            print(f"Sent to Kafka: {record}")

        time.sleep(interval_sec)

if __name__ == "__main__":
    stream_to_kafka(interval_sec=30)