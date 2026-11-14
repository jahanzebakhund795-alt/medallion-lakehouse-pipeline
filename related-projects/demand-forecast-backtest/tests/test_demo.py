import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertEqual(result['predictions'][0]['moving_average'],14.0)
        self.assertEqual(result['predictions'][0]['actual'],16)
        self.assertGreaterEqual(result['moving_average_mae'],0)
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        modified = copy.deepcopy(data)
        modified['demand'][-1] = 10000
        self.assertEqual(run(data)['predictions'][0], run(modified)['predictions'][0])
        data['window'] = 99
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()
