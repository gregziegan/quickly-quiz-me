from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

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
    course = models.ForeignKey(Course)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    answer_file = models.FileField(upload_to=get_quiz_answer_filepath, null=True, blank=True)

    def __unicode__(self):
        return self.name


class QuizUserManager(BaseUserManager):
    def create_user(self, email, case_id, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            case_id=case_id,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, case_id, password):
        user = self.create_user(email,
            case_id=case_id,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

 
class QuizUser(AbstractBaseUser):
    case_id = models.CharField(max_length=10)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = QuizUserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

class Session(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(QuizUser)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    quiz = models.ForeignKey(Quiz)

    def __unicode__(self):
        return u'Quiz - {} : {}\'s Session -- {}'.format(self.quiz, self.created_by, self.created_at)


class Question(models.Model):
    content = models.TextField()
    ordinal = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    session = models.ForeignKey(Session)
    answer = models.TextField()

    def __unicode__(self):
        content_words = self.content.split()
        if len(content_words) < 7:
            return self.content
        else:
            return u'{}...'.format(' '.join(content_words[:7]))


class PlayerAnswer(models.Model):
    content = models.TextField()
    session = models.ForeignKey(Session)
    player = models.ForeignKey(QuizUser)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        content_words = self.content.split()
        representation = self.player + u'\'s Answer: {}'
        if len(content_words) < 7:
            representation.format(self.content)
        else:
            representation.format(' '.join(content_words[:7]))
        return representation

