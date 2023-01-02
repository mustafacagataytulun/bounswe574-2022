from django.db import models
from django.utils import timezone

from colearnapp.base_models import TaggableEntity

class Space(TaggableEntity):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', on_delete=models.SET_NULL, null=True)
    subscribed_users = models.ManyToManyField('users.ColearnAppUser', related_name='space_subscribed_users')
    main_page = models.OneToOneField('MainPage', on_delete=models.RESTRICT, related_name='space_main_page', null=True)
    related_spaces = models.ManyToManyField('Space', related_name='space_related_spaces', null=True)
    semantic_tags = models.CharField(max_length=65535, null=True)

    def __str__(self):
        return self.name

class MainPage(models.Model):
    content = models.TextField(max_length=65535)
    space = models.OneToOneField('Space', on_delete=models.RESTRICT, related_name='space_main_page')


class SemanticTag(models.Model):
    label = models.TextField(max_length=65535)
    descripion = models.TextField(max_length=65535)
