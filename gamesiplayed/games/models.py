from django.db import models

class Game(models.Model):
    game_title = models.CharField('Title', max_length=250)
    wikidata_item_identifier = models.CharField('Wikidata Item Identifier', max_length=50)
    cover_image_uri = models.CharField('Cover Image URI', max_length=1024, null=True)

    def __str__(self):
        return self.game_title
