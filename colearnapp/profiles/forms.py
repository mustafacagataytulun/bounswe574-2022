from django import forms

from .models import Profile

class ProfileEditForm(forms.ModelForm):
    display_name = forms.CharField(label="Display Name", required=True)
    profile_picture = forms.FileField(label="Profile Picture", required=False)

    class Meta:
        model = Profile
        fields = ('display_name', 'bio', 'interests', 'profile_picture',)
        help_texts = {
            'bio': 'You can use <a href="https://www.markdownguide.org/" target="_blank" />Markdown</a> to format your bio.'
        }
