from django.db import models
from django.utils import timezone

from users.models import ColearnAppUser

class Profile(models.Model):
    bio = models.TextField(max_length=2000, blank=True)
    interests = models.CharField(max_length=500, blank=True)
    user = models.OneToOneField(ColearnAppUser, on_delete=models.RESTRICT, related_name='profile')

    def __str__(self):
        return 'Profile of ' + self.user.username

class Friends(models.Model):
    userid=models.PositiveIntegerField()
    friendid=models.PositiveIntegerField()
    friendname=models.TextField()

    def __str__(self):
        return self.friendname

class Notifications(models.Model):
    userid=models.PositiveIntegerField()
    action=models.TextField()
    link=models.TextField(default="null")
    isread=models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    