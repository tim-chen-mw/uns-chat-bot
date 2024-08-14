from typing import AsyncGenerator
from langchain.tools import tool
from langchain_core.messages import ToolMessage, AIMessageChunk
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from models import SubLlmToolCall
from tools import generate_name
from config.config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_ENDPOINT
from config.logger import logger


def combine_chunks(chunks):
    """Combine a list of streamed chunks into a single result."""
    if (len(chunks) == 0):
        return None

    if (len(chunks) == 1):
        return chunks[0]

    result = chunks[0] + chunks[1]
    for stored_chunk in chunks[2:]:
        result += stored_chunk

    return result


def get_complex_chain():
    trivial_llm_system_prompt = "You are a helpful assistant"
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", trivial_llm_system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    trivial_chat_instance = AzureChatOpenAI(
        openai_api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
        temperature=0,
        streaming=True
    )

    trivial_llm_tools = [generate_name]

    trivial_chat_instance_with_tools = trivial_chat_instance.bind_tools(trivial_llm_tools)

    return prompt | trivial_chat_instance_with_tools


def get_trivial_chain():
    trivial_llm_system_prompt = "You are a helpful assistant"
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", trivial_llm_system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    trivial_chat_instance = AzureChatOpenAI(
        openai_api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
        temperature=0,
        streaming=True
    )

    trivial_llm_tools = [generate_name]

    trivial_chat_instance_with_tools = trivial_chat_instance.bind_tools(trivial_llm_tools)

    return prompt | trivial_chat_instance_with_tools


async def process_tool_calls(response, chat_history, chain):
    logger.debug("Processing tool calls...")
    for tool_call in response.tool_calls:
        # Select the tool to call based on the tool call name
        logger.debug("Sub Context: starting tool call %s...", tool_call["name"])
        try:
            selected_tool = {
                "generate_name": generate_name,
            }[tool_call["name"].lower()]
        except Exception as e:
            logger.exception(e)
            continue

        # Invoke the selected tool with the tool call arguments
        logger.debug("Sub Context: calling tool %s with args: %s", tool_call['name'], tool_call['args'])
        tool_output = None
        try:
            tool_output = await selected_tool.ainvoke(tool_call["args"])
            logger.debug("Sub Context: tool call %s finished...", tool_call["name"])
        except Exception as e:
            logger.exception(e)
            tool_output = f"An error occurred while processing the tool call: {tool_call['name']}"

        logger.debug("Adding tool output to chat history: %s", tool_call['id'])
        chat_history.add_message(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

    # Streaming the chain again with the updated message history
    logger.debug("Starting stream after tool calls...")
    chunks = []

    async for chunk in chain.astream({"messages": chat_history.messages}):
        if (chunk.tool_call_chunks):
            chunks.append(chunk)
        else:
            chunks.append(chunk)
            yield chunk

    result = combine_chunks(chunks)
    if (result.tool_calls):
        chat_history.add_message(result)
        logger.debug("Tool calls found in result. Processing tool calls...")
        async for tool_chunk in process_tool_calls(result, chat_history, chain):
            yield tool_chunk


@tool(args_schema=SubLlmToolCall)
async def sub_llm_call(chat_input: str, model: str) -> AsyncGenerator[AIMessageChunk, None]:
    """
    Calls a sub llm to process the user's request. The sub llm can handle anything that is related to employee profile data.
    It takes the current user chat input and returns an async generator object iterable to retrieve chunks of the response from the sub llm.
    The complex model has the tools "perform_semantic_search" and "get_employee_profiles" built in.
    The trivial model only has the tool "get_employee_profiles" built in.
    The trivial model should only be used for trivial tasks like summarizing or translating a profile or parts of it.

    Args:
        chat_input (str): The chat input from the user.
        model (str): The model to use for the sub llm. Valid values are "trivial" and "complex".

    Returns:
        response: An async generator object that can be iterated to retrieve chunks of the sub llms response.
    """

    try:
        chat_history = ChatMessageHistory()
        chunks = []

        logger.info("Calling sub-LLM with %s model...", model)

        if (model == "trivial"):
            chain = get_trivial_chain()
        elif (model == "complex"):
            chain = get_complex_chain()
        else:
            raise ValueError(f"Invalid model passed to sub_llm_call: {model}")

        logger.debug("Sub Context: Chain initalized...")
        logger.debug("Adding user message to chat history...")
        chat_history.add_user_message(chat_input)
        logger.debug("User message added to chat history...")

        logger.debug("Streaming subllm chain with chat history...")
        async for chunk in chain.astream({"messages": chat_history.messages}):
            chunks.append(chunk)
            if (chunk.content):
                yield chunk

        result = combine_chunks(chunks)
        logger.debug("Finished streaming sub-LLM chain.")

        logger.debug("Adding result to chat history...")
        chat_history.add_message(result)
        logger.debug("Finished Adding result to chat history")
        logger.debug("Checking if there are any tool calls in the result...")
        
        if (result.tool_calls):
            logger.debug("Tool calls found in result. Processing tool calls...")
            async for tool_chunk in process_tool_calls(result, chat_history, chain):
                yield tool_chunk

    except Exception as e:
        logger.exception(e)
        yield AIMessageChunk("I'm sorry, but I'm having trouble processing your request. Please try again.")
