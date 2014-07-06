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
    instructions = models.TextField(default="Answer the following questions to the best of your ability.")
    course = models.ForeignKey(Course)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    answer_file = models.FileField(upload_to=get_quiz_answer_filepath, null=True, blank=True)

    class Meta:
        verbose_name_plural = "quizzes"

    def __unicode__(self):
        return self.name


class QuizUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, email, username, password=None):
        staff_user = self.create_user(email,
            username=username,
            password=password,
        )
        staff_user.is_staff = True
        staff_user.save(using=self._db)
        return staff_user


    def create_superuser(self, email, username, password):
        superuser = self.create_user(email,
            username=username,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser

 
class QuizUser(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )

    is_active = models.BooleanField(default=True)
    permission_level = models.SmallIntegerField(default=0)

    @property
    def is_staff(self):
        return self.permission_level >= 1

    @property
    def is_admin(self):
        return self.permission_level == 2

    objects = QuizUserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

class QuizSession(models.Model):
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
    quiz = models.ForeignKey(Quiz)
    answer = models.TextField()


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

