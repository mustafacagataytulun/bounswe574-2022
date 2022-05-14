from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from spaces.models import Space

from .forms import QuizSaveForm
from .models import Answer, Quiz

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
