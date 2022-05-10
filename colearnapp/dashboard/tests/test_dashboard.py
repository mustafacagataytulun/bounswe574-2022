from django.test import TestCase
from django.urls import reverse

from users.models import ColearnAppUser

class DashboardViewTests(TestCase):
    def test_view_anonymous_user(self):
        """
        Dashboard should greet anonymous users.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to ColearnApp!')

    def test_view_authenticated_user(self):
        """
        Dashboard should show spaces of authenticated users.
        """
        email = "dashboardtest@example.com"
        username = "dashboardtest"
        password = "y$T&P!NAPL$wu8hX"
        interests = "example interests"
        ColearnAppUser.objects.create_user(email=email, username=username, password=password, interests=interests)
        self.client.post(reverse('login'), data={'username':email, 'password': password})
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Spaces')
