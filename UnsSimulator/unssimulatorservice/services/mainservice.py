from .datasimulator import *
from ..mqtt.publisher import MqttPublisher
from .update_service import UnsUpdateService
from ..util import settings
from ..util import metrics
import json
import time


class MainService:
    """Some service with cool features. Acts as the main orchestration service of the app, delegates logic to other services."""

    def __init__(self, mqtt: MqttPublisher):
        self._mqtt = mqtt

    @metrics.ENDPOINT_DO_SOMETHING.time() # With this the prom library automatically tracks invocations and runtime
    def do_something(self):
        """Does something.
        Note: This service only handles objects of internal models. The API layer is responsible for translating between external and internal models.
        """
        response = self.uns
        return response
   
    def update_uns(self, simulated_data):
        """
        Periodically calls all necessary function to update the UNS
        """
        base_topic = settings.MQTT_BASE_TOPIC
        self._publish_recursive(base_topic, simulated_data)
    
    def _contains_dict(self,dictionary):
        """
        Takes a dictionary object and checks if the given dict contains further dictionaries.
        """
        value_types = []
        for value in dictionary.values():
            value_types.append(type(value))
            return dict in value_types
                
    def _publish_recursive(self, current_topic, data):
        """Recursively goes through uns data and publishes all dictionaries as json payload, that do not contain further dictionaries."""
        for sub_topic, message in data.items():
            #time.sleep(1)
            full_topic = f"{current_topic}/{sub_topic}"
            if isinstance(message, dict) and self._contains_dict(message):
                self._publish_recursive(full_topic, message)
            else:
                payload = json.dumps(message, indent=4)
                self._mqtt.publish(topic=full_topic, payload=payload, qos=1, retain=False)