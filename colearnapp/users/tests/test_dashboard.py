from django.test import TestCase
from django.urls import reverse

class DashboardViewTests(TestCase):
    def test_view(self):
        """
        Dashboard should greet users with Hello message.
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')
