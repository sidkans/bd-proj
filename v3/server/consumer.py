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

es = Elasticsearch(["http://localhost:9200"])

# for message in consumer:
#     es.index(index="logs", document=message.value)

for message in consumer:
    print(f"Message: {message.value}")
    es.index(index="logs", document=message.value)

    response = es.search(
        index="logs",
        body={"query": {"match": {"message_type": message.value.get("message_type")}}},
    )
    print(f"Indexed message: {response['hits']['hits']}")
