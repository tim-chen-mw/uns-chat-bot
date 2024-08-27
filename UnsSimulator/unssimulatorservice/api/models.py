"""Models exposed via the API. These should be changed with care to not break API compatibility."""

from pydantic import BaseModel, Json
from typing import Any

class ConversationRequest(BaseModel):
    """A model that represents the conversation input"""
    message : str
    conversation_id : str

class ConversationResponse(BaseModel):
    """A model for the conversation response"""
    conversation_id: str
    response_message:str
    error_message :str
