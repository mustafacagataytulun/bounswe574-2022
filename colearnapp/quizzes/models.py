from django.db import models
from django.utils import timezone

from spaces.models import Space

class Quiz(models.Model):
    question = models.CharField(max_length=500)
    tags = models.CharField(max_length=500, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', related_name='quiz_created_by_user', on_delete=models.SET_NULL, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey('users.ColearnAppUser', related_name='quiz_updated_by_user', on_delete=models.SET_NULL, null=True, blank=True)
    space = models.ForeignKey(Space, on_delete=models.RESTRICT)
    upvoters = models.ManyToManyField('users.ColearnAppUser', related_name='quiz_upvoter_users')
    downvoters = models.ManyToManyField('users.ColearnAppUser', related_name='quiz_downvoter_users')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Answer(models.Model):
    content = models.TextField(max_length=500)
    is_correct = models.BooleanField(null=False, default=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', related_name='quiz_answer_created_by_user', on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Quiz, on_delete=models.RESTRICT)
