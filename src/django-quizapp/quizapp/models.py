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
        ordering = ['-created_at']

    def __unicode__(self):
        return self.name

class Question(models.Model):
    content = models.TextField()
    ordinal = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz)
    answer = models.TextField(null=True, blank=True)
    multiple_choice_answer = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        ordering = ['ordinal']
        unique_together = ('ordinal', 'quiz')

    def get_content_summary(self):
        content_words = self.content.split()
        if len(content_words) < 10:
            return self.content
        else:
            return u'{}...'.format(' '.join(content_words[:7]))

    def is_multiple_choice(self):
        return True if self.multiple_choice_answer else False

    def __unicode__(self):
        return u'<Question: {}>'.format(self.get_content_summary())

class Choice(models.Model):
    content = models.TextField()
    letter = models.CharField(max_length=1)
    question = models.ForeignKey(Question)

    class Meta(object):
        ordering = ['letter']
        unique_together = ('letter', 'question')

    def __unicode__(self):
        return u'<Choice: {}>'.format(self.content)

class PlayerAnswer(models.Model):
    essay_answer = models.TextField(null=True, blank=True)
    multiple_choice_answer = models.CharField(max_length=1, null=True, blank=True)
    session = models.ForeignKey(QuizSession)
    player = models.ForeignKey(User)
    question = models.ForeignKey(Question)

    def add_answer(self, answer):
        if self.question.is_multiple_choice():
            self.multiple_choice_answer = answer
        else:
            self.essay_answer = answer

    def __unicode__(self):
        return u'<Answer: <Player: {}> {}>'.format(self.player, self.question)

class Score(models.Model):
    score = models.DecimalField(max_digits=5, decimal_places=2)
    session = models.ForeignKey(QuizSession)
    player = models.ForeignKey(User)

    def __unicode__(self):
        return u'<Score {} -- Player {}>'.format(self.score, self.player)
