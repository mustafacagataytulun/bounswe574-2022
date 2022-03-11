from django.views import generic

from games.models import Game

class IndexView(generic.ListView):
    model = Game
