"""
Runtime settings of the app. 
The defaults here are aimed at locally running the service. For production deployments the environment variables need to be set externally.
"""
import os
import json
import os
#from dotenv import load_dotenv

#load_dotenv()

# MQTT
MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = int(os.environ.get("MQTT_PORT"))
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_CLIENTID = os.environ.get("MQTT_CLIENTID")
MQTT_BASE_TOPIC = os.environ.get("MQTT_BASE_TOPIC")

#UNS
UNS_PUBLISH_PERIOD = int(os.environ.get("UNS_PUBLISH_PERIOD"))

# App
LOG_MODE = os.environ.get("LOG_MODE", "plain") # allowed: plain or json
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info")

#OpenAI
OPENAI_API_KEY = os.environ.get("OPEN_AI_API_KEY")
GPT_MODEL = os.environ.get("GPT_MODEL")
CONVERSATION_EXPIRY_PERIOD = os.environ.get("CONVERSATION_EXPIRY_PERIOD")