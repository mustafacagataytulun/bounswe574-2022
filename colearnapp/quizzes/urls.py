from django.urls import path

from .views import save, save_success

app_name = 'quizzes'

urlpatterns = [
    path('create', save, name='create'),
    path('edit/<int:id>', save, name='edit'),
    path('<int:id>/saved', save_success, name='save_success'),
]
