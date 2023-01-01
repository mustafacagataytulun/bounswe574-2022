from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Q

from spaces.models import Space
from profiles.models import Notifications, Friends
from .forms import ArticleSaveForm, CommentSaveForm
from .models import Article, Comment


def view(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    article = get_object_or_404(Article, pk=id)
    comments = Comment.objects.filter(article__id = id)
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(space_id)
    form = CommentSaveForm()
    friendid=Friends.objects.filter(userid=request.user.id).values_list('friendid', flat=True)
    notificationCount=Notifications.objects.filter(Q(userid__in=friendid) & Q(isread=False)).count()


    return render(request, 'articles/view.html', {
        'space': space,
        'article': article,
        'user': request.user,
        'notificationCount': notificationCount,
        'has_user_joined':has_user_joined,
        'form': form,
        'comments': comments, })

@login_required
def save_comment(request, space_id, id):
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('articles:view', space_id=space_id, id=id)

    get_object_or_404(Space, pk=space_id)
    article = get_object_or_404(Article, pk=id)
    comment = Comment()

    form = CommentSaveForm(request.POST or None, instance=comment)

    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.created_by = request.user
        comment.article = article
        comment.save()

    return redirect('articles:view', space_id=space_id, id=id)

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
        notification = Notifications()
        notification.userid = request.user.id
        notification.timestamp=timezone.now
        notification.action = request.user.username + " created new article! "
        notification.link = "/spaces/" + str(space_id) + "/articles/" + str(article.id)
        notification.save(notification)

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
