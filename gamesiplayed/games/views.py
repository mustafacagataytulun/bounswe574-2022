from django.views import generic

from games.models import Game

class IndexView(generic.ListView):
    model = Game

class DetailView(generic.DetailView):
    model = Game
    extra_context = {
        'game_data': {
            'description': 'This is a test description.',
            'genre': 'Test genre, another test genre',
            'developer': 'Lorem Ipsum Developer',
            'publisher': 'Dolor Sit Amet Publisher'
        }
    }
