from django.test import TestCase
from django.urls import reverse

from .models import ColearnAppUser

class RegisterViewTests(TestCase):
    def test_form(self):
        """
        User registration form should contain necessary inputs.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, '<label for="id_email">')
        self.assertContains(response, '<input type="email" name="email" maxlength="254" autofocus id="id_email">')
        self.assertContains(response, '<label for="id_username">')
        self.assertContains(response, '<input type="text" name="username" maxlength="150" autocapitalize="none" autocomplete="username" required id="id_username">')
        self.assertContains(response, '<label for="id_password1">')
        self.assertContains(response, '<input type="password" name="password1" autocomplete="new-password" required id="id_password1">')
        self.assertContains(response, '<label for="id_password2">')
        self.assertContains(response, '<input type="password" name="password2" autocomplete="new-password" required id="id_password2">')
        self.assertContains(response, '<label for="id_interests">')
        self.assertContains(response, '<input type="text" name="interests" maxlength="500" id="id_interests">')
        self.assertContains(response, '<input type="submit"')

    def test_form_submission(self):
        """
        User registration form should create user.
        """
        email = "example1@example.com"
        username = "example1"
        password1 = "y$T&P!NAPL$wu8hX"
        password2 = "y$T&P!NAPL$wu8hX"
        interests = "example interests"
        response = self.client.post(reverse('register'), data={'email':email, 'username':username, 'password1': password1, 'password2': password2, 'interests': interests}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your account has been created successfully.')

    def test_form_submission_with_invalid_form(self):
        """
        User registration form should return to form if it is not valid.
        """
        email = "example1@example.com"
        username = "example1"
        password1 = "test"
        password2 = "test"
        interests = "example interests"
        response = self.client.post(reverse('register'), data={'email':email, 'username':username, 'password1': password1, 'password2': password2, 'interests': interests})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post">')

class DashboardViewTests(TestCase):
    def test_view(self):
        """
        Dashboard should greet users with Hello message.
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')

class ColearnAppUserModelTests(TestCase):
    def test_create_user(self):
        """
        User should be created successfully.
        """
        email = "example@example.com"
        username = "example"
        password = "test"
        interests = "example interests"
        user = ColearnAppUser.objects.create_user(email=email, username=username, password=password, interests=interests)

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertEqual(user.interests, interests)
