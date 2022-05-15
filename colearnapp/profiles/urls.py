from django.urls import path

from .views import edit, edit_success

app_name = 'profiles'

urlpatterns = [
    path('edit', edit, name='edit'),
    path('saved', edit_success, name='edit_success'),
]
