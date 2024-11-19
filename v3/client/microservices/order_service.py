from base_service import BaseService
import random
import time
import logging
import logging.handlers
import json
from datetime import datetime
from uuid import uuid4


class OrderService(BaseService):
    def __init__(self):
        super().__init__("OrderService")
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(logging.INFO)
        handler = logging.handlers.SocketHandler("localhost", 24224)
        self.logger.addHandler(handler)

    def process_order(self, order_id: str):
        start_time = time.time()
        processing_time = random.uniform(0.1, 2.0)
        time.sleep(processing_time)
        response_time = int((time.time() - start_time) * 1000)

        if processing_time > 1.5:
            self.logger.warning(
                json.dumps(
                    {
                        "log_id": str(uuid4()),
                        "node_id": self.node_id,
                        "log_level": "WARN",
                        "message_type": "LOG",
                        "message": f"Order {order_id} processing delayed",
                        "service_name": self.service_name,
                        "response_time_ms": response_time,
                        "threshold_limit_ms": 1500,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
            )
        elif random.random() < 0.1:
            try:
                raise Exception("Order processing error")
            except Exception as e:
                self.logger.error(
                    json.dumps(
                        {
                            "log_id": str(uuid4()),
                            "node_id": self.node_id,
                            "log_level": "ERROR",
                            "message_type": "LOG",
                            "message": f"Order {order_id} failed to process",
                            "service_name": self.service_name,
                            "error_details": {
                                "error_code": "ORDER_PROCESSING_ERROR",
                                "error_message": str(e),
                            },
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    )
                )
        else:
            self.logger.info(
                json.dumps(
                    {
                        "log_id": str(uuid4()),
                        "node_id": self.node_id,
                        "log_level": "INFO",
                        "message_type": "LOG",
                        "message": f"Successfully processed order {order_id}",
                        "service_name": self.service_name,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
            )

    def start(self):
        log_id = 1
        while True:
            order_id = f"order-{log_id}"
            self.process_order(order_id)
            if log_id % 5 == 0:
                heartbeat_message = {
                    "node_id": self.node_id,
                    "message_type": "HEARTBEAT",
                    "status": "UP",
                    "timestamp": datetime.utcnow().isoformat(),
                }
                self.logger.info(json.dumps(heartbeat_message))
            log_id += 1
            time.sleep(2)


if __name__ == "__main__":
    service = OrderService()
    service.start()
