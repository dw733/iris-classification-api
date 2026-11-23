import unittest

from app import create_app

EXAMPLE = {
    "sepal_length_cm": 5.1,
    "sepal_width_cm": 3.5,
    "petal_length_cm": 1.4,
    "petal_width_cm": 0.2,
}


class IrisApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = create_app().test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_prediction_uses_named_features(self):
        response = self.client.post("/predict", json=dict(reversed(list(EXAMPLE.items()))))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"species": "setosa"})

    def test_invalid_measurements(self):
        for value in (False, "5.1", float("nan"), float("inf"), -1, 101, 10**400):
            with self.subTest(value=value):
                response = self.client.post("/predict", json={**EXAMPLE, "sepal_length_cm": value})
                self.assertEqual(response.status_code, 400)
                self.assertIn("sepal_length_cm", response.json["error"])

    def test_missing_extra_or_malformed_input(self):
        examples = ({"sepal_length_cm": 5.1}, {**EXAMPLE, "species": "setosa"}, [5.1, 3.5, 1.4, 0.2])
        for example in examples:
            with self.subTest(example=example):
                self.assertEqual(self.client.post("/predict", json=example).status_code, 400)
        self.assertEqual(self.client.post("/predict", data="{", content_type="application/json").status_code, 400)
        self.assertEqual(self.client.post("/predict", data="Flower").status_code, 415)
