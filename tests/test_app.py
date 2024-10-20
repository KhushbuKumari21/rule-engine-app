import unittest
import json
from app import app

class FlaskAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def test_create_rule(self):
        response = self.app.post('/api/rules', json={"rule_string": "age > 30"})
        self.assertEqual(response.status_code, 201)

    def test_create_rule_no_rule_string(self):
        response = self.app.post('/api/rules', json={})
        self.assertEqual(response.status_code, 400)

    def test_combine_rules(self):
        response = self.app.post('/api/combine_rules', json={
            "rules": [
                "age > 30",
                "income < 50000",
                "department == \"IT\""
            ]
        })
        self.assertEqual(response.status_code, 201)

    def test_evaluate_rule(self):
        response = self.app.post('/api/evaluate_rule', json={
            "rule_string": "age > 30",
            "user_data": {"age": 35}
        })
        self.assertEqual(response.status_code, 200)

    def test_evaluate_rule_no_user_data(self):
        response = self.app.post('/api/evaluate_rule', json={"rule_string": "age > 30"})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
