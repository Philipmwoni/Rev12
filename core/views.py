from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserForm, ExpenseForm
from .models import Expense, User
from .serializers import UserSerializer, ExpenseSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   
#

from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "homepage.html")

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"expenses": expenses})


class UserRegistrationView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, "register.html", {"form": form})


    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            activation_code = generate_activation_code()
            ActivationCode.objects.create(user=user, code=activation_code)
            send_mail(
                'Your Activation Code',
                f'Your activation code is: {activation_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Registration successful! Please check your email for the activation code.")
            return redirect('login')
        return render(request, "register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

#CRUD FUNCTIONALITY FOR THE EXPENSES
#API ENDPOINTS FOR THE MODELS(class based views)



class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer   

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
