from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import OTP, User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
import random

# Create your views here.

def generate_otp(user_id, subject):
    otp_value = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    otp_instance, created = OTP.objects.get_or_create(user_id=user_id)
    otp_instance.otp = otp_value
    otp_instance.save()
    user_instance = User.objects.get(pk=user_id)
    send_mail(
        subject,
        f'Your OTP is: {otp_value}',
        'sendemail@gmail.com',
        [user_instance.email],
        fail_silently=False,
    )
    return otp_value

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        generate_otp(user.id,'Email Verification')
        return Response({
            'success' : True,
            'message' : 'User registered successfully',
            'data' : serializer.data
            }, status=status.HTTP_201_CREATED)
    return Response({
        'success' : False,
        'message' : "Validation Error",
        'errors' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def email_verification(request):
    username = request.data.get('username')
    email = request.data.get('email')
    otp = request.data.get('otp')
    errors = []
    if not email and not username:
        errors.append({"username/email": "Either username or email is required."})
    if not otp:
        errors.append({"otp": "This field is required."})
    if errors:
        return Response({
            'success': False,
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = None
    if username:
        user = User.objects.filter(username=username).first()
    else:
        user = User.objects.filter(email=email).first()

    if not user:
        return Response({
            'success': False,
            'message': "User not found"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    otp_instance = OTP.objects.filter(user=user, otp=otp)
    if otp_instance.exists():
        user.verified = True
        user.save()
        otp_instance.delete()
        return Response({
            'success': True,
            'message': "Verification successful",
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'message': "OTP doesn't match",
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    otp = request.data.get('otp')
    errors = []
    if not email and not username:
        errors.append({"username/email": "Either username or email is required."})
    if not otp:
        errors.append({"otp": "This field is required."})
    if errors:
        return Response({
            'success': False,
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, email=email, password=otp)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            "success" : True,
            "message" : "Loggedin Successfully",
            "data" : {"access_token": access_token, "refresh_token": refresh_token}
            }, status=status.HTTP_200_OK)
    else:
        return Response({
            "success" : False,
            "message" : "Invalid credentials!"
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def forgot_password(request):
    username = request.data.get('username')
    email = request.data.get('email')
    errors = []
    if not email and not username:
        errors.append({"username/email": "Either username or email is required."})
    if errors:
        return Response({
            'success': False,
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)
    user = None
    if username:
        user = User.objects.filter(username=username).first()
    else:
        user = User.objects.filter(email=email).first()

    if not user:
        return Response({
            'success': False,
            'message': "User not found"
        }, status=status.HTTP_400_BAD_REQUEST)
    generate_otp(user.id,'Forgot Password OTP')
    return Response({
        'success' : True,
        'message' : "OTP sent to email!"
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password(request):
    username = request.data.get('username')
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('password')
    errors = []
    
    if not email and not username:
        errors.append({"username/email": "Either username or email is required."})
    if not otp:
        errors.append({"otp": "This field is required."})
    if not new_password:
        errors.append({"password": "This field is required."})

    if errors:
        return Response({
            'success': False,
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = None
    if username:
        user = User.objects.filter(username=username).first()
    else:
        user = User.objects.filter(email=email).first()

    if not user:
        return Response({
            'success': False,
            'message': "User not found"
        }, status=status.HTTP_400_BAD_REQUEST)

    otp_instance = OTP.objects.filter(user=user, otp=otp)

    if not otp_instance.exists():
        return Response({
            'success': False,
            'message': "OTP doesn't match",
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    otp_instance.delete()

    return Response({
        'success': True,
        'message': "Password reset successfully!",
    }, status=status.HTTP_200_OK)