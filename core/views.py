from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserForm
from .models import Expense, User
from .serializers import UserSerializer, ExpenseSerializer
from rest_framework import generics

from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "homepage.html")

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"expenses": expenses})


def register_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserForm()

    return render(request, "register.html", {"form": form})


#the user already created the account!!!
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
