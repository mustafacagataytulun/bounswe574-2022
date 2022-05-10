from django.shortcuts import redirect, render

from .forms import SpaceCreateForm

def create(request):
    if request.method == "POST":
        form = SpaceCreateForm(request.POST)

        if form.is_valid():
            space = form.save()

            return redirect('create_success', id=space.id)

    else:
        form = SpaceCreateForm()

    return render(request, 'spaces/create_form.html', {'form': form})

def create_success(request, id):
    return render(request, 'spaces/create_done.html', {'id':id})

def view(request, id):
    return render(request, 'spaces/view.html', {'id':id})
