from django.conf.urls import *
from django.shortcuts import *
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^$', 'quizapp.views.index', name="index"),
    url(r'^(?i)login$', 'quizapp.views.login', name="login"),
    url(r'^(?i)logout$', 'quizapp.views.logout', name="logout"),
    url(r'^(?i)change-password/?$', 'quizapp.views.change_password', name="change_password"),
)
