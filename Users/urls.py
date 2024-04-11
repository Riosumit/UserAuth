from django.urls import path
from .views import register_user, email_verification, login_user, forgot_password, reset_password

urlpatterns = [
    path('register', register_user, name='register'),
    path('verification', email_verification, name='email_verification'),
    path('login', login_user, name='login'),
    path('forgot-password', forgot_password, name='forgot_password'),
    path('reset-password', reset_password, name='reset_password'),
]
