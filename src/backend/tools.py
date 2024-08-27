import json
from langchain.tools import tool
from config.logger import logger


@tool
def get_uns_snapshot():
    """
    Reads the mqtt snapshot file and returns the data.

    Args:

    Returns:
        dict: The uns snapshot data.
    """
    try:
        with open("mqtt_snapshot.json", 'r') as file:
            data = json.load(file)
        return json.dumps(data, indent=4)

    except Exception as e:
        logger.exception(f"Failed to read or sanitize JSON file: {e}")
        return {}
