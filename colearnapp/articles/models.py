from django.db import models
from django.utils import timezone

from spaces.models import Space

class Article(models.Model):
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=500, blank=True)
    prerequisites = models.CharField(max_length=2048, blank=True)
    content = models.TextField(max_length=65535)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', related_name='created_by_user', on_delete=models.SET_NULL, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey('users.ColearnAppUser', related_name='updated_by_user', on_delete=models.SET_NULL, null=True, blank=True)
    space = models.ForeignKey(Space, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title
