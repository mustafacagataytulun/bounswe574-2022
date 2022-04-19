from django.conf.urls import include
from django.urls import path
from .views import dashboard, register

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
]
