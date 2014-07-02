from django.contrib import admin
from quizapp.models import *

admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(QuizUser)
admin.site.register(QuizSession)
admin.site.register(Question)
admin.site.register(PlayerAnswer)