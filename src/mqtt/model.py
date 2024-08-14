"""Models exposed via the MQTT interface. This needs to be changed with care to remain compatible."""

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pydantic import BaseModel


@dataclass_json
@dataclass
class SomeMqttMessage:
    msg: str


class InternalMqttMessage(BaseModel):
    topic: str
    payload: str
