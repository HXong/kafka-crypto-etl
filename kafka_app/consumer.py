import json
from kafka import KafkaConsumer
from config_app.kafka_config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from db.db_utils import insert_price_record

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer = lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'crypto-consumer-group',
)

for message in consumer:
    data = message.value
    print(f"Received message: {data}")

    insert_price_record(data)