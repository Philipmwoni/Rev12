from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ActivationCode
from .utils import generate_activation_code
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


class ActivationCodeView(APIView):
    
