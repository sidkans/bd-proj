from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer(
    "logs",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

es = Elasticsearch(["localhost:9200"])

for message in consumer:
    print("\nReceived Message:")
    print(json.dumps(message.value, indent=4))

    es.index(index="logs", document=message.value)

    response = es.search(
        index="logs",
        body={
            "query": {"match": {"message_type": message.value.get("message_type")}},
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": 3,
        },
    )
    print("\nLast 3 indexed messages:")
    print(json.dumps(response["hits"]["hits"], indent=4))
    print("-" * 50)
