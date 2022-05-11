from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from spaces.models import Space

from .forms import ArticleCreateForm
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
def create(request, space_id):
    space = Space.objects.get(pk=space_id)

    if request.method == "POST":
        form = ArticleCreateForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.space = space
            article.save()

            return redirect('articles:create_success', space_id=space_id, id=article.id)

    else:
        form = ArticleCreateForm()

    return render(request, 'articles/create_form.html', {'form': form, 'space': space})

@login_required
def create_success(request, space_id, id):
    return render(request, 'articles/create_done.html', {'space_id': space_id, 'id': id})

@login_required
def edit(request, space_id, id):
    has_user_joined = request.user.is_authenticated & request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('articles:view', space_id=space_id, id=id)

    return render(request, 'articles/edit_form.html', {'space_id': space_id, 'id': id})
