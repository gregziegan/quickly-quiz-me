from django.conf.urls import *
from django.shortcuts import *
from django.conf import settings

admin_patterns = patterns('quizapp.views',
    url(r'^dashboard/$', 'admin_dashboard', name="admin_dashboard"),
)

quiz_patterns = patterns('quizapp.views',
    url(r'^dashboard/$', 'quiz_dashboard', name="quiz_dashboard"),
)

urlpatterns = patterns(
    'quizapp.views',
    url(r'^$', 'index', name="index"),
    url(r'^(?i)login$', 'login', name="login"),
    url(r'^(?i)logout$', 'logout', name="logout"),
    url(r'^(?i)change-password/?$', 'change_password', name="change_password"),
    url(r'^manage/', include(admin_patterns)),
    url(r'^participate/', include(quiz_patterns))
)

