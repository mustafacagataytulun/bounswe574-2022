from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ColearnAppUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ColearnAppUser
        User = get_user_model()
        fields = ('email', 'username', 'password1', 'password2', 'interests',)

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ColearnAppUser
        User = get_user_model()
        fields = ('email', 'username', 'interests',)
