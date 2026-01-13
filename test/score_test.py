import unittest
import tempfile

from tools.score import * 

class TestScore(unittest.TestCase):
    def test_result_computation(self):
        expected = "Др. Јован 12.0 дин ."
        actual = "Др . Јован 12 . 0 дин ."
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as expected_file:
            expected_file.write(expected)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as actual_file:
            actual_file.write(actual)

        total, tp = process_file_pair(expected_file.name, actual_file.name)
        
        os.remove(expected_file.name)
        os.remove(actual_file.name)

        self.assertEqual(5, total)
        self.assertEqual(3, tp)




if __name__ == '__main__':
    unittest.main()
