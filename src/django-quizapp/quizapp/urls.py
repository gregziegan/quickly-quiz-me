from django.conf.urls import *
from django.shortcuts import *
from django.conf import settings

manage_patterns = patterns('quizapp.views',
    url(r'^$', 'manage_index', name="manage_index"),
    url(r'^dashboard/$', 'manage_dashboard', name="manage_dashboard"),
    url(r'^create-quiz/$', 'edit_quiz', name="create_quiz"),
    url(r'^edit-quiz/(\d+)$', 'edit_quiz', name="edit_quiz"),
    url(r'^edit-quiz/(\d+)/add-questions/$', 'add_questions', name="add_questions"),
    url(r'^quiz-selector/$', 'quiz_selector', name="quiz_selector"),
    url(r'^quiz-timeline/$', 'quiz_timeline', name="quiz_timeline"),
    url(r'^course-overview/$', 'course_overview', name="course_overview"),
    url(r'^student-overview/$', 'student_overview', name="student_overview"),
)

quiz_patterns = patterns('quizapp.views',
    url(r'^dashboard/$', 'quiz_dashboard', name="quiz_dashboard"),
    url(r'^quiz-session/(\d+)/$', 'quiz', name="quiz"),
    url(r'^quiz-session/(\d+)/auto-save/$', 'quiz'),
)

urlpatterns = patterns(
    'quizapp.views',
    url(r'^$', 'index', name="index"),
    url(r'^(?i)login$', 'login', name="login"),
    url(r'^(?i)logout$', 'logout', name="logout"),
    url(r'^(?i)change-password/?$', 'change_password', name="change_password"),
    url(r'^manage/', include(manage_patterns)),
    url(r'^participate/', include(quiz_patterns))
)

