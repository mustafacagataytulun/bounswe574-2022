from django.db import models

class TaggableEntity(models.Model):
    tags = models.CharField(max_length=500, blank=True)

    class Meta:
        abstract=True

    def get_tag_list(self):
        return self.tags.split(',')
