from django.db import models
from django.utils import timezone

from spaces.models import Space

class GlossaryItem(models.Model):
    term = models.CharField(max_length=200)
    definition = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.ColearnAppUser', related_name='glossary_item_created_by_user', on_delete=models.SET_NULL, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey('users.ColearnAppUser', related_name='glossary_item_updated_by_user', on_delete=models.SET_NULL, null=True, blank=True)
    space = models.ForeignKey(Space, on_delete=models.RESTRICT)

    def __str__(self):
        return self.term
