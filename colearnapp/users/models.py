from django.contrib.auth.models import AbstractUser
from django.db import models

from spaces.models import Space

class ColearnAppUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    interests = models.CharField(max_length=500, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_joined_to_space(self, space_id):
        return Space.objects.filter(pk=space_id, subscribed_users__pk=self.id).count() > 0
    