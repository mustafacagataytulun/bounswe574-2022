from django.conf.urls import include
from django.urls import path
from .views import register, register_success

app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('register/success', register_success, name='register_success'),
]
