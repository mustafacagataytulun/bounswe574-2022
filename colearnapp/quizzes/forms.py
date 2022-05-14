from django import forms

from .models import Quiz

class QuizSaveForm(forms.ModelForm):
    answers = forms.CharField(label="Answers", required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Enter each answer in a new line. Put an "*" sign at the beginning of the correct answer.', 'rows': '10'}),
        help_text='Enter each answer in a new line. Put an "*" sign at the beginning of the correct answer.')

    class Meta:
        model = Quiz
        fields = ('question', 'tags', 'answers',)
