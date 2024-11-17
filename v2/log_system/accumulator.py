import logging
from logging import LogRecord
from utils.models import LogMessage, ErrorLogMessage, WarnLogMessage
from kafka_client import KafkaProducer


class LogAccumulator:
    def __init__(self, service_name: str, node_id: str):
        self.service_name = service_name
        self.node_id = node_id
        self.kafka_producer = KafkaProducer()
        self._setup_logging()

    def _setup_logging(self):
        logger = logging.getLogger(self.service_name)
        logger.setLevel(logging.INFO)
        handler = LoggingHandler(self)
        logger.addHandler(handler)
        self.logger = logger

    def process_log(self, record: LogRecord):
        if record.levelno >= logging.ERROR:
            message = ErrorLogMessage(
                node_id=self.node_id,
                message_type="LOG",
                log_level="ERROR",
                message=record.getMessage(),
                service_name=self.service_name,
                error_details={
                    "error_code": getattr(record, "error_code", "UNKNOWN"),
                    "error_message": (
                        str(record.exc_info[1])
                        if record.exc_info
                        else record.getMessage()
                    ),
                },
            )
        elif record.levelno >= logging.WARNING:
            message = WarnLogMessage(
                node_id=self.node_id,
                message_type="LOG",
                log_level="WARN",
                message=record.getMessage(),
                service_name=self.service_name,
                response_time_ms=getattr(record, "response_time_ms", 0),
                threshold_limit_ms=getattr(record, "threshold_limit_ms", 0),
            )
        else:
            message = LogMessage(
                node_id=self.node_id,
                message_type="LOG",
                log_level="INFO",
                message=record.getMessage(),
                service_name=self.service_name,
            )

        self.kafka_producer.send_log(message)


class LoggingHandler(logging.Handler):
    def __init__(self, accumulator: LogAccumulator):
        super().__init__()
        self.accumulator = accumulator

    def emit(self, record):
        self.accumulator.process_log(record)
