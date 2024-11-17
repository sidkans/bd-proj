from kafka import KafkaProducer as KafkaProducerLib
from kafka import KafkaConsumer as KafkaConsumerLib
import json
from common.utils import DateTimeEncoder
from common.models import BaseMessage


class KafkaProducer:
    def __init__(self, bootstrap_servers="localhost:9092"):
        self.producer = KafkaProducerLib(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, cls=DateTimeEncoder).encode(
                "utf-8"
            ),
        )

    def send_log(self, message: BaseMessage):
        self.producer.send("logs", message.dict())

    def send_heartbeat(self, message: BaseMessage):
        self.producer.send("heartbeats", message.dict())


class KafkaConsumer:
    def __init__(self, topics, group_id, bootstrap_servers="localhost:9092"):
        self.consumer = KafkaConsumerLib(
            topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
