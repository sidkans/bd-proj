#!/usr/bin/env python3
from kafka_helper import init_producer, current_timestamp
import time

producer = init_producer()
node_id = "notification_service_node"

# Register the service on startup
registration_message = {
    "node_id": node_id,
    "message_type": "REGISTRATION",
    "service_name": "NotificationService",
    "timestamp": current_timestamp()
}
producer.send('logs', registration_message)
print("Registered Notification Service:", registration_message)

# Function to simulate log generation
def send_logs():
    log_id = 1
    while True:
        log_message = {
            "log_id": f"notification-{log_id}",
            "node_id": node_id,
            "log_level": "ERROR" if log_id % 4 == 0 else "INFO",
            "message_type": "LOG",
            "message": "Notification sent" if log_id % 4 != 0 else "Notification failed",
            "service_name": "NotificationService",
            "timestamp": current_timestamp()
        }
        producer.send('logs', log_message)
        print("Notification Log Sent:", log_message)

        # Send a heartbeat every 5 logs
        if log_id % 5 == 0:
            heartbeat_message = {
                "node_id": node_id,
                "message_type": "HEARTBEAT",
                "status": "UP",
                "timestamp": current_timestamp()
            }
            producer.send('logs', heartbeat_message)
            print("Notification Heartbeat Sent:", heartbeat_message)

        log_id += 1
        producer.flush()
        time.sleep(2)

if __name__ == "__main__":
    send_logs()
