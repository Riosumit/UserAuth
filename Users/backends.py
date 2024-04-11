from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request,email=None, username=None, password=None, **kwargs):
        try:
            if email:
                user = User.objects.get(email=email)
            elif username:
                user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None