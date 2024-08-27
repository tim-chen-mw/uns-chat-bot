import logging
from .client import MqttClient
from .model import SomeMqttMessage
from ..models.internalmodel import InternalMqttMessage
from ..util import metrics


class MqttPublisher:
    """Higher level adapter for MQTT. Publishes MQTT messages"""

    def __init__(self):
        self._client = MqttClient()

    def connect_and_start(self):
        """Connect to MQTT and launch client loop in the backgorund"""
        self._client.connect()
        self._client.start()

    def publish(self, topic: str, payload: str, qos=1, retain=True):
        print(f'{topic} updated')
        self._client.send_message(topic, payload, qos=qos, retain=retain)
