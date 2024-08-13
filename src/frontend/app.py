import time
from typing import TypeVar, Callable
import inspect
import uuid
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.scriptrunner import get_script_run_ctx, add_script_run_ctx
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

from frontend.chat_client import ChatClient
from utils.config import CHAT_API_URL

T = TypeVar("T")

client = ChatClient(CHAT_API_URL)


# Workaround for compatibility between StreamlitCallback and LangGraph
def get_streamlit_cb(parent_container: DeltaGenerator):
    def decor(fn: Callable[..., T]) -> Callable[..., T]:
        ctx = get_script_run_ctx()

        def wrapper(*args, **kwargs) -> T:
            add_script_run_ctx(ctx=ctx)
            return fn(*args, **kwargs)

        return wrapper

    st_cb = StreamlitCallbackHandler(parent_container=parent_container)

    for name, fn in inspect.getmembers(st_cb, predicate=inspect.ismethod):
        if name.startswith("on_"):
            setattr(st_cb, name, decor(fn))

    return st_cb


st.set_page_config(
    page_title="UNS Chatbot", page_icon="../res/icon.png", layout="centered"
)

st.title("UNS Chatbot")

# Generate or retrieve session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.write(f"**Session ID:** {st.session_state.session_id}")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # try:
    #     st_callback = get_streamlit_cb(st.container())
    #     response = client.stream(prompt)
    # except Exception as e:
    #     logger.error(e)
    #     response = "I'm sorry, but I'm having trouble processing your request. Please try again."
    # # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     st.markdown(response)
    # # Add assistant response to chat history
    # st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = ""
        response_stream = client.stream(prompt, session_id=st.session_state.session_id)

        with st.spinner("Thinking..."):
            for chunk in response_stream:
                time.sleep(0.02)
                response += chunk
                message_placeholder.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
