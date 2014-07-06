from django.conf import settings
from django.contrib.auth.models import check_password
from quizapp.models import QuizUser

class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            user = QuizUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except QuizUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = QuizUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except QuizUser.DoesNotExist:
            return None