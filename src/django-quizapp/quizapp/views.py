from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from quizapp.models import *
import json

#################################  Registration  #################################

def logout(request):
    auth_logout(request)
    return redirect("/")


def login(request, template_name='login.html'):
    message = None

    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('/')
                else:
                    message = "Your account has been disabled!"
            else:
                message = "Your username and password were incorrect."

    return render(request, template_name, {'message':message})

@login_required
def change_password(request, template_name='change_password.html'):
    change_password_form = PasswordChangeForm(request.user)
    message = ''

    if request.POST:
        change_password_form = PasswordChangeForm(request.user, data=request.POST)
        if change_password_form.is_valid():
            change_password_form.save()
            message = 'Your password has been changed.'

    return render(request, template_name, {'change_password_form':change_password_form, 'message': message})


@login_required
def index(request):
    if request.user.is_staff:
        return redirect(reverse('quizapp.views.manage_index'))
    else:
        return redirect(reverse('quizapp.views.quiz_dashboard'))

#################################  Quiz Views  #################################

@login_required
def quiz_dashboard(request, template_name='quiz/dashboard.html'):
    quiz_sessions = QuizSession.objects.filter(ended_at=None)
    return render(request, template_name, {'quiz_sessions': quiz_sessions})


@login_required
def quiz(request, session_id, template_name='quiz/quiz.html'):

    quiz_session = get_object_or_404(QuizSession, id=session_id)
    quiz = quiz_session.quiz
    quiz_questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        if request.is_ajax():
            question_id = int(request.GET['question_id'])
            answer, created = PlayerAnswer.objects.get_or_create(
                question=Question.objects.get(id=question_id), 
                player=request.user,
                session=quiz_session,
            )
            answer.content = request.POST.get('answer')
            answer.save()
            answer_json = json.dumps({ 'answer_id': answer.id, 'answer_content': answer.content })
            return HttpResponse(answer_json, content_type="application/json")

    answers = PlayerAnswer.objects.filter(session=quiz_session, player=request.user).values_list('question', 'content')
    answers = { int(answer[0]): answer[1] for answer in answers }
    answers = json.dumps(answers)

    return render(request, template_name, {'quiz_questions': quiz_questions, 'quiz':quiz, 'answers': answers})


#################################  Management Views  #################################

@permission_required('user.is_staff')
def manage_index(request, template_name='manage/index.html'):
    return render(request, template_name, {})

@permission_required('user.is_staff')
def manage_dashboard(request, template_name='manage/dashboard.html'):
    return render(request, template_name, {})