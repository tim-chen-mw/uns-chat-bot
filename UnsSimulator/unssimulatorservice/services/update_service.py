from threading import Thread
from ..services import datasimulator
from ..mqtt.publisher import MqttPublisher
from ..util import settings
from datetime import datetime
import json

class UnsUpdateService(Thread):
    def __init__(self, event, mqtt: MqttPublisher):
        super().__init__()
        self.event = event
        self._mqtt = mqtt
        self._timestamp = datetime.now()

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
    
    def run(self):
        while not self.event.is_set():
            time_elapsed = datetime.now()-self._timestamp
            publish_period = settings.UNS_PUBLISH_PERIOD
            if time_elapsed.total_seconds() > publish_period:
                
                dough_prep_data = datasimulator.generate_dough_prep_data()
                self.update_uns(dough_prep_data)
                print('Doug Prep data published')

                topping_and_freezing_data = datasimulator.generate_topping_and_freezing_data()
                self.update_uns(topping_and_freezing_data)
                print('Topping and Freezing data published')

                packaging_data = datasimulator.generate_packaging_data()
                self.update_uns(packaging_data)
                print('Packaging data published')
                
                self._timestamp = datetime.now()

