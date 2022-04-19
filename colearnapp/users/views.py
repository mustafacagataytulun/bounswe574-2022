from django.contrib.auth import login
from django.shortcuts import render

from .forms import CustomUserCreationForm

def dashboard(request):
    return render(request, "users/dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register_form.html",
            {"form": CustomUserCreationForm}
        )

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return render(
                request, "users/register_done.html"
            )

    return None
