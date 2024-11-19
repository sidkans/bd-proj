import threading
import time
from uuid import uuid4
from datetime import datetime
import logging
from schema import RegistrationMessage, HeartbeatMessage


class BaseService:
    def __init__(self, service_name: str):
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
            time.sleep(10)

    def _start_heartbeat(self):
        thread = threading.Thread(target=self._send_heartbeat, daemon=True)
        thread.start()

    def start(self):
        raise NotImplementedError("Service must implement start method")
