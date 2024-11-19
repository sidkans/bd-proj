from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer(
    "logs",
    bootstrap_servers=["kafka_broker:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

es = Elasticsearch(["elasticsearch_host:9200"])

for message in consumer:
    es.index(index="logs", document=message.value)
