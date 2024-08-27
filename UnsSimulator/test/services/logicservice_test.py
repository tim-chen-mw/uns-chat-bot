import unittest
from templateservice.services.logicservice import LogicService


class LogicServiceTest(unittest.TestCase):
    
    def test_add(self):
        under_test = LogicService()
        self.assertEqual(3, under_test.add(1, 2))

        # Also think to test edge cases
        self.assertEqual(1, under_test.add(-1, 2))

        # It is also possible to test for thrown exceptions
        with self.assertRaises(TypeError) as context:
            under_test.add(None, 2)
        # The context gives access to the thrown exception to verify details
        self.assertTrue("unsupported operand type(s) for +: 'NoneType' and 'int'" in str(context.exception))

    def test_transform_name(self):
        under_test = LogicService()
        self.assertEqual("foobar-transformed", under_test.transform_name("foobar"))
