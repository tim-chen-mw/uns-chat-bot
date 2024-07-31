from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import BaseModel
import uvicorn

from src.backend.chat_bot import AgentManager
from src.utils import logger


agent_manager = AgentManager()
agent = agent_manager.agent


async def stream(human_message, session_id, callbacks=None):
    async def event_generator():
        inputs = [("user", human_message)]
        # Future session_id
        async for event in agent.astream_events(
            {"messages": inputs},
            {"configurable": {"thread_id": session_id}, "callbacks": callbacks},
            version="v1",
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield content
            elif kind == "on_tool_start":
                logger.info(
                    f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
                )
            elif kind == "on_tool_end":
                logger.info(f"Done tool: {event['name']}")
                logger.info(f"Tool output was: {event['data'].get('output')}")

    return StreamingResponse(event_generator(), media_type="text/event-stream")


app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/stream")
async def chat_stream(request: ChatRequest):
    return await stream(request.message, request.session_id)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
