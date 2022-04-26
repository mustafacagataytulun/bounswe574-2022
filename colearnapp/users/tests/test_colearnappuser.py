from django.test import TestCase

from ..models import ColearnAppUser

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
        self.assertRegex(user.password, '^pbkdf2_sha256\$320000\$')
