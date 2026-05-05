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


def home(request):
    context = {}
    return render(request, 'auth/home.html', context)


class ActivationCodeView(APIView):
    def post(self, request):
        # Add your activation code logic here
        return Response({"message": "Activation code endpoint"}, status=status.HTTP_200_OK)


def chart_data_api(request):
    # Add your chart data logic here
    return Response({"data": []}, status=status.HTTP_200_OK)
    
