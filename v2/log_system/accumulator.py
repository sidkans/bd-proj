import logging
import json
import requests
from logging.handlers import SysLogHandler

class LogAccumulator:
    def __init__(self, fluentd_host="localhost", fluentd_port=24224):
        """
        Initialize the Log Accumulator with Fluentd configuration.
        
        :param fluentd_host: Host where Fluentd is running
        :param fluentd_port: Port on which Fluentd is listening
        """
        self.fluentd_host = fluentd_host
        self.fluentd_port = fluentd_port

        # Set up logging
        self.logger = logging.getLogger("fluentd")
        self.logger.setLevel(logging.INFO)

        # Use SysLogHandler for Fluentd integration
        syslog_handler = SysLogHandler(address=(fluentd_host, fluentd_port))
        syslog_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(syslog_handler)

    def log(self, level, service, message, metadata=None):
        """
        Send a log message to Fluentd.

        :param level: Log level (e.g., 'INFO', 'ERROR', etc.)
        :param service: Name of the service generating the log
        :param message: Log message
        :param metadata: Additional metadata as a dictionary
        """
        log_entry = {
            "level": level,
            "service": service,
            "message": message,
            "metadata": metadata or {},
        }

        try:
            # Convert log entry to JSON
            log_json = json.dumps(log_entry)

            # Log through Fluentd
            self.logger.info(log_json)
        except Exception as e:
            print(f"Error logging to Fluentd: {e}")

    def log_error(self, service, message, metadata=None):
        """
        Convenience method to log errors.
        """
        self.log(level="ERROR", service=service, message=message, metadata=metadata)

    def log_info(self, service, message, metadata=None):
        """
        Convenience method to log informational messages.
        """
        self.log(level="INFO", service=service, message=message, metadata=metadata)

    def log_warn(self, service, message, metadata=None):
        """
        Convenience method to log warnings.
        """
        self.log(level="WARNING", service=service, message=message, metadata=metadata)
