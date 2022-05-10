import os

from django.shortcuts import redirect, render
from storages.backends.s3boto3 import S3Boto3Storage

from .forms import SpaceCreateForm
from .models import Space

#pylint: disable=W0223
class SpaceCoversStorage(S3Boto3Storage):
    bucket_name = 'colearnapp-space-covers'

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

            return redirect('create_success', id=space.id)

    else:
        form = SpaceCreateForm()

    return render(request, 'spaces/create_form.html', {'form': form})

def create_success(request, id):
    return render(request, 'spaces/create_done.html', {'id':id})

def articles(request, id):
    space = Space.objects.get(pk=id)

    return render(request, 'spaces/articles.html', {'space':space})
