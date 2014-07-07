from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def get_quiz_answer_filepath(self, filename):
        filepath_format_string = settings.ANSWER_DIRECTORY
        answer_directory_filepath = filepath_format_string.format(self.name, filename)
        return answer_directory_filepath

class Course(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=200, unique=True)
    instructions = models.TextField(default="Answer the following questions to the best of your ability.")
    course = models.ForeignKey(Course)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    answer_file = models.FileField(upload_to=get_quiz_answer_filepath, null=True, blank=True)

    class Meta:
        verbose_name_plural = "quizzes"

    def __unicode__(self):
        return self.name

class QuizSession(models.Model):
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    quiz = models.ForeignKey(Quiz)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __unicode__(self):
        return self.name


class Question(models.Model):
    content = models.TextField()
    ordinal = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz)
    answer = models.TextField(null=True, blank=True)


    class Meta:
        ordering = ['ordinal']


    def __unicode__(self):
        content_words = self.content.split()
        if len(content_words) < 7:
            return self.content
        else:
            return u'{}...'.format(' '.join(content_words[:7]))


class PlayerAnswer(models.Model):
    content = models.TextField(null=True, blank=True)
    session = models.ForeignKey(QuizSession)
    player = models.ForeignKey(User)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        content_words = self.content.split()
        if len(content_words) < 7:
            representation = '{}\'s Answer: {}'.format(self.player, self.content)
        else:
            representation = '{}\'s Answer: {}'.format(self.player, ' '.join(content_words[:7]))
        return representation

