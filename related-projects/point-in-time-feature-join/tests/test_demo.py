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
        self.assertEqual([r['feature_value'] for r in result['training_rows']],[10,40,None])
        self.assertEqual(result['missing_features'],1)
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        output = run({'features':[{'entity':'a','event_at':3,'available_at':8,'value':30}],
                      'labels':[{'entity':'a','at':5}]})
        self.assertIsNone(output['training_rows'][0]['feature_value'])
        data['features'][0]['available_at'] = 0
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()
