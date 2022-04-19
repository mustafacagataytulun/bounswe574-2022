from django.contrib.auth.models import AbstractUser
from django.db import models

class ColearnAppUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    interests = models.CharField(max_length=500, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
