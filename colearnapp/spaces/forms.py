from django import forms

from .models import Space

class SpaceCreateForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ('name', 'tags',)
