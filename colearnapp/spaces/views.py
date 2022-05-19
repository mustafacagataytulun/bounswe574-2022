import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from storages.backends.s3boto3 import S3Boto3Storage

from articles.models import Article
from glossary.models import GlossaryItem
from questions.models import Question
from quizzes.models import Quiz

from .forms import SpaceCreateForm
from .models import MainPage, Space

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

            space.subscribed_users.add(request.user)
            space.save()

            main_page = MainPage(content='### Welcome to ' + space.name + ' colearning space!\n\n' +
                'This is the welcoming page of this space.\n\nYou can edit it however you like to describe this colearning space, ' +
                'or give your new colearners a direction for where to start. You can use **Markdown** for styling. *Yay!*')
            main_page.space = space
            main_page.save()

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

def main(request, id):
    space = Space.objects.get(pk=id)
    main_page = MainPage.objects.get(space_id=space.id)
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(id)
    joined_users = space.subscribed_users.all()

    return render(request, 'spaces/main.html', {
        'space':space,
        'main_page':main_page,
        'has_user_joined':has_user_joined,
        'joined_users':joined_users,})

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

def questions(request, id):
    space = Space.objects.get(pk=id)
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(id)
    joined_users = space.subscribed_users.all()
    question_list = Question.objects.filter(space_id=id)

    return render(request, 'spaces/questions.html', {
        'space':space,
        'has_user_joined':has_user_joined,
        'joined_users':joined_users,
        'questions':question_list,})

def quizzes(request, id):
    space = get_object_or_404(Space, pk=id)
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(id)
    joined_users = space.subscribed_users.all()
    quiz_list = Quiz.objects.filter(space_id=id)

    return render(request, 'spaces/quizzes.html', {
        'space':space,
        'has_user_joined':has_user_joined,
        'joined_users':joined_users,
        'quizzes':quiz_list,})

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
