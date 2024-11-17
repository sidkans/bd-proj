import threading
import time
from uuid import uuid4
from datetime import datetime
import logging
from utils.models import RegistrationMessage, HeartbeatMessage
from log_system.accumulator import LogAccumulator
from log_system.kafka_client import KafkaProducer


class BaseService:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.node_id = str(uuid4())
        self.kafka_producer = KafkaProducer()
        self.log_accumulator = LogAccumulator(service_name, self.node_id)
        self.logger = self.log_accumulator.logger
        self._register_service()
        self._start_heartbeat()

    def _register_service(self):
        registration = RegistrationMessage(
            node_id=self.node_id,
            message_type="REGISTRATION",
            service_name=self.service_name,
        )
        self.kafka_producer.send_heartbeat(registration)

    def _send_heartbeat(self):
        while True:
            heartbeat = HeartbeatMessage(node_id=self.node_id, message_type="HEARTBEAT")
            self.kafka_producer.send_heartbeat(heartbeat)
            time.sleep(10)  # Send heartbeat every 10 seconds

    def _start_heartbeat(self):
        thread = threading.Thread(target=self._send_heartbeat, daemon=True)
        thread.start()

    def start(self):
        raise NotImplementedError("Service must implement start method")
