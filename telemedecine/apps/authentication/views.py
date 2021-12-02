from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import (
    login as telemedecine_login,
    logout as telemedecine_logout,
    authenticate as telemedecine_authenticate,
)

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
                if user.is_active:
                    telemedecine_login(request, user)
                    return redirect(
                        "/administration/dashboard"
                    )  # user is redirected to dashboard
    else:
        form = AuthenticationForm()

    return render(
        request,
        "auth/login.html",
        {
            "form": form,
        },
    )


# def admin_login(request):

#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             email = request.POST["email"]
#             password = request.POST["password"]
#             user = telemedecine_authenticate(email=email, password=password)
#             if user is not None:
#                 if user.is_active:
#                     telemedecine_login(request, user)
#                     return redirect(
#                         "administration:dashboard"
#                     )  # user is redirected to dashboard
#     else:
#         form = AuthenticationForm()

#     return render(
#         request,
#         "auth/login.html",
#         {
#             "form": form,
#         },
#     )


def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            u = telemedecine_authenticate(
                user.email == user, user.password == password
            )
            telemedecine_login(request, u)
            return redirect("/dashboard")
    else:
        form = RegistrationForm()

    return render(
        request,
        "register.html",
        {
            "form": form,
        },
    )


def logout(request):
    telemedecine_logout(request)
    return redirect("/")


@login_required(login_url="/")
def dashboard(request):
    return render(request, "dashboard.html", {})
