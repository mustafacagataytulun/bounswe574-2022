from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from spaces.models import Space

from .forms import GlossaryItemSaveForm
from .models import GlossaryItem

@login_required
def save(request, space_id, id=None):
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('spaces:glossary', space_id=space_id)

    space = get_object_or_404(Space, pk=space_id)

    if id:
        glossary_item = get_object_or_404(GlossaryItem, pk=id)
    else:
        glossary_item = GlossaryItem()

    form = GlossaryItemSaveForm(request.POST or None, instance=glossary_item)

    if request.method == "POST" and form.is_valid():
        glossary_item = form.save(commit=False)

        if id:
            glossary_item.updated_by = request.user
            glossary_item.updated_date = datetime.now(timezone.utc).isoformat()
        else:
            glossary_item.created_by = request.user

        glossary_item.space = space
        glossary_item.save()

        return redirect('glossary:save_success', space_id=space_id, id=glossary_item.id)

    return render(request, 'glossary/save_form.html', {'form': form, 'space': space})

@login_required
def save_success(request, space_id, id):
    return render(request, 'glossary/save_success.html', {'space_id': space_id, 'id': id})
