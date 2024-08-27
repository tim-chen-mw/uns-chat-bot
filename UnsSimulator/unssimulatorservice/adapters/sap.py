from dataclasses import dataclass
from dataclasses_json import dataclass_json


class SAPAdapter:
    """A dummy to show where adapters are placed in the code structure"""
    pass


@dataclass_json
@dataclass
class SomeSAPModel:
    """A dummy model for SAP"""
    foo: str
    bar: str
