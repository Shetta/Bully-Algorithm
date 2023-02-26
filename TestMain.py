from unittest import TestCase
from NodeWrapper import NodeWrapper


class TestBully(TestCase):
    def setUp(self) -> None:
        # Set up test variables
        self.processes = [NodeWrapper(i, [], []) for i in range(5)]
        self.node = NodeWrapper(5, self.processes, [1, 2, 3])

    def test___init__(self):
        # Ensure that the NodeWrapper object is initialized correctly
        self.assertTrue(isinstance(self.node.process_id, int))
        self.assertTrue(isinstance(self.node.processes, list))
        self.assertTrue(isinstance(self.node.array, list))
        self.assertEqual(self.node.coordinator, None)

