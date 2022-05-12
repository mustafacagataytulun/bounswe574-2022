from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from spaces.models import Space

from .forms import ArticleSaveForm
from .models import Article

def view(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    article = get_object_or_404(Article, pk=id)
    has_user_joined = request.user.is_authenticated & request.user.has_joined_to_space(space_id)
    has_user_upvoted = request.user in article.upvoters.all()
    has_user_downvoted = request.user in article.downvoters.all()

    return render(request, 'articles/view.html', {
        'space': space,
        'article': article,
        'user': request.user,
        'has_user_joined':has_user_joined,
        'has_user_upvoted': has_user_upvoted,
        'has_user_downvoted': has_user_downvoted, })

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

@login_required
def upvote(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    article = get_object_or_404(Article, pk=id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('articles:view', space_id=space.id, id=article.id)

    if request.user not in article.upvoters.all():
        if request.user in article.downvoters.all():
            article.downvoters.remove(request.user)
            Article.objects.filter(pk=id).update(score=F('score') + 2)
        else:
            Article.objects.filter(pk=id).update(score=F('score') + 1)

        article.upvoters.add(request.user)
    else:
        article.upvoters.remove(request.user)
        Article.objects.filter(pk=id).update(score=F('score') - 1)

    return redirect('articles:view', space_id=space.id, id=article.id)

@login_required
def downvote(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    article = get_object_or_404(Article, pk=id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('articles:view', space_id=space.id, id=article.id)

    if request.user not in article.downvoters.all():
        if request.user in article.upvoters.all():
            article.upvoters.remove(request.user)
            Article.objects.filter(pk=id).update(score=F('score') - 2)
        else:
            Article.objects.filter(pk=id).update(score=F('score') - 1)

        article.downvoters.add(request.user)
    else:
        article.downvoters.remove(request.user)
        Article.objects.filter(pk=id).update(score=F('score') + 1)

    return redirect('articles:view', space_id=space.id, id=article.id)
