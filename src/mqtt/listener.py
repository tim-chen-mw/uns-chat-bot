import logging

from src.mqtt.model import InternalMqttMessage
from .client import MqttClient


class MqttListener:
    """Higher level adapter for MQTT. Receives MQTT messages and routes them to a callback.
    If needed routing to different services can be implemented here"""

    def __init__(self):
        self._client = MqttClient()

    def connect_and_start(self):
        """Connect to MQTT and launch client loop in the backgorund"""
        self._client.connect(self._message_callback)
        self._client.start()

    def register_some_message_callback(self, callback):
        """Register the callback for SomeMqttMessage"""
        self._callback = callback

    def _message_callback(self, topic: str, payload: str):
        """Handle an incoming message"""
        try:
            payload = payload.decode('utf-8')
            topic = topic
        except Exception as ex:
            logging.error("Could not parse json message from mqtt topic %s: %s", topic, ex)
            return
        # Map to internal model
        mapped = _map_message(topic, payload)

        self._callback(mapped)


def _map_message(topic, payload) -> InternalMqttMessage:
    """Map the external mqtt message model to the internal model"""
    return InternalMqttMessage(topic=topic, payload=payload)


