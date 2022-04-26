from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from ..models import ColearnAppUser

class LoginViewTests(TestCase):
    def test_form(self):
        """
        Login form should contain necessary inputs.
        """
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, '<label class="form-label" for="id_username">')
        self.assertContains(response, '<input type="text" name="username" autofocus autocapitalize="none" autocomplete="username" maxlength="254" class="form-control" placeholder="Email" required id="id_username">')
        self.assertContains(response, '<label class="form-label" for="id_password">')
        self.assertContains(response, '<input type="password" name="password" autocomplete="current-password" class="form-control" placeholder="Password" required id="id_password">')
        self.assertContains(response, '<button class="btn btn-primary" type="submit">Sign in</button>')

    def test_form_submission(self):
        """
        Login form should log the user in and redirect to root URL.
        """
        email = "logintest@example.com"
        username = "logintest"
        password = "y$T&P!NAPL$wu8hX"
        interests = "example interests"
        ColearnAppUser.objects.create_user(email=email, username=username, password=password, interests=interests)

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        response = self.client.post(reverse('login'), data={'username':email, 'password': password})
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/')
        self.assertTrue(user.is_authenticated)

    def test_form_submission_with_invalid_credentials(self):
        """
        Login form should display error for invalid credentials.
        """
        email = "logintestinvalid@example.com"
        username = "logintestinvalid"
        password = "y$T&P!NAPL$wu8hX"
        invalid_password = "zk^YVWuLxd8&5*&D"
        interests = "example interests"
        ColearnAppUser.objects.create_user(email=email, username=username, password=password, interests=interests)

        response = self.client.post(reverse('login'), data={'username':email, 'password': invalid_password})
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct email and password. Note that both fields may be case-sensitive.')
        self.assertFalse(user.is_authenticated)
