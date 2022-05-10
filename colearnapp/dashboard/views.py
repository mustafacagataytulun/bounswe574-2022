from django.shortcuts import render

from spaces.models import Space

def index(request):
    own_spaces = None

    if request.user.is_authenticated:
        own_spaces = Space.objects.filter(created_by=request.user).order_by('-id')[:10]

    all_spaces = Space.objects.order_by('-id')[:10]

    return render(request, "dashboard/index.html", {
        'all_spaces':all_spaces,
        'own_spaces':own_spaces
        })
