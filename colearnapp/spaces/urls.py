from django.urls import path
from django.views.generic.base import RedirectView

from .views import articles, create, create_success

app_name = 'spaces'

urlpatterns = [
    path('create/', create, name='create'),
    path('create/success/<int:id>', create_success, name='create_success'),
    path('<int:id>', RedirectView.as_view(pattern_name='spaces:articles', permanent=False), name='view'),
    path('<int:id>/articles', articles, name='articles'),
]
