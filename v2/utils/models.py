from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4


class BaseMessage(BaseModel):
    node_id: str
    message_type: str
    timestamp: datetime = datetime.utcnow()


class RegistrationMessage(BaseMessage):
    service_name: str
    status: str = "UP"


class HeartbeatMessage(BaseMessage):
    status: str = "UP"


class LogMessage(BaseMessage):
    log_id: str = str(uuid4())
    log_level: str
    message: str
    service_name: str


class ErrorLogMessage(LogMessage):
    error_details: Dict[str, str]


class WarnLogMessage(LogMessage):
    response_time_ms: int
    threshold_limit_ms: int
