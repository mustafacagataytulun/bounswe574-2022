import os
import logging
import requests

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from storages.backends.s3boto3 import S3Boto3Storage

from articles.models import Article
from glossary.models import GlossaryItem
from questions.models import Question
from quizzes.models import Quiz

from .forms import MainPageSaveForm, SpaceCreateForm
from .models import MainPage, Space

#pylint: disable=W0223
class SpaceCoversStorage(S3Boto3Storage):
    bucket_name = 'colearnapp-space-covers'


def wikidata_results(term):
    wikidata_query = {
        "action": "wbsearchentities",
        "search": term,
        "language": "en",
        "format": "json",
        "limit": 50,
        "continue": 0,
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get('https://www.wikidata.org/w/api.php', params=wikidata_query, headers=headers)
    data = response.json()
    print(data)
    search_data = data['search']
    result_list = []
    for item in search_data:
        label = item['display']['label']['value']
        id = item['id']
        print(label)
        print(id)
        description = ""
        if item['display'].get('description'):
            description = item['display']['description']['value']
        #description = item['display']['description']['value']
        print(description)
        result_list.append(label + ", " + description)

        #result_list.append(label + ", " + id)
    # return HttpResponse(json.dumps(result_list))
    return JsonResponse(result_list, safe=False)


def tag_autocomplete(request):
    if 'query' in request.GET:
        term = request.GET['query']
    else:
        term = "all"
    tags = wikidata_results(term)
    # return HttpResponse(json.dumps(tags))
    return render(request, 'spaces/wikidata_results.html', {'tags': tags})

def wikidata_q(request):
    if 'query' in request.GET:
        term = request.GET['query']
    else:
        term = "all"
    tags = wikidata_results(term)
    #return HttpResponse(json.dumps(tags))
    return tags


@login_required
def create(request):
    if request.method == "POST":
        form = SpaceCreateForm(request.POST, request.FILES)

        if form.is_valid():
            space = form.save(commit=False)
            space.created_by = request.user
            space.save()

            space.subscribed_users.add(request.user)
            space.semantic_tags = request.POST.get('semanticTags')
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
            print("semantic_tags:", space.semantic_tags)
            print("request.POST:", request.POST)
            print("request:", request)
            print("request.POST.get('query'):", request.POST.get('query'))
            print("request.POST.get('semanticTags'):", request.POST.get('semanticTags'))

            return redirect('spaces:create_success', id=space.id)

    else:
        if 'query' in request.GET:
            term = request.GET['query']
        else:
            term = "all"
        tags = wikidata_results(term)
        form = SpaceCreateForm()

    return render(request, 'spaces/create_form.html', {'tags': tags,
                                                       'form': form})

@login_required
def create_success(request, id):
    return render(request, 'spaces/create_done.html', {'id':id})

def main(request, id):
    space = Space.objects.get(pk=id)
    main_page = MainPage.objects.get(space_id=space.id)
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(id)
    joined_users = space.subscribed_users.all()
    if joined_users:
        related_spaces = Space.objects.filter(subscribed_users__pk=request.user.id)
    else:
        related_spaces = Space.objects.all()

    logging.warning(related_spaces)

    return render(request, 'spaces/main.html', {
        'space':space,
        'main_page':main_page,
        'has_user_joined':has_user_joined,
        'joined_users':joined_users,
        'related_spaces':related_spaces})

def save_main_page(request, id):
    has_user_joined = request.user.has_joined_to_space(id)

    if not has_user_joined:
        return redirect('spaces:main', space_id=id)

    space = get_object_or_404(Space, pk=id)

    if hasattr(space, 'main_page'):
        main_page = get_object_or_404(MainPage, space_id=space.id)
    else:
        main_page = MainPage()

    form = MainPageSaveForm(request.POST or None, instance=main_page)

    if request.method == "POST" and form.is_valid():
        main_page = form.save(commit=False)
        main_page.space = space
        main_page.save()

        return redirect('spaces:main', id=id)

    return render(request, 'spaces/main_page_save_form.html', {'form': form, 'space': space})

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
