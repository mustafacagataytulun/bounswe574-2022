from django import forms

from .models import Article, Comment

class ArticleSaveForm(forms.ModelForm):
    prerequisites = forms.CharField(label="Recommended Prerequisites", required=False)

    class Meta:
        model = Article
        fields = ('title', 'tags', 'prerequisites', 'content',)
        help_texts = {
            'content': 'You can use <a href="https://www.markdownguide.org/" target="_blank" />Markdown</a> to format the article.'
        }

class CommentSaveForm(forms.ModelForm):
    content = forms.CharField(label="Your Comment", required=True, widget=forms.Textarea(attrs={'placeholder': 'Please respect community rules.', 'rows': '5'}))

    class Meta:
        model = Comment
        fields = ('content',)
