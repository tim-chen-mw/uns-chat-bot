import os

# Azure OpenAI
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_TEMPERATURE = os.getenv("AZURE_OPENAI_TEMPERATURE") or 0
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Chat API
CHAT_API_URL = os.getenv("CHAT_API_URL")

# MQTT
MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = os.environ.get("MQTT_PORT")
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_CLIENTID = os.environ.get("MQTT_CLIENTID")
MQTT_TOPICS = os.environ.get("MQTT_TOPICS")

# MQTT Broker
brokerAddress = os.getenv("brokerAddress")
borkerPort = os.getenv("borkerPort")
brokerUsername = os.getenv("brokerUsername")
brokerPassword = os.getenv("brokerPassword")
