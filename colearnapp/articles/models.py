from django.db import models
from django.utils import timezone

from colearnapp.base_models import TaggableEntity
from spaces.models import Space

class Article(TaggableEntity):
    title = models.CharField(max_length=200)
    prerequisites = models.CharField(max_length=2048, blank=True)
    content = models.TextField(max_length=65535)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', related_name='created_by_user', on_delete=models.SET_NULL, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey('users.ColearnAppUser', related_name='updated_by_user', on_delete=models.SET_NULL, null=True, blank=True)
    space = models.ForeignKey(Space, on_delete=models.RESTRICT)
    upvoters = models.ManyToManyField('users.ColearnAppUser', related_name='article_upvoter_users')
    downvoters = models.ManyToManyField('users.ColearnAppUser', related_name='article_downvoter_users')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(max_length=1024)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', related_name='article_comment_created_by_user', on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.RESTRICT)
