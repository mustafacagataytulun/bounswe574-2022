from django.urls import path

from .views import downvote, save, save_success, upvote, view

app_name = 'quizzes'

#pylint: disable=R0801
urlpatterns = [
    path('<int:id>', view, name='view'),
    path('create', save, name='create'),
    path('edit/<int:id>', save, name='edit'),
    path('<int:id>/saved', save_success, name='save_success'),
    path('<int:id>/upvote', upvote, name='upvote'),
    path('<int:id>/downvote', downvote, name='downvote'),
]
