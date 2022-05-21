from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from spaces.models import Space

from .forms import SpaceSearchForm

def index(request):
    own_spaces = None

    if request.user.is_authenticated:
        own_spaces = Space.objects.filter(created_by=request.user).order_by('-id')

    form = SpaceSearchForm(request.GET or None)
    is_searched = form.is_valid() and len(form.cleaned_data['search'])

    if is_searched:
        all_spaces = Space.objects.all().filter(Q(name__icontains=form.cleaned_data['search']) | Q(tags__icontains=form.cleaned_data['search'])).order_by('-id')
    else:
        all_spaces = Space.objects.all().order_by('-id')

    paginator = Paginator(all_spaces, per_page=24)
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, "dashboard/index.html", {
        'all_spaces':all_spaces,
        'own_spaces':own_spaces,
        'form':form,
        'is_searched':is_searched,
        'page':page,
        })
