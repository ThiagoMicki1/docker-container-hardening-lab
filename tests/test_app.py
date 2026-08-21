import unittest

from app.app import create_app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_index_returns_ok(self):
        response = self.client.get("/")
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["status"], "ok")

    def test_health_endpoint(self):
        response = self.client.get("/health")
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["status"], "healthy")

    def test_config_demo_does_not_return_secret(self):
        response = self.client.get("/config-demo")
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("secret", body)
        self.assertFalse(body["debug_mode"])


if __name__ == "__main__":
    unittest.main()
