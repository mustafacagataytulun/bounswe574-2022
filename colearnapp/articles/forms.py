from django import forms

from .models import Article

class ArticleCreateForm(forms.ModelForm):
    prerequisites = forms.CharField(label="Recommended Prerequisites", required=False)

    class Meta:
        model = Article
        fields = ('title', 'tags', 'prerequisites', 'content',)
        help_texts = {
            'content': 'You can use <a href="https://www.markdownguide.org/" target="_blank" />Markdown</a> to format the article.'
        }
