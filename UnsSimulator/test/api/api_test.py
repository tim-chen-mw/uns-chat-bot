import unittest
from unittest import mock
from fastapi.testclient import TestClient
from templateservice.services.mainservice import MainService
from templateservice.services.logicservice import LogicService
from templateservice.api.app import create_app


class ApiTest(unittest.TestCase):
    
    def test_some_endpoint(self):
        # given
        mqtt_mock, db_mock = prepare_mocks()
        mainservice = MainService(mqtt_mock, db_mock, LogicService())
        app = create_app(mainservice)
        client = TestClient(app)
        
        # when
        response = client.post("/api/someendpoint", json={"name": "foobar", "a": 2})
        
        # then
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual("foobar-transformed", data["name"])
        self.assertEqual(20, data["entity_count"])


def prepare_mocks():
    mqtt_mock = mock.MagicMock()
    mqtt_mock.register_callback = mock.MagicMock()
    db_mock = mock.MagicMock()
    db_mock.get_entity_count = mock.MagicMock(return_value=20)
    return mqtt_mock, db_mock
