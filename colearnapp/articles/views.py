from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from spaces.models import Space

from .forms import ArticleSaveForm
from .models import Article

def view(request, space_id, id):
    space = Space.objects.get(pk=space_id)

    if not space:
        return HttpResponseNotFound()

    article = Article.objects.get(pk=id)

    if not article:
        return HttpResponseNotFound()

    has_user_joined = request.user.is_authenticated & request.user.has_joined_to_space(space_id)

    return render(request, 'articles/view.html', {
        'space': space,
        'article': article,
        'user': request.user,
        'has_user_joined':has_user_joined })

@login_required
def save(request, space_id, id=None):
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('articles:view', space_id=space_id, id=id)

    space = get_object_or_404(Space, pk=space_id)

    if id:
        article = get_object_or_404(Article, pk=id)
    else:
        article = Article()

    form = ArticleSaveForm(request.POST or None, instance=article)

    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)

        if id:
            article.updated_by = request.user
            article.updated_date = datetime.now(timezone.utc).isoformat()
        else:
            article.created_by = request.user

        article.space = space
        article.save()

        return redirect('articles:save_success', space_id=space_id, id=article.id)

    return render(request, 'articles/save_form.html', {'form': form, 'space': space})

@login_required
def save_success(request, space_id, id):
    return render(request, 'articles/save_success.html', {'space_id': space_id, 'id': id})
