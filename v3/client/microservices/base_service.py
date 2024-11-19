import threading
import time
from uuid import uuid4
from datetime import datetime
from kafka import KafkaProducer
import json
from schema import RegistrationMessage, HeartbeatMessage


class BaseService:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.node_id = f"{service_name}-{str(uuid4())}"
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=['kafka_broker:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self._register_service()
        self._start_heartbeat()

    def _register_service(self):
        self.registration_message = {
            "message_type": "REGISTRATION",
            "node_id": self.node_id,
            "service_name": self.service_name,
            "status": "UP",
            "timestamp": datetime.utcnow().isoformat(),
        }
        # Send registration message to Kafka
        self.kafka_producer.send('service_registry', self.registration_message)

    def _send_heartbeat(self):
        while True:
            heartbeat = {
                "message_type": "HEARTBEAT",
                "node_id": self.node_id,
                "timestamp": datetime.utcnow().isoformat(),
            }
            self.kafka_producer.send('heartbeats', heartbeat)
            time.sleep(10)

    def _start_heartbeat(self):
        thread = threading.Thread(target=self._send_heartbeat, daemon=True)
        thread.start()

    def start(self):
        raise NotImplementedError("Service must implement start method")
