from base_service import BaseService
import random
import time
from fluent import sender, event

# Fluentd setup
sender.setup('fluentd-service', host='fluentd', port=24224)


class PaymentService(BaseService):
    def __init__(self):
        super().__init__("PaymentService")

    def process_payment(self, amount: float):
        start_time = time.time()

        # Simulate processing time
        processing_time = random.uniform(0.1, 2.0)
        time.sleep(processing_time)

        response_time = int((time.time() - start_time) * 1000)

        # Simulate different scenarios
        if processing_time > 1.5:
            self.logger.warning(
                "Payment processing slower than threshold",
                extra={"response_time_ms": response_time, "threshold_limit_ms": 1500},
            )
        elif random.random() < 0.1:  # 10% chance of error
            try:
                raise Exception("Payment gateway error")
            except Exception as e:
                self.logger.error(
                    "Payment processing failed",
                    exc_info=True,
                    extra={"error_code": "PAYMENT_ERROR"},
                )
        else:
            self.logger.info(f"Successfully processed payment of ${amount}")

    def start(self):
        while True:
            self.process_payment(random.uniform(10.0, 1000.0))
            time.sleep(random.uniform(1.0, 5.0))
