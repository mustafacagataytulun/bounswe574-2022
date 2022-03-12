import requests

from django.views import generic
from typing import Any

from games.models import Game

class IndexView(generic.ListView):
    model = Game
    ordering = ['-completion_date']

class DetailView(generic.DetailView):
    model = Game

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        wikidata = get_wikidata(context['game'].wikidata_item_identifier)
        context['game_data'] = wikidata
        return context

def get_wikidata(item_identifier):
    wikidata_query = {
        "query": "SELECT ?propUrl ?valLabel ?gameDesc WHERE {wd:" + item_identifier + " ?propUrl ?valUrl . wd:" + item_identifier + " schema:description ?gameDesc . ?property ?ref ?propUrl . ?property rdf:type wikibase:Property . ?valUrl rdfs:label ?valLabel . FILTER (LANG(?gameDesc) = 'en') FILTER (LANG(?valLabel) = 'en') FILTER(?propUrl = wdt:P123 || ?propUrl = wdt:P178 || ?propUrl = wdt:P136)}"
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get('https://query.wikidata.org/sparql', params=wikidata_query, headers=headers)
    data = response.json()
    developer = next((x for x in data['results']['bindings'] if x['propUrl']['value'] == 'http://www.wikidata.org/prop/direct/P178'), None)
    publisher = next((x for x in data['results']['bindings'] if x['propUrl']['value'] == 'http://www.wikidata.org/prop/direct/P123'), None)
    genres = [x for x in data['results']['bindings'] if x['propUrl']['value'] == 'http://www.wikidata.org/prop/direct/P136']
    genreValues = []

    for genre in genres:
        genreValues.append(genre['valLabel']['value'])
    
    genre_text = ', '.join(genreValues)

    game_data = {
        'description': data['results']['bindings'][0]['gameDesc']['value'],
        'genre': genre_text,
        'developer': developer['valLabel']['value'],
        'publisher': publisher['valLabel']['value'],
    }

    return game_data
