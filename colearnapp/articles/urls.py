from django.urls import path

from .views import create, create_success, edit, view

app_name = 'articles'

urlpatterns = [
    path('<int:id>', view, name='view'),
    path('create', create, name='create'),
    path('create/success/<int:id>', create_success, name='create_success'),
    path('edit/<int:id>', edit, name='edit'),
]
