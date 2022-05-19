from django.urls import path

from .views import downvote, downvote_answer, save, save_answer, save_success, upvote, upvote_answer, view

app_name = 'questions'

#pylint: disable=R0801
urlpatterns = [
    path('<int:id>', view, name='view'),
    path('create', save, name='create'),
    path('edit/<int:id>', save, name='edit'),
    path('<int:id>/saved', save_success, name='save_success'),
    path('<int:id>/upvote', upvote, name='upvote'),
    path('<int:id>/downvote', downvote, name='downvote'),
    path('<int:id>/save_answer', save_answer, name='save_answer'),
    path('<int:question_id>/answer/<int:id>/upvote', upvote_answer, name='upvote_answer'),
    path('<int:question_id>/answer/<int:id>/downvote', downvote_answer, name='downvote_answer'),
]
