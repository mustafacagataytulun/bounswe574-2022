from django import forms

class SpaceSearchForm(forms.Form):
    search = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'placeholder': 'Find your Colearning Space'}))
