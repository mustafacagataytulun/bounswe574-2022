from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from spaces.models import Space

from .forms import QuizSaveForm
from .models import Answer, Quiz

def view(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    quiz = get_object_or_404(Quiz, pk=id)
    answers = Answer.objects.filter(quiz__id = id)
    has_user_joined = request.user.is_authenticated and request.user.has_joined_to_space(space_id)

    is_user_answer_correct = False

    if request.method == "POST":
        user_answer = get_object_or_404(Answer, pk=request.POST['attempted_answer_id'])

        if user_answer.is_correct:
            is_user_answer_correct = user_answer.is_correct

    return render(request, 'quizzes/view.html', {
        'space': space,
        'quiz': quiz,
        'user': request.user,
        'has_user_joined':has_user_joined,
        'answers': answers,
        'attempted_answer_id': int(request.POST.get('attempted_answer_id', 0)),
        'is_user_answer_correct': is_user_answer_correct })

@login_required
def save(request, space_id, id=None):
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('quizzes:view', space_id=space_id, id=id)

    space = get_object_or_404(Space, pk=space_id)
    answers = None

    if id:
        quiz = get_object_or_404(Quiz, pk=id)
        answers = Answer.objects.filter(quiz__id=id).all()
    else:
        quiz = Quiz()

    if answers:
        form_answers_string = ''

        for answer in answers:
            if answer.is_correct:
                form_answers_string += '*'

            form_answers_string += answer.content + '\n'

        form = QuizSaveForm(request.POST or {**{'question': quiz.question, 'tags': quiz.tags, 'answers': form_answers_string }} or None, instance=quiz)
    else:
        form = QuizSaveForm(request.POST or None, instance=quiz)

    if request.method == "POST" and form.is_valid():
        quiz = form.save(commit=False)

        if id:
            quiz.updated_by = request.user
            quiz.updated_date = datetime.now(timezone.utc).isoformat()
        else:
            quiz.created_by = request.user

        quiz.space = space
        quiz.save()

        Answer.objects.filter(quiz__pk=quiz.id).delete()

        raw_answers = request.POST['answers'].splitlines()

        for raw_answer in raw_answers:
            answer = Answer()
            answer.content = raw_answer.lstrip('*')
            answer.created_by = request.user
            answer.quiz = quiz
            answer.is_correct = raw_answer.startswith('*')
            answer.save()

        return redirect('quizzes:save_success', space_id=space_id, id=quiz.id)

    return render(request, 'quizzes/save_form.html', {'form': form, 'space': space,})

@login_required
def save_success(request, space_id, id):
    return render(request, 'quizzes/save_success.html', {'space_id': space_id, 'id': id})

@login_required
def upvote(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    quiz = get_object_or_404(Quiz, pk=id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('quizzes:view', space_id=space.id, id=quiz.id)

    if request.user not in quiz.upvoters.all():
        if request.user in quiz.downvoters.all():
            quiz.downvoters.remove(request.user)
            Quiz.objects.filter(pk=id).update(score=F('score') + 2)
        else:
            Quiz.objects.filter(pk=id).update(score=F('score') + 1)

        quiz.upvoters.add(request.user)
    else:
        quiz.upvoters.remove(request.user)
        Quiz.objects.filter(pk=id).update(score=F('score') - 1)

    return redirect('quizzes:view', space_id=space.id, id=quiz.id)

@login_required
def downvote(request, space_id, id):
    space = get_object_or_404(Space, pk=space_id)
    quiz = get_object_or_404(Quiz, pk=id)
    has_user_joined = request.user.has_joined_to_space(space_id)

    if not has_user_joined:
        return redirect('quizzes:view', space_id=space.id, id=quiz.id)

    if request.user not in quiz.downvoters.all():
        if request.user in quiz.upvoters.all():
            quiz.upvoters.remove(request.user)
            Quiz.objects.filter(pk=id).update(score=F('score') - 2)
        else:
            Quiz.objects.filter(pk=id).update(score=F('score') - 1)

        quiz.downvoters.add(request.user)
    else:
        quiz.downvoters.remove(request.user)
        Quiz.objects.filter(pk=id).update(score=F('score') + 1)

    return redirect('quizzes:view', space_id=space.id, id=quiz.id)
