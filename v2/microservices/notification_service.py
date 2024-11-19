from base_service import BaseService
import random
import time
from fluent import sender, event

# Fluentd setup
sender.setup('fluentd-service', host='fluentd', port=24224)


class NotificationService(BaseService):
    def __init__(self):
        super().__init__("NotificationService")

    def send_notification(self, recipient: str, message: str):
        start_time = time.time()

        # Simulate processing time
        processing_time = random.uniform(0.2, 3.0)
        time.sleep(processing_time)

        response_time = int((time.time() - start_time) * 1000)

        # Simulate different scenarios
        if processing_time > 2.5:
            self.logger.warning(
                f"Notification to {recipient} delayed",
                extra={
                    "response_time_ms": response_time,
                    "threshold_limit_ms": 2500,
                },
            )
        elif random.random() < 0.1:  # 10% chance of error
            try:
                raise Exception("Notification gateway error")
            except Exception as e:
                self.logger.error(
                    f"Failed to send notification to {recipient}",
                    exc_info=True,
                    extra={"error_code": "NOTIFICATION_ERROR"},
                )
        else:
            self.logger.info(
                f"Notification sent to {recipient}",
                extra={"message": message, "response_time_ms": response_time},
            )

    def start(self):
        while True:
            recipient = f"user{random.randint(100, 999)}@example.com"
            message = f"Hello, this is your notification {random.randint(1, 100)}"
            self.send_notification(recipient, message)
            time.sleep(random.uniform(2.0, 6.0))


if __name__ == "__main__":
    service = NotificationService()
    service.start()
