"""Models exposed via the MQTT interface. This needs to be changed with care to remain compatible."""

from dataclasses import dataclass


@dataclass
class SomeMqttMessage:
    msg: str