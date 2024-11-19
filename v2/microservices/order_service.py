from base_service import BaseService
import random
import time
from fluent import sender, event

# Fluentd setup
sender.setup('fluentd-service', host='fluentd', port=24224)


class OrderService(BaseService):
    def __init__(self):
        super().__init__("OrderService")

    def process_order(self, order_id: str):
        start_time = time.time()

        # Simulate order processing time
        processing_time = random.uniform(0.1, 2.0)
        time.sleep(processing_time)

        response_time = int((time.time() - start_time) * 1000)

        # Simulate different order scenarios
        if processing_time > 1.5:
            self.logger.warning(
                f"Order {order_id} processing delayed",
                extra={"response_time_ms": response_time, "threshold_limit_ms": 1500},
            )
        elif random.random() < 0.1:  # 10% chance of error
            try:
                raise Exception("Order processing error")
            except Exception as e:
                self.logger.error(
                    f"Order {order_id} failed to process",
                    exc_info=True,
                    extra={"error_code": "ORDER_PROCESSING_ERROR"},
                )
        else:
            self.logger.info(f"Successfully processed order {order_id}")

    def start(self):
        log_id = 1
        while True:
            order_id = f"order-{log_id}"
            self.process_order(order_id)
            
            # Send heartbeat every 5 logs
            if log_id % 5 == 0:
                heartbeat_message = {
                    "node_id": self.node_id,
                    "message_type": "HEARTBEAT",
                    "status": "UP",
                    "timestamp": self.current_timestamp(),
                }
                self.kafka_producer.send_heartbeat(heartbeat_message)
                print("Order Heartbeat Sent:", heartbeat_message)

            log_id += 1
            time.sleep(2)


if __name__ == "__main__":
    service = OrderService()
    service.start()
