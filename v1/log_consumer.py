#!/usr/bin/env python3
from kafka import KafkaConsumer
import json

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'logs',  # Topic name
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start from the beginning of the log
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('ASCII'))
)

print("Listening for messages on 'logs' topic...")

# Listen for messages and print them
for message in consumer:
    print("Received message:", message.value)
