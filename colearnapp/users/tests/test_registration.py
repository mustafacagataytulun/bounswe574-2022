from django.test import TestCase
from django.urls import reverse

class RegisterViewTests(TestCase):
    def test_form(self):
        """
        User registration form should contain necessary inputs.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, '<label class="form-label" for="id_email">')
        self.assertContains(response, '<input type="email" name="email" maxlength="254" autofocus class="form-control" placeholder="Email" id="id_email">')
        self.assertContains(response, '<label class="form-label" for="id_username">')
        self.assertContains(response, '<input type="text" name="username" maxlength="150" autocapitalize="none" autocomplete="username" class="form-control" placeholder="Username" required id="id_username">')
        self.assertContains(response, '<label class="form-label" for="id_password1">')
        self.assertContains(response, '<input type="password" name="password1" autocomplete="new-password" class="form-control" placeholder="Password" required id="id_password1">')
        self.assertContains(response, '<label class="form-label" for="id_password2">')
        self.assertContains(response, '<input type="password" name="password2" autocomplete="new-password" class="form-control" placeholder="Password confirmation" required id="id_password2">')
        self.assertContains(response, '<label class="form-label" for="id_interests">')
        self.assertContains(response, '<input type="text" name="interests" maxlength="500" class="form-control" placeholder="Interests" id="id_interests">')
        self.assertContains(response, '<button class="btn btn-primary" type="submit">Register</button>')

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
