from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return HttpResponseRedirect(reverse('register_success'))

    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register_form.html', {'form': form})

def register_success(request):
    return render(request, 'users/register_done.html')
