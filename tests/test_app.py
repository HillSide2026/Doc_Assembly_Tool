import tempfile
import unittest
from pathlib import Path

import app as app_module


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app_module.app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.temp_dir = tempfile.TemporaryDirectory()
        app_module.OUTPUT_DIR = Path(self.temp_dir.name)
        app_module.OUTPUT_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_form_contains_fields(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        for field_name in [
            "client_name",
            "client_type",
            "matter_type",
            "payment_method",
            "matter_description",
            "instructing_officer_name",
            "retainer_amount",
        ]:
            self.assertIn(field_name, body)

    def test_requires_instructing_officer_for_corporation(self):
        response = self.client.post(
            "/generate",
            data={
                "client_name": "Acme",
                "client_type": "Corporation",
                "matter_type": "Flat",
                "payment_method": "retainer",
                "matter_description": "incorporation",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Instructing officer name is required", response.get_data(as_text=True))

    def test_requires_retainer_amount_for_hourly_strategy(self):
        response = self.client.post(
            "/generate",
            data={
                "client_name": "Pat",
                "client_type": "Individual",
                "matter_type": "Hourly Strategy",
                "payment_method": "pay on invoice",
                "matter_description": "corporate advisory",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Retainer amount is required", response.get_data(as_text=True))

    def test_valid_submission_generates_document(self):
        response = self.client.post(
            "/generate",
            data={
                "client_name": "Jordan",
                "client_type": "Corporation",
                "instructing_officer_name": "Taylor",
                "matter_type": "Hourly Strategy",
                "retainer_amount": "5000",
                "payment_method": "authorize credit card",
                "matter_description": "business acquisition",
            },
        )
        self.assertEqual(response.status_code, 200)
        response.close()
        output_files = list(app_module.OUTPUT_DIR.glob("document_*.docx"))
        self.assertEqual(len(output_files), 1)


if __name__ == "__main__":
    unittest.main()
