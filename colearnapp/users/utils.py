import random
import string

from django.test import TestCase

from users.models import ColearnAppUser

def create_random_string(char_count):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_count))

def create_test_user():
    email = create_random_string(10) + "@example.com"
    username = create_random_string(10)
    password = create_random_string(20)
    interests = create_random_string(10)
    return (ColearnAppUser.objects.create_user(email=email, username=username, password=password, interests=interests), password,)

def create_and_login_test_user(test_case: TestCase):
    (user, real_password,) = create_test_user()
    test_case.client.login(username=user.email, password=real_password)
