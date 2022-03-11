from django.db import models

class Game(models.Model):
    game_title = models.CharField(max_length=250)
    wikidata_item_identifier = models.CharField(max_length=50)

    def __str__(self):
        return self.game_title
