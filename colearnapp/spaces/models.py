from django.db import models
from django.utils import timezone

from colearnapp.base_models import TaggableEntity

class Space(TaggableEntity):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', on_delete=models.SET_NULL, null=True)
    subscribed_users = models.ManyToManyField('users.ColearnAppUser', related_name='space_subscribed_users')

    def __str__(self):
        return self.name
