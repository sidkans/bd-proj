from kafka import KafkaProducer
import json
import time

# Initialize a Kafka producer
def init_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda m: json.dumps(m).encode("ASCII")
    )

# Generate a timestamp
def current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")