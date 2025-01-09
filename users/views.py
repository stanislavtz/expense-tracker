from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    reg_form = RegisterForm()
    message = None

    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data.get("username")
            email = reg_form.cleaned_data.get("email")
            first_name = reg_form.cleaned_data.get("first_name")
            last_name = reg_form.cleaned_data.get("last_name")
            password = reg_form.cleaned_data.get("password")
            repeat_password = reg_form.cleaned_data.get("repeat_password")

            if password != repeat_password:
                message = "Password not match."
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )

                return redirect("login")
        else:
            message = "Please fill all input fields with valid data."
           
    context = {
        "form": reg_form,
        "message": message
    }

    return render(request, "users/register.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("index")

    login_form = LoginForm()
    message = None

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user=user)
                return redirect("index")
            else:
                message = "Invalid username or password!"
        else:
            message = "Please fill all input fields with valid data."

    context = {
        "form": login_form,
        "message": message
    }

    return render(request, "users/login.html", context)


@login_required
def logout_user(request):
    logout(request)
    return redirect("index")
