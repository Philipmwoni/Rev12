from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Rev Core App!")


#the user already created the account!!!
def login(request):
    if request.method== "POST":
        usernamame= request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request, username=username , password=password)

        if user is not None:
            login(request,user)


    
        else:
            messages.error(request,"invalid username or password")



    return render(request,"login.html")