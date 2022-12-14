from django.urls import path
from django.views.generic.base import RedirectView

from .views import articles, create, create_success, glossary, join, leave, main, questions, quizzes, save_main_page, tag_autocomplete, wikidata_q

app_name = 'spaces'

urlpatterns = [
    path('wikidata_results/', tag_autocomplete, name='tag_autocomplete'),
    path('wikidata_q/', wikidata_q, name='wikidata_q'),
    path('create/', create, name='create'),
    path('create/success/<int:id>', create_success, name='create_success'),
    path('<int:id>', RedirectView.as_view(pattern_name='spaces:main', permanent=False), name='view'),
    path('<int:id>/join', join, name='join'),
    path('<int:id>/leave', leave, name='leave'),
    path('<int:id>/main', main, name='main'),
    path('<int:id>/save_main_page', save_main_page, name='save_main_page'),
    path('<int:id>/articles', articles, name='articles'),
    path('<int:id>/questions', questions, name='questions'),
    path('<int:id>/quizzes', quizzes, name='quizzes'),
    path('<int:id>/glossary', glossary, name='glossary'),
]
