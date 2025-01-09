from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.
def register(request):
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

                return redirect("index")
        else:
            message = "Please fill all input fields with valid data."
            
        context = {
            "form": reg_form,
            "message": message
        }

    return render(request, "users/register.html", context)
