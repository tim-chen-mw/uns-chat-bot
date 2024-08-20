from pydantic import BaseModel, Field


class ChatInput(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Represents the input data for a chat session.

    Attributes:
        human_input (str): The human input to the chat system.
        session_id (str): The ID of the chat session.
    """
    human_input: str = Field(
        ...,
        description="The human input to the chat system.",
        extra={"widget": {"type": "chat", "input": "human_input"}},
    )

    session_id: str


class SubLlmToolCall(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Represents a call to a sub-language model tool.

    Attributes:
        chat_input (str): The chat input from the user.
        model (str): The model to use for the sub-language model. Valid values are 'trivial' and 'complex'.
    """
    chat_input: str = Field(description="The chat input from the user.")
