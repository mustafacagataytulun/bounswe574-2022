from django import forms

from .models import MainPage, Space

class SpaceCreateForm(forms.ModelForm):
    cover_image = forms.FileField(label="Cover Image", required=True)

    class Meta:
        model = Space
        fields = ('name', 'tags',)
        help_texts = {
            'tags': 'Separate tags with commas.',
        }

class MainPageSaveForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ('content',)
