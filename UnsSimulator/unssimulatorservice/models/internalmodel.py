"""Models used internally between the services. These are not exposed via the API so can be changed anytime."""

from pydantic import BaseModel, Json
from typing import Any

class InternalRequest(BaseModel):
    message: str
    conversation_id: str
    
class InternalResponse(BaseModel):
    conversation_id: str
    response_message:str
    error_message : str

class InternalMqttMessage(BaseModel):
    topic: str
    payload: str

