from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import (
    login as telemedecine_login,
    logout as telemedecine_logout,
    authenticate as telemedecine_authenticate,
)
from django.contrib import messages

# importing as such so that it doesn't create a confusion with our methods and django's default methods

from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, RegistrationForm


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = telemedecine_authenticate(email=email, password=password)
            if user is not None:
                if user.is_active and user.is_staff:
                    telemedecine_login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return redirect(
                        "administration:providers"
                    )  # user is redirected to dashboard
                elif user.is_active and user.user_role.role == "A":
                    telemedecine_login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return redirect(
                        "administration:doctors"
                    )  # user is redirected to dashboard
            else:
                messages.error(
                    request, "Username or Password incorrect, Please try again"
                )
                form = AuthenticationForm()
        else:
            messages.error(
                request, "Please enter a valid email and a valid password"
            )
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()

    return render(
        request,
        "auth/login.html",
        {
            "form": form,
        },
    )


def logout(request):
    telemedecine_logout(request)
    messages.success(request, "Logged out successfully, see you soon")
    return redirect("/")


@login_required(login_url="/")
def dashboard(request):
    return render(request, "dashboard.html", {})
