from django.conf.urls import include
from django.urls import path
from .views import dashboard, register, register_success

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('register/success', register_success, name='register_success'),
]
