import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from storages.backends.s3boto3 import S3Boto3Storage

from users.models import ColearnAppUser

from .forms import ProfileEditForm
from .models import Profile

#pylint: disable=W0223
class ProfilePicturesStorage(S3Boto3Storage):
    bucket_name = 'colearnapp-profile-pictures'

@login_required
def edit(request):
    profile = Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(ColearnAppUser, pk=request.user.id)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user.profile)

        if form.is_valid():
            user.username = form.cleaned_data['display_name']
            user.save()

            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                profile_picture_extension = os.path.splitext(str(profile_picture))[1]
                storage = ProfilePicturesStorage()
                storage.save(str(user.id) + profile_picture_extension, profile_picture)

            return redirect('profiles:edit_success')

    else:
        #if profile:
        form = ProfileEditForm(initial={'display_name': user.username, 'bio': user.profile.bio, 'interests': user.profile.interests}, instance=user.profile)
        #else:
        #    form = ProfileEditForm({'display_name': user.username})

    return render(request, 'profiles/edit.html', {'form': form, 'user': user})

@login_required
def edit_success(request):
    return render(request, 'profiles/edit_success.html')
