import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import ToolMessage, AIMessageChunk
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import AzureChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from models import ChatInput
from sub_chat import combine_chunks, sub_llm_call
from config.config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_ENDPOINT

from config.logger import logger

logger.info("Starting LangChain server...")

app = FastAPI(
    title="Consultant Chatbot",
    root_path="/chat"
)

session_store = {}


def history_by_session_id(session_id) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{human_input}"),
    ]
)

chat = AzureChatOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
    temperature=0,
    streaming=True
)

chat_with_tools = chat.bind_tools([sub_llm_call])

chain = prompt | chat_with_tools

chain_with_history = RunnableWithMessageHistory(
    chain,
    history_by_session_id,
    input_messages_key="human_input",
    history_messages_key="history",
).with_types(input_type=ChatInput)


async def process_tool_calls(response, session_id):
    """
    Processes tool calls in the response and invokes the corresponding tools with the tool call arguments.

    Args:
        response: The response containing tool calls.
        session_id (str): The ID of the chat session.

    Yields:
        AIMessageChunk: The result of the tool call processing.
    """
    for tool_call in response.tool_calls:
        # Select the tool to call based on the tool call name
        try:
            selected_tool = {
                "sub_llm_call": sub_llm_call,
            }[tool_call["name"].lower()]
        except Exception as e:
            logger.exception(e)
            continue

        # Invoke the selected tool with the tool call arguments
        logger.debug("Main Context: calling tool %s with args: %s", tool_call['name'], tool_call['args'])
        try:
            chunks = []
            async for chunk in selected_tool.astream(tool_call["args"]):
                async for sub_chunk in chunk:
                    chunks.append(sub_chunk)
                    if sub_chunk.content:
                        yield sub_chunk

            result = combine_chunks(chunks)

            history_by_session_id(session_id).messages.append(ToolMessage("Sub-LLM Call successfull:", tool_call_id=tool_call["id"]))
            history_by_session_id(session_id).add_message(result)

        except Exception as e:
            logger.exception(e)
            yield AIMessageChunk(f"An error occurred while processing the tool call: {tool_call['name']}")


async def stream_result(chat_input: ChatInput):
    """
    Streams the result of the chat input processing.

    Args:
        chat_input (ChatInput): The input data for the chat session.

    Yields:
        str: The chunks of the streaming response.
    """
    current_session_id = chat_input.session_id

    try:

        logger.debug("Starting streaming response...")

        chunks = []

        async for chunk in chain_with_history.astream(chat_input.dict(), {"configurable": {"session_id": current_session_id}}):
            chunks.append(chunk)
            if chunk.content:
                yield chunk.content

        result = combine_chunks(chunks)

        if result.tool_calls:
            async for tool_chunk in process_tool_calls(result, current_session_id):
                if tool_chunk.content:
                    yield tool_chunk.content

    except Exception as e:
        logger.exception(e)

        if isinstance(e):
            yield e.args[0]
        else:
            yield "I'm sorry, but I'm having trouble processing your request. Please try again."

    logger.debug("Finished streaming response.")


@app.post("/stream")
async def chat_stream(chat_input: ChatInput):
    """
    Handles the POST request for the chat stream endpoint.

    Args:
        chat_input (ChatInput): The input data for the chat session.

    Returns:
        StreamingResponse: The streaming response with the chat output.
    """
    logger.debug("Received chat input: %s", chat_input.human_input)
    return StreamingResponse(stream_result(chat_input), media_type="application/stream+json")


def main():
    """
    The main entry point of the application. Starts the Uvicorn server.
    """
    try:
        logger.info("Starting Uvicorn server...")
        uvicorn.run(app, host="0.0.0.0", port=8001, root_path="/chat")

    except KeyboardInterrupt:
        logger.info("Shut down complete!")


if __name__ == "__main__":
    main()
