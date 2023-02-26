from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from NodeWrapper import NodeWrapper
from BullyAlgorithm import Bully


class TestNodeWrapper(TestCase):
    def setUp(self) -> None:
        # Set up test variables
        self.processes = [NodeWrapper(i, [], []) for i in range(5)]
        self.node = NodeWrapper(5, self.processes, [1, 2, 3])

    def test_start_election(self):
        # Test NodeWrapper.start_election() function
        self.node.start_election()

    def test_divide_array(self):
        # Test NodeWrapper.divide_array() function
        result = self.node.divide_array()
        self.assertEqual(result, [1, 2, 3])

    def test_find_minimum(self):
        # Test NodeWrapper.find_minimum() function
        result = self.node.find_minimum()
        self.assertEqual(result, 1)

    def test_send_message(self):
        # Test NodeWrapper.send_message() function
        bully = Bully(5)
        bully.start()
        with patch('builtins.input', return_value='RESULT'):
            self.node.send_message('VICTORY', bully.coordinator)

