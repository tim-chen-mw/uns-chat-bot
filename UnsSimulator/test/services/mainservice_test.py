import unittest
from unittest import mock
from templateservice.services.mainservice import MainService, InternalRequest
from templateservice.models.entities import SomeEntity
from templateservice.models.internalmodel import InternalMqttMessage

class MainServiceTest(unittest.TestCase):
    
    def test_do_something(self):
        # given
        mqtt_mock, db_mock, logic_mock = prepare_mocks()
        under_test = MainService(mqtt_mock, db_mock, logic_mock)
        input = InternalRequest(name="foo", a=1, desc="doesntmatter")

        # when
        result = under_test.do_something(input)

        # then
        self.assertEqual(20, result.entity_count)
        self.assertEqual("foobar", result.transformed_name)
        self.assertEqual(3, result.b)

        db_mock.get_entity_count.assert_called_once()
        logic_mock.add.assert_called_once_with(1, 2)
        logic_mock.transform_name.assert_called_once_with("foo")

    def test_handle_some_message(self):
        # given
        mqtt_mock, db_mock, logic_mock = prepare_mocks()
        under_test = MainService(mqtt_mock, db_mock, logic_mock)
        msg = InternalMqttMessage(name="foobar", description="baz")

        # when
        under_test.handle_some_message(msg)

        # then
        db_mock.persist_entity.assert_called_once_with(SomeEntity(name="foobar", is_active=True))


def prepare_mocks():
    mqtt_mock = mock.MagicMock()
    mqtt_mock.register_callback = mock.MagicMock()
    db_mock = mock.MagicMock()
    db_mock.persist_entity = mock.MagicMock()
    db_mock.get_entity_count = mock.MagicMock(return_value=20)
    logic_mock = mock.MagicMock()
    logic_mock.transform_name = mock.MagicMock(return_value="foobar")
    logic_mock.add = mock.MagicMock(return_value=3)
    return mqtt_mock, db_mock, logic_mock
