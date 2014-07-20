from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from quizapp.forms import QuizForm, QuestionForm, QuizSessionForm
from quizapp.models import *
import json
import logging
logger = logging.getLogger(__name__)

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
        return redirect(reverse('quizapp.views.choose_app'))
    else:
        return redirect(reverse('quizapp.views.quiz_dashboard'))

@permission_required('user.is_staff')
def choose_app(request, template_name='choose_app.html'):
    return render(request, template_name, {})

#################################  Quiz Views  #################################

@login_required
def quiz_dashboard(request, template_name='quiz/dashboard.html'):
    quiz_sessions = QuizSession.objects.filter(ended_at=None, is_private=False)
    return render(request, template_name, {'quiz_sessions': quiz_sessions})

@login_required
def create_session(request, template_name='quiz/create_session.html'):
    
    form = QuizSessionForm()

    if request.method == 'POST':
        form = QuizSessionForm(request.POST)
        if form.is_valid():
            quiz_session = form.save(commit=False)
            quiz_session.created_by = request.user
            quiz_session.save()
            return redirect(reverse('quizapp.views.quiz_dashboard'))

    return render(request, template_name, {'form':form})

@login_required
def quiz(request, session_id, template_name='quiz/quiz.html'):

    quiz_session = get_object_or_404(QuizSession, id=session_id)
    quiz = quiz_session.quiz
    questions = Question.objects.filter(quiz=quiz)
    question_ids = questions.values_list('id', flat=True)
    quiz_questions = { question:Choice.objects.filter(question=question) for question in questions }

    if request.method == 'POST':
        if request.is_ajax():
            question_id = int(request.GET['question_id'])
            answer, created = PlayerAnswer.objects.get_or_create(
                question=Question.objects.get(id=question_id), 
                player=request.user,
                session=quiz_session,
            )
            answer.add_answer(request.POST.get('answer'))
            answer.save()
            answer_json = json.dumps({ 'answer_id': answer.id, 'answer_content': answer.essay_answer })
            return HttpResponse(answer_json, content_type="application/json")

    answer_vals = PlayerAnswer.objects.filter(session=quiz_session, player=request.user).values('question', 'essay_answer', 'multiple_choice_answer')
    answers = { int(answer['question']): {'essay':answer['essay_answer'],'mult_choice':answer['multiple_choice_answer']}  for answer in answer_vals }
    answers = json.dumps(answers)

    return render(request, template_name, 
        {'quiz_questions': quiz_questions,
         'quiz': quiz,
         'question_ids':question_ids,
         'answers': answers}
    )


#################################  Management Views  #################################

@permission_required('user.is_staff')
def manage_index(request, template_name='manage/index.html'):
    return render(request, template_name, {})

@permission_required('user.is_staff')
def manage_dashboard(request, template_name='../ajax/dashboard.html'):
    return render(request, template_name, {})

@permission_required('user.is_staff')
def edit_quiz(request, quiz_id=None, template_name='manage/edit_quiz.html'):

    try:
        quiz = get_object_or_404(Quiz, id=quiz_id) if quiz_id else None

        if quiz:
            form = QuizForm(instance=quiz)
        else:
            form = QuizForm()

        if request.method == 'POST' and request.is_ajax():
            logger.info(request.POST)
            form = QuizForm(request.POST, instance=quiz) if quiz else QuizForm(request.POST)
            if form.is_valid():
                q = form.save()
                return HttpResponse(json.dumps({'quiz_id': q.id}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'message': 'error'}), content_type='application/json')

        return render(request, template_name, {'quiz':quiz, 'form':form})
    except:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)

@permission_required('user.is_staff')
def add_questions(request, quiz_id, template_name='manage/add_questions.html'):
    questions = Question.objects.filter(is_deleted=False, quiz__id=quiz_id)
    return render(request, template_name, {'questions':questions})

@permission_required('user.is_staff')
def quiz_selector(request, template_name='manage/quiz_selector.html'):
    quizzes = Quiz.objects.filter(is_deleted=False)
    return render(request, template_name, {'quizzes':quizzes})

@permission_required('user.is_staff')
def quiz_timeline(request, template_name='manage/quiz_timeline.html'):
    return render(request, template_name, {})

@permission_required('user.is_staff')
def course_overview(request, template_name='manage/course_overview.html'):
    courses = Course.objects.all()
    return render(request, template_name, {'courses': courses})

@permission_required('user.is_staff')
def student_overview(request, template_name='manage/student_overview.html'):
    students = User.objects.all()
    return render(request, template_name, {'students': students})