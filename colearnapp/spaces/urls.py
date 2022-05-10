from django.urls import path
from .views import create, create_success, view

app_name = 'spaces'

urlpatterns = [
    path('create/', create, name='create'),
    path('create/success/<int:id>', create_success, name='create_success'),
    path('view/<int:id>', view, name='view'),
]
