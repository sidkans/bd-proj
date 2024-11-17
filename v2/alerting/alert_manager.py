from kafka import KafkaConsumer
import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict


class AlertManager:
    def __init__(self):
        self.logger = logging.getLogger("AlertManager")
        self.last_heartbeats = defaultdict(datetime)
        self._setup_consumer()

    def _setup_consumer(self):
        self.consumer = KafkaConsumer(
            "logs",
            "heartbeats",
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            group_id="alert_manager",
        )

    def _check_heartbeats(self):
        current_time = datetime.utcnow()
        for node_id, last_heartbeat in self.last_heartbeats.items():
            if current_time - last_heartbeat > timedelta(seconds=30):
                self.logger.error(
                    f"Node {node_id} may have failed! Last heartbeat: {last_heartbeat}"
                )

    def process_message(self, message):
        data = message.value

        if data["message_type"] == "HEARTBEAT":
            self.last_heartbeats[data["node_id"]] = datetime.utcnow()
            self._check_heartbeats()

        elif data["message_type"] == "LOG":
            if data.get("log_level") in ["ERROR", "WARN"]:
                self.logger.warning(
                    f"Critical log from {data['service_name']} (Node: {data['node_id']}): "
                    f"{data.get('message', '')}"
                )

    def start(self):
        for message in self.consumer:
            self.process_message(message)
