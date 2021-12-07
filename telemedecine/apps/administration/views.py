from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from telemedecine.apps.core.models.hospital_models import *
from .forms import AddProviderForm
from telemedecine.apps.authentication.models import (
    CustomUser,
    CustomUserManager,
)
import uuid
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.


def load_providers():
    providers = Institution.objects.all()
    return providers


@login_required
def dashboard(request):
    return render(request, "administration/main.html")


class Providers(View):
    def get(self, request):
        form = AddProviderForm()
        providers = load_providers()
        context = {"providers": providers, "form": form}
        return render(request, "superadmin/providers.html", context=context)

    def post(self, request):
        providers = load_providers()
        if request.method == "POST":
            form = AddProviderForm(data=request.POST)
            if form.is_valid():
                provider_name = request.POST["provider_name"]
                country = request.POST["country"]
                state = request.POST["state"]
                city = request.POST["city"]
                specialization = request.POST["specialization"]
                admin_mail = request.POST["admin_mail"]
                try:
                    admin_user = CustomUser.objects.get(email=admin_mail)
                except CustomUser.DoesNotExist:
                    temp_password = uuid.uuid4().hex[:6].upper()
                    admin_user = CustomUser.objects.create_user(
                        admin_mail, temp_password
                    )
                    admin_user.save()
                    send_mail(
                        "Telemedecine User Creation",
                        "Hi "
                        + admin_user.email
                        + " Your Generated Password is "
                        + temp_password
                        + " Please change it and create your own",
                        " telemedecine@gmail.com",
                        [admin_mail],
                        fail_silently=False,
                    )

                provider = Institution.objects.create(
                    institution_name=provider_name,
                    country=country,
                    state=state,
                    city=city,
                    default_admin=admin_user,
                )
                if specialization:
                    provider.specialization = specialization

                provider.save()
                send_mail(
                    "Telemedecine User Creation",
                    "Hi "
                    + admin_user.email
                    + " Welcome to Telemedecine, please use your credentials to log into the system ",
                    " telemedecine@gmail.com",
                    [admin_mail],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    "Institution created successfully!",
                )

            else:
                messages.error(
                    request, "Institution not created, Please check each field!"
                )
                form = AddProviderForm()

        else:
            form = AddProviderForm()
            return render(
                request,
                "superadmin/providers.html",
                context={"form": form, "providers": providers},
            )
        form = AddProviderForm()
        return redirect(
            "administration:providers",
        )


def delete_provider(request, id):
    provider = Institution.objects.get(id=id)
    if provider:
        provider.delete()
        messages.success(
            request,
            "Institution deleted successfully",
        )
    else:
        messages.error(
            request,
            "Couldn't delete institution",
        )
    return redirect("administration:providers")
