from django import forms

from .models import Question, Answer

class QuestionSaveForm(forms.ModelForm):
    content = forms.CharField(label="Question", widget=forms.Textarea(attrs={'placeholder': 'Please respect community rules.'}),
        help_text='You can use <a href="https://www.markdownguide.org/" target="_blank" />Markdown</a> to format the question content.')

    class Meta:
        model = Question
        fields = ('title', 'tags', 'content',)

class AnswerSaveForm(forms.ModelForm):
    content = forms.CharField(label="Your Answer", required=True, widget=forms.Textarea(attrs={'placeholder': 'Please respect community rules.', 'rows': '5'}),
        help_text='You can use <a href="https://www.markdownguide.org/" target="_blank" />Markdown</a> to format the answer content.')

    class Meta:
        model = Answer
        fields = ('content',)
