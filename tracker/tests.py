from django.test import TestCase
from .models import Issue


class ReportWorkflow(TestCase):
    def test_report_appears_in_desk_and_can_be_resolved_twice(self):
        result = self.client.post("/api/issues", {"title": " Lamp broken ", "location": "Lab 3"}, content_type="application/json")
        self.assertEqual(result.status_code, 201)
        report = result.json()
        self.assertEqual(report["title"], "Lamp broken")
        self.assertFalse(report["resolved"])
        self.assertEqual(self.client.get("/api/issues").json(), [report])
        url = f"/api/issues/{report['id']}/resolve"
        for _ in range(2):
            self.assertEqual(self.client.post(url, {}, content_type="application/json").status_code, 200)
        self.assertTrue(self.client.get("/api/issues").json()[0]["resolved"])

    def test_invalid_reports_are_rejected(self):
        for body in ('{', '[]', '{}', '{"title":"Lamp","location":" "}', '{"location":"lab","title":"' + 'x'*121 + '"}'):
            with self.subTest(body=body):
                self.assertEqual(self.client.post("/api/issues", body, content_type="application/json").status_code, 400)
        self.assertFalse(Issue.objects.exists())

    def test_missing_report(self):
        self.assertEqual(self.client.post("/api/issues/77/resolve", {}, content_type="application/json").status_code, 404)
