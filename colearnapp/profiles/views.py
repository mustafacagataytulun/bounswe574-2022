import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from storages.backends.s3boto3 import S3Boto3Storage

from spaces.models import Space
from users.models import ColearnAppUser

from profiles.models import Notifications, Friends, Profile
from .forms import ProfileEditForm

#pylint: disable=W0223
class ProfilePicturesStorage(S3Boto3Storage):
    bucket_name = 'colearnapp-profile-pictures'

@login_required
def view(request, id):
    user = get_object_or_404(ColearnAppUser, pk=id)
    user_spaces = Space.objects.filter(subscribed_users=user).order_by('name')
    friends=Friends.objects.filter(userid=id)
    friendCount=Friends.objects.filter(userid=request.user.id).values_list('friendid', flat=True).count()
    friendid=Friends.objects.filter(userid=request.user.id).values_list('friendid', flat=True)
    notificationCount=Notifications.objects.filter(Q(userid__in=friendid) & Q(isread=False)).count()



    return render(request, 'profiles/view.html', {
        'user': user,
        'user_spaces': user_spaces,
        'friends': friends,
        'notificationCount': notificationCount,
        'friendCount': friendCount,
    })

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

@login_required
def add_friend(request,id):
    # print(id)
    # friend=ColearnAppUser.objects.get(id=id)
    # print(friend)
    _friendname=ColearnAppUser.objects.get(id=id).username
    new_friend = Friends(userid=request.user.id, friendid=id, friendname=_friendname)
    new_friend.save()
    new_friend2=Friends(userid=id, friendid=request.user.id, friendname=request.user.username)
    new_friend2.save()
    messages.success(request,'Friend added!')
    return render(request, 'profiles/view.html')

@login_required
def remove_friend(request,id):
    # print(id)
    # friend=ColearnAppUser.objects.get(id=id)
    # print(friend)
    _friendname=ColearnAppUser.objects.get(id=id).username
    Friends.objects.filter(friendid=id).filter(userid=request.user.id).delete()
    Friends.objects.filter(userid=id).filter(friendid=request.user.id).delete()
    messages.success(request,'Friend removed!')
    return render(request, 'profiles/view.html')

@login_required
def notifications(request):
    friendid=Friends.objects.filter(userid=request.user.id).values_list('friendid', flat=True)
    notifications_existing=Notifications.objects.filter(Q(userid__in=friendid) & Q(isread=False))
    return render(request, 'profiles/notifications.html', {
        'notifications': notifications_existing,
    })

@login_required
def notif_read(request,id):

    Notifications.objects.filter(id=id).update(isread = True)

    messages.success(request,'Notification is read!')
    return render(request, 'profiles/view.html')
    