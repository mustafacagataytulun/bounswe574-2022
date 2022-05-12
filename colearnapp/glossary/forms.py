from django import forms

from .models import GlossaryItem

class GlossaryItemSaveForm(forms.ModelForm):
    class Meta:
        model = GlossaryItem
        fields = ('term', 'definition',)
