from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from spaces.models import Space

from .forms import QuestionSaveForm, AnswerSaveForm
from .models import Question, Answer

def view(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    question = get_object_or_404(Question, pk=id)
    answers = Answer.objects.filter(question__id = id).order_by('-score', 'created_date')
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(space_id)
    form = AnswerSaveForm()

    return render(request, 'questions/view.html', {
        'space': space,
        'question': question,
        'user': request.user,
        'has_user_joined':has_user_joined,
        'form': form,
        'answers': answers, })

@login_required
def save_answer(request, space_id, id):
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('questions:view', space_id=space_id, id=id)

    get_object_or_404(Space, pk=space_id)
    question = get_object_or_404(Question, pk=id)
    answer = Answer()

    form = AnswerSaveForm(request.POST or None, instance=answer)

    if request.method == "POST" and form.is_valid():
        answer = form.save(commit=False)
        answer.created_by = request.user
        answer.question = question
        answer.save()

    return redirect('questions:view', space_id=space_id, id=id)

@login_required
def save(request, space_id, id=None):
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('questions:view', space_id=space_id, id=id)

    space = get_object_or_404(Space, pk=space_id)

    if id:
        question = get_object_or_404(Question, pk=id)
    else:
        question = Question()

    form = QuestionSaveForm(request.POST or None, instance=question)

    if request.method == "POST" and form.is_valid():
        question = form.save(commit=False)

        if id:
            question.updated_by = request.user
            question.updated_date = datetime.now(timezone.utc).isoformat()
        else:
            question.created_by = request.user

        question.space = space
        question.save()

        return redirect('questions:save_success', space_id=space_id, id=question.id)

    return render(request, 'questions/save_form.html', {'form': form, 'space': space})

@login_required
def save_success(request, space_id, id):
    return render(request, 'questions/save_success.html', {'space_id': space_id, 'id': id})

@login_required
def upvote(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    question = get_object_or_404(Question, pk=id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('questions:view', space_id=space.id, id=question.id)

    if request.user not in question.upvoters.all():
        if request.user in question.downvoters.all():
            question.downvoters.remove(request.user)
            Question.objects.filter(pk=id).update(score=F('score') + 2)
        else:
            Question.objects.filter(pk=id).update(score=F('score') + 1)

        question.upvoters.add(request.user)
    else:
        question.upvoters.remove(request.user)
        Question.objects.filter(pk=id).update(score=F('score') - 1)

    return redirect('questions:view', space_id=space.id, id=question.id)

@login_required
def downvote(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    question = get_object_or_404(Question, pk=id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('questions:view', space_id=space.id, id=question.id)

    if request.user not in question.downvoters.all():
        if request.user in question.upvoters.all():
            question.upvoters.remove(request.user)
            Question.objects.filter(pk=id).update(score=F('score') - 2)
        else:
            Question.objects.filter(pk=id).update(score=F('score') - 1)

        question.downvoters.add(request.user)
    else:
        question.downvoters.remove(request.user)
        Question.objects.filter(pk=id).update(score=F('score') + 1)

    return redirect('questions:view', space_id=space.id, id=question.id)

@login_required
def upvote_answer(request, space_id, question_id, id):
    space = get_object_or_404(Space, pk=space_id)
    question = get_object_or_404(Question, pk=question_id, space__id=space.id)
    answer = get_object_or_404(Answer, pk=id, question__id=question.id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('questions:view', space_id=space.id, id=question.id)

    if request.user not in answer.upvoters.all():
        if request.user in answer.downvoters.all():
            answer.downvoters.remove(request.user)
            Answer.objects.filter(pk=id).update(score=F('score') + 2)
        else:
            Answer.objects.filter(pk=id).update(score=F('score') + 1)

        answer.upvoters.add(request.user)
    else:
        answer.upvoters.remove(request.user)
        Answer.objects.filter(pk=id).update(score=F('score') - 1)

    return redirect('questions:view', space_id=space.id, id=question.id)

@login_required
def downvote_answer(request, space_id, question_id, id):
    space = get_object_or_404(Space, pk=space_id)
    question = get_object_or_404(Question, pk=question_id, space__id=space.id)
    answer = get_object_or_404(Answer, pk=id, question__id=question.id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('questions:view', space_id=space.id, id=question.id)

    if request.user not in answer.downvoters.all():
        if request.user in answer.upvoters.all():
            answer.upvoters.remove(request.user)
            Answer.objects.filter(pk=id).update(score=F('score') - 2)
        else:
            Answer.objects.filter(pk=id).update(score=F('score') - 1)

        answer.downvoters.add(request.user)
    else:
        answer.downvoters.remove(request.user)
        Answer.objects.filter(pk=id).update(score=F('score') + 1)

    return redirect('questions:view', space_id=space.id, id=question.id)
