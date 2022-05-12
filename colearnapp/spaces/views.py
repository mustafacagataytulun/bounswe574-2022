import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from storages.backends.s3boto3 import S3Boto3Storage

from articles.models import Article
from glossary.models import GlossaryItem

from .forms import SpaceCreateForm
from .models import Space

#pylint: disable=W0223
class SpaceCoversStorage(S3Boto3Storage):
    bucket_name = 'colearnapp-space-covers'

@login_required
def create(request):
    if request.method == "POST":
        form = SpaceCreateForm(request.POST, request.FILES)

        if form.is_valid():
            space = form.save(commit=False)
            space.created_by = request.user
            space.save()

            cover_image = request.FILES['cover_image']
            cover_image_extension = os.path.splitext(str(cover_image))[1]
            storage = SpaceCoversStorage()
            storage.save(str(space.id) + cover_image_extension, cover_image)

            return redirect('spaces:create_success', id=space.id)

    else:
        form = SpaceCreateForm()

    return render(request, 'spaces/create_form.html', {'form': form})

@login_required
def create_success(request, id):
    return render(request, 'spaces/create_done.html', {'id':id})

def articles(request, id):
    space = Space.objects.get(pk=id)
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(id)
    joined_users = space.subscribed_users.all()
    article_list = Article.objects.filter(space_id=id)

    return render(request, 'spaces/articles.html', {
        'space':space,
        'has_user_joined':has_user_joined,
        'joined_users':joined_users,
        'articles':article_list,})

def glossary(request, id):
    space = Space.objects.get(pk=id)
    has_user_joined = request.user.has_joined_to_space(id)
    joined_users = space.subscribed_users.all()
    glossary_items = GlossaryItem.objects.filter(space_id=id).order_by('term')

    return render(request, 'spaces/glossary.html', {
        'space':space,
        'has_user_joined':has_user_joined,
        'joined_users':joined_users,
        'glossary_items':glossary_items,})

@login_required
def join(request, id):
    space = get_object_or_404(Space, pk=id)
    has_user_joined = request.user.has_joined_to_space(id)

    if not has_user_joined:
        space.subscribed_users.add(request.user)

    return redirect('spaces:view', id=space.id)

@login_required
def leave(request, id):
    space = get_object_or_404(Space, pk=id)
    has_user_joined = request.user.has_joined_to_space(id)

    if has_user_joined:
        space.subscribed_users.remove(request.user)

    return redirect('spaces:view', id=space.id)
