from django.db import models

from users.models import ColearnAppUser

class Profile(models.Model):
    bio = models.TextField(max_length=2000, blank=True)
    interests = models.CharField(max_length=500, blank=True)
    user = models.OneToOneField(ColearnAppUser, on_delete=models.RESTRICT, related_name='profile')

    def __str__(self):
        return 'Profile of ' + self.user.username
