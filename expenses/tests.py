from django.test import TestCase


class ExpensesSmokeTest(TestCase):
    def test_index_renders(self):
        response = self.client.get('/expenses/')
        self.assertIn(response.status_code, (200, 302))
