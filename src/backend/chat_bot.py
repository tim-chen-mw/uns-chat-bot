from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint import MemorySaver
from langgraph.checkpoint.base import empty_checkpoint, BaseCheckpointSaver
from langgraph.prebuilt import create_react_agent
from src.backend.tools import generate_name
from src.utils import logger
from src.utils.config import AZURE_OPENAI_DEPLOYMENT_NAME


class AgentManager:
    def __init__(self):
        self.model = AzureChatOpenAI(
            azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.4,
            streaming=True,
        )
        self.prompt = "You are a helpful assistant."
        self.tools = [generate_name]
        self.memory = MemorySaver()
        self.agent = self.create_agent()

    def create_agent(self):
        return create_react_agent(
            self.model,
            self.tools,
            messages_modifier=self.prompt,
            checkpointer=self.memory,
        )

    def clear_memory(
        self, memory_to_clear: BaseCheckpointSaver, session_id: str
    ) -> None:
        checkpoint = empty_checkpoint()
        memory_to_clear.put(
            config={"configurable": {"thread_id": session_id}},
            checkpoint=checkpoint,
            metadata={},
        )

    def clear_chat_history(self, session_id):
        self.clear_memory(self.memory, session_id)
        logger.info("Chat history cleared")
