from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from BullyAlgorithm import Bully


class TestBully(TestCase):
    def test_main_valid_input(self):
        # Test Bully.main() function with valid input
        with patch('builtins.input', return_value='5'):
            self.assertEqual(Bully.main(), None)

    def test_main_invalid_input(self):
        # Test Bully.main() function with invalid input
        with patch('builtins.input', side_effect=['-1', '0', 'invalid', '3']):
            expected_output = 'Please enter a positive integer for the number of processes.\n' * 3
            with patch('sys.stdout', new=StringIO()) as output:
                Bully.main()
                self.assertEqual(output.getvalue(), expected_output)

    def test_start(self):
        # Test Bully.start() function
        bully = Bully(5)
        bully.start()

    def test_collect_results(self):
        # Test Bully.collect_results() function
        bully = Bully(5)
        results = bully.collect_results()
        self.assertTrue(isinstance(results, int))
