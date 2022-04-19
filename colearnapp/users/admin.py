from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import ColearnAppUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = ColearnAppUser
    list_display = ["email", "username", "interests"]

admin.site.register(ColearnAppUser, CustomUserAdmin)
