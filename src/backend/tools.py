from langchain.tools import tool


@tool
def generate_name():
    """Generate a name for the chatbot."""
    return "UNS Bot"
