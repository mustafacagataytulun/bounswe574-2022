from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ColearnAppUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ColearnAppUser
        fields = ('email', 'username', 'password1', 'password2', 'interests',)

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ColearnAppUser
        fields = ('email', 'username', 'interests',)
