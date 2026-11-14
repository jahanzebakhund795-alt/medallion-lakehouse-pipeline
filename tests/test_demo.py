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
        self.assertEqual(result['gold'],{'WEST':200})
        self.assertEqual(len(result['quarantine']),1)
        self.assertEqual(len(result['bronze']),4)
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['records'] = [{'id':'a','region':'west','cents':'-1','version':1}, {}]
        output = run(data)
        self.assertEqual(output['gold'], {})
        self.assertEqual(len(output['quarantine']), 2)


if __name__ == '__main__':
    unittest.main()
