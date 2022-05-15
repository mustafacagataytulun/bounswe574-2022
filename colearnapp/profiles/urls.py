from django.urls import path

from .views import edit, edit_success, view

app_name = 'profiles'

urlpatterns = [
    path('<int:id>', view, name='view'),
    path('edit', edit, name='edit'),
    path('saved', edit_success, name='edit_success'),
]
