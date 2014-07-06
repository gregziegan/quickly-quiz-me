from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from quizapp.forms import AuthenticationForm, RegistrationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse


#################################  Registration  #################################

def logout(request):
    auth_logout(request)
    return redirect("/")


def login(request, template_name='login.html'):
    message = None

    form = AuthenticationForm()

    print request.POST
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            print user
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('/')
                else:
                    message = "Your account has been disabled!"
            else:
                message = "Your email and password were incorrect."

    return render(request, template_name, {'message':message, 'form':form})

def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    return render('accounts/register.html', {'form': form})


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
        return redirect(reverse('quizapp.views.manage_dashboard'))
    else:
        return redirect(reverse('quizapp.views.quiz_dashboard'))

#################################  Quiz Views  #################################

@login_required
def quiz_dashboard(request, template_name='quiz/dashboard.html'):
    return render(request, template_name, {})


@login_required
def quiz(request, session_id, template_name='quiz.html'):

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
            answer_json = json.dumps({ answer.id: answer.content })
            return HttpResponse(answer_json, content_type="application/json")
        else:
            form = AnswerForm(request.POST, request.FILES)
            if form.is_valid():
                answer_file = form.cleaned_data['answer_file']
                return redirect(reverse('quizapp.views.quiz_dashboard'))

    form = AnswerForm()
    answers = PlayerAnswer.objects.filter(session=quiz_session, player=request.user).values_list('question', 'content')
    answers = { int(answer[0]): answer[1] for answer in answers }
    answers = json.dumps(answers)

    return render(request, template_name, {'quiz_questions': quiz_questions, 'answers': answers, 'form': form})


#################################  Management Views  #################################


@permission_required('quizuser.is_staff')
def manage_dashboard(request, template_name='manage/dashboard.html'):
    return render(request, template_name, {})