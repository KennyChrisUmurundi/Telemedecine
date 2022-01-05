import logging
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from telemedecine.apps.core.models.hospital_models import (
    Institution,
    Pharmacist,
    Doctor,
    LabSpecialist,
    Patient,
    Nurse,
    Receptionist,
)
from telemedecine.apps.core.models.administration import Role
from .forms import (
    AddProviderForm,
    UpdateProviderForm,
    AddDoctorForm,
    AddPharmacistForm,
    AddLabForm,
    AddReceptionistForm,
    AddNurseForm,
    AddPatientForm,
)
from telemedecine.apps.authentication.models import (
    CustomUser,
    CustomUserManager,
)

# from django.contrib.auth import get_user_model

import uuid
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

logging.getLogger(__name__)


def is_telemedecine_super_admin(user):
    if user.is_staff:
        return True
    else:
        return False
    return False


def load_providers():
    providers = Institution.objects.all()
    return providers


def get_institution(user):
    try:
        resp = Institution.objects.get(id=user)
    except Institution.DoesNotExist as err:
        logging.debug("INSTITUTION NOT FOUND:%s" % err)
        resp = None
    return resp


@login_required
def dashboard(request):
    return render(request, "administration/main.html")


class Providers(View):
    # @method_decorator(user_passes_test(is_telemedecine_super_admin))
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
                if not admin_mail:
                    messages.error("Email must be set")
                try:
                    admin_user = CustomUser.objects.get(email=admin_mail)
                except CustomUser.DoesNotExist:
                    temp_password = uuid.uuid4().hex[:6].upper()
                    admin_user = CustomUser.objects.create_user(
                        admin_mail, temp_password
                    )
                    admin_user.save()
                    try:
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
                    except BaseException:
                        pass
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
                try:
                    role = Role.objects.get(
                        user=admin_user,
                        institution=provider,
                        role=Role.ADMIN,
                    )
                except Role.DoesNotExist:
                    role = Role.objects.create(
                        user=admin_user,
                        institution=provider,
                        role=Role.ADMIN,
                    )
                    role.save()
                try:
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
                except BaseException:
                    pass

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


class UpdateProvider(LoginRequiredMixin, UpdateView):

    model = Institution
    template_name = "superadmin/edit_provider.html"
    form_class = UpdateProviderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        con = self.object.pk
        context["pk"] = con
        context["provider"] = Institution.objects.get(id=con)
        return context


class UserList(View):
    def get(self, request):
        users = CustomUser.objects.all()
        # role = Role.objects.all()
        context = {"users": users}
        return render(request, "superadmin/users.html", context=context)


class DoctorView(View):
    def get(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        # print(institution)
        logging.debug("INSTITUTION :%s" % institution)
        doctors = Doctor.objects.filter(institution=institution)
        form = AddDoctorForm()
        context = {"doctors": doctors, "form": form}
        return render(request, "administration/doctors.html", context=context)

    def post(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        if request.method == "POST":
            form = AddDoctorForm(data=request.POST)
            if form.is_valid():
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                country = request.POST["country"]
                email = request.POST["email"]
                gender = request.POST["gender"]
                speciality = request.POST["speciality"]
                publication = request.POST["publication"]
                licence_number = request.POST["licence_number"]

                try:
                    user = CustomUser.objects.get(email=email)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                except CustomUser.DoesNotExist:
                    temp_password = uuid.uuid4().hex[:6].upper()
                    user = CustomUser.objects.create_user(email, temp_password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    try:
                        send_mail(
                            "Telemedecine User Creation",
                            "Hi "
                            + user.email
                            + " Your Generated Password is "
                            + temp_password
                            + " Please change it and create your own",
                            " telemedecine@gmail.com",
                            [email],
                            fail_silently=False,
                        )
                    except BaseException:
                        pass

                try:
                    existing_role = Role.objects.get(user=user)
                    messages.error(
                        request,
                        "The Email entered already has a role in the system, Kindly check the system users page.",
                    )
                    form = AddDoctorForm()
                    return redirect(
                        "administration:doctors",
                    )
                except Role.DoesNotExist:
                    pass

                try:
                    role = Role.objects.get(
                        user=user, institution=institution, role=Role.DOCTOR
                    )
                except Role.DoesNotExist:
                    role = Role.objects.create(
                        user=user, institution=institution, role=Role.DOCTOR
                    )
                    role.save()
                doctor = Doctor.objects.create(
                    institution=institution,
                    user=user,
                    speciality=speciality,
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    email=email,
                    gender=gender,
                )
                if publication:
                    doctor.publication = publication
                elif licence_number:
                    doctor.licence_number = licence_number
                doctor.save()
                try:
                    send_mail(
                        "Telemedecine User Creation",
                        "Hi "
                        + user.email
                        + " Welcome to Telemedecine, please use your credentials to log into the system ",
                        " telemedecine@gmail.com",
                        [email],
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        "Doctor created successfully!",
                    )
                except BaseException:
                    pass
            else:
                messages.error(
                    request, "Doctor not created, Please check each field!"
                )
                form = AddDoctorForm()
        else:
            form = AddDoctorForm()
            return render(
                request,
                "superadmin/doctors.html",
                context={"form": form, "doctors": doctors},
            )
        form = AddDoctorForm()
        return redirect(
            "administration:doctors",
        )


def delete_doctor(request, id):
    doctor = Doctor.objects.get(id=id)
    if doctor:
        doctor.delete()
        messages.success(
            request,
            "Doctor deleted successfully",
        )
    else:
        messages.error(
            request,
            "Couldn't delete doctor",
        )
    return redirect("administration:doctors")


class PharmacistView(View):
    def get(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        # print(institution)
        logging.debug("INSTITUTION :%s" % institution)
        pharmacists = Pharmacist.objects.filter(institution=institution)
        form = AddPharmacistForm()
        context = {"pharmacists": pharmacists, "form": form}
        return render(
            request, "administration/pharmacist.html", context=context
        )

    def post(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        if request.method == "POST":
            form = AddPharmacistForm(data=request.POST)
            if form.is_valid():
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                country = request.POST["country"]
                email = request.POST["email"]
                gender = request.POST["gender"]
                # publication = request.POST["publication"]
                licence_number = request.POST["licence_number"]

                try:
                    user = CustomUser.objects.get(email=email)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                except CustomUser.DoesNotExist:
                    temp_password = uuid.uuid4().hex[:6].upper()
                    user = CustomUser.objects.create_user(email, temp_password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    try:
                        send_mail(
                            "Telemedecine User Creation",
                            "Hi "
                            + user.email
                            + " Your Generated Password is "
                            + temp_password
                            + " Please change it and create your own",
                            " telemedecine@gmail.com",
                            [email],
                            fail_silently=False,
                        )
                    except BaseException:
                        pass

                try:
                    existing_role = Role.objects.get(user=user)
                    messages.error(
                        request,
                        "The Email entered already has a role in the system, Kindly check the system users page.",
                    )
                    form = AddPharmacistForm()
                    return redirect(
                        "administration:pharmacists",
                    )
                except Role.DoesNotExist:
                    pass

                try:
                    role = Role.objects.get(
                        user=user, institution=institution, role=Role.PHARMACIST
                    )
                except Role.DoesNotExist:
                    role = Role.objects.create(
                        user=user, institution=institution, role=Role.PHARMACIST
                    )
                    role.save()
                pharmacist = Pharmacist.objects.create(
                    institution=institution,
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    email=email,
                    gender=gender,
                )
                # if publication:
                #     pharmacist.publication = publication
                if licence_number:
                    pharmacist.licence_number = licence_number
                pharmacist.save()
                try:
                    send_mail(
                        "Telemedecine User Creation",
                        "Hi "
                        + user.email
                        + " Welcome to Telemedecine, please use your credentials to log into the system ",
                        " telemedecine@gmail.com",
                        [email],
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        "Pharmacist created successfully!",
                    )
                except BaseException:
                    pass
            else:
                messages.error(
                    request, "Pharmacist not created, Please check each field!"
                )
                form = AddPharmacistForm()
        else:
            form = AddPharmacistForm()
            return render(
                request,
                "administration/pharmacists.html",
                context={"form": form, "pharmacists": pharmacists},
            )
        form = AddPharmacistForm()
        return redirect(
            "administration:pharmacists",
        )


def delete_pharmacist(request, id):
    pharmacist = Pharmacist.objects.get(id=id)
    if pharmacist:
        pharmacist.delete()
        messages.success(
            request,
            "Pharmacist deleted successfully",
        )
    else:
        messages.error(
            request,
            "Couldn't delete Pharmacist",
        )
    return redirect("administration:pharmacists")


class LaboratoryView(View):
    def get(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        # print(institution)
        logging.debug("INSTITUTION :%s" % institution)
        lab_specialist = LabSpecialist.objects.filter(institution=institution)
        form = AddLabForm()
        context = {"objects": lab_specialist, "form": form}
        return render(request, "administration/lab.html", context=context)

    def post(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        if request.method == "POST":
            form = AddLabForm(data=request.POST)
            if form.is_valid():
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                country = request.POST["country"]
                email = request.POST["email"]
                gender = request.POST["gender"]
                # publication = request.POST["publication"]
                licence_number = request.POST["licence_number"]

                try:
                    user = CustomUser.objects.get(email=email)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                except CustomUser.DoesNotExist:
                    temp_password = uuid.uuid4().hex[:6].upper()
                    user = CustomUser.objects.create_user(email, temp_password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    try:
                        send_mail(
                            "Telemedecine User Creation",
                            "Hi "
                            + user.email
                            + " Your Generated Password is "
                            + temp_password
                            + " Please change it and create your own",
                            " telemedecine@gmail.com",
                            [email],
                            fail_silently=False,
                        )
                    except BaseException:
                        pass

                try:
                    existing_role = Role.objects.get(user=user)
                    messages.error(
                        request,
                        "The Email entered already has a role in the system, Kindly check the system users page.",
                    )
                    form = AddLabForm()
                    return redirect(
                        "administration:lab",
                    )
                except Role.DoesNotExist:
                    pass

                try:
                    role = Role.objects.get(
                        user=user,
                        institution=institution,
                        role=Role.LAB_SPECIALIST,
                    )
                except Role.DoesNotExist:
                    role = Role.objects.create(
                        user=user,
                        institution=institution,
                        role=Role.LAB_SPECIALIST,
                    )
                    role.save()
                lab_specialist = LabSpecialist.objects.create(
                    institution=institution,
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    email=email,
                    gender=gender,
                )
                if licence_number:
                    lab_specialist.licence_number = licence_number
                lab_specialist.save()
                try:
                    send_mail(
                        "Telemedecine User Creation",
                        "Hi "
                        + user.email
                        + " Welcome to Telemedecine, please use your credentials to log into the system ",
                        " telemedecine@gmail.com",
                        [email],
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        "Lab Specialist created successfully!",
                    )
                except BaseException:
                    pass
            else:
                messages.error(
                    request,
                    "Lab Specialist not created, Please check each field!",
                )
                form = AddLabForm()
        else:
            form = AddLabForm()
            return render(
                request,
                "administration/lab.html",
                context={"form": form, "pharmacists": pharmacists},
            )
        form = AddLabForm()
        return redirect(
            "administration:lab",
        )


def delete_laboratorist(request, id):
    lab = LabSpecialist.objects.get(id=id)
    if lab:
        lab.delete()
        messages.success(
            request,
            "Lab Specialist deleted successfully",
        )
    else:
        messages.error(
            request,
            "Couldn't delete LabSpecialist",
        )
    return redirect("administration:lab")


class SystemUser(View):
    def get(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        users = Role.objects.filter(institution=institution)

        context = {"users": users}
        return render(request, "administration/system_users.html", context)


class ReceptionistView(View):
    def get(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        # print(institution)
        logging.debug("INSTITUTION :%s" % institution)
        receptionist = Receptionist.objects.filter(institution=institution)
        form = AddReceptionistForm()
        context = {"objects": receptionist, "form": form}
        return render(
            request, "administration/receptionist.html", context=context
        )

    def post(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        if request.method == "POST":
            form = AddReceptionistForm(data=request.POST)
            if form.is_valid():
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                country = request.POST["country"]
                email = request.POST["email"]
                gender = request.POST["gender"]
                # publication = request.POST["publication"]
                # licence_number = request.POST["licence_number"]

                try:
                    user = CustomUser.objects.get(email=email)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                except CustomUser.DoesNotExist:
                    temp_password = uuid.uuid4().hex[:6].upper()
                    user = CustomUser.objects.create_user(email, temp_password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    try:
                        send_mail(
                            "Telemedecine User Creation",
                            "Hi "
                            + user.email
                            + " Your Generated Password is "
                            + temp_password
                            + " Please change it and create your own",
                            " telemedecine@gmail.com",
                            [email],
                            fail_silently=False,
                        )
                    except BaseException:
                        pass

                try:
                    existing_role = Role.objects.get(user=user)
                    messages.error(
                        request,
                        "The Email entered already has a role in the system, Kindly check the system users page.",
                    )
                    form = AddLabForm()
                    return redirect(
                        "administration:receptionist",
                    )
                except Role.DoesNotExist:
                    pass

                try:
                    role = Role.objects.get(
                        user=user,
                        institution=institution,
                        role=Role.RECEPTIONIST,
                    )
                except Role.DoesNotExist:
                    role = Role.objects.create(
                        user=user,
                        institution=institution,
                        role=Role.RECEPTIONIST,
                    )
                    role.save()
                receptionist = Receptionist.objects.create(
                    institution=institution,
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    email=email,
                    gender=gender,
                )
                receptionist.save()
                try:
                    send_mail(
                        "Telemedecine User Creation",
                        "Hi "
                        + user.email
                        + " Welcome to Telemedecine, please use your credentials to log into the system ",
                        " telemedecine@gmail.com",
                        [email],
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        "Receptionist created successfully!",
                    )
                except BaseException:
                    pass
            else:
                messages.error(
                    request,
                    "Receptionist not created, Please check each field!",
                )
                form = AddLabForm()
        else:
            form = AddReceptionistForm()
            return render(
                request,
                "administration/receptionist.html",
                context={"form": form, "objects": receptionist},
            )
        form = AddReceptionistForm()
        return redirect(
            "administration:receptionist",
        )


def delete_receptionist(request, id):
    receptionist = Receptionist.objects.get(id=id)
    if receptionist:
        receptionist.delete()
        messages.success(
            request,
            "Receptionist deleted successfully",
        )
    else:
        messages.error(
            request,
            "Couldn't delete Receptionist",
        )
    return redirect("administration:receptionist")


class NurseView(View):
    def get(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        # print(institution)
        logging.debug("INSTITUTION :%s" % institution)
        nurses = Nurse.objects.filter(institution=institution)
        form = AddNurseForm()
        context = {"objects": nurses, "form": form}
        return render(request, "administration/nurse.html", context=context)

    def post(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        if request.method == "POST":
            form = AddReceptionistForm(data=request.POST)
            if form.is_valid():
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                country = request.POST["country"]
                email = request.POST["email"]
                gender = request.POST["gender"]
                is_practitioner = request.POST["is_practitioner"]
                # publication = request.POST["publication"]
                # licence_number = request.POST["licence_number"]

                try:
                    user = CustomUser.objects.get(email=email)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                except CustomUser.DoesNotExist:
                    temp_password = uuid.uuid4().hex[:6].upper()
                    user = CustomUser.objects.create_user(email, temp_password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    try:
                        send_mail(
                            "Telemedecine User Creation",
                            "Hi "
                            + user.email
                            + " Your Generated Password is "
                            + temp_password
                            + " Please change it and create your own",
                            " telemedecine@gmail.com",
                            [email],
                            fail_silently=False,
                        )
                    except BaseException:
                        pass

                try:
                    existing_role = Role.objects.get(user=user)
                    messages.error(
                        request,
                        "The Email entered already has a role in the system, Kindly check the system users page.",
                    )
                    form = AddLabForm()
                    return redirect(
                        "administration:nurse",
                    )
                except Role.DoesNotExist:
                    pass

                try:
                    role = Role.objects.get(
                        user=user,
                        institution=institution,
                        role=Role.NURSE,
                    )
                except Role.DoesNotExist:
                    role = Role.objects.create(
                        user=user,
                        institution=institution,
                        role=Role.NURSE,
                    )
                    role.save()
                nurse = Nurse.objects.create(
                    institution=institution,
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    email=email,
                    gender=gender,
                )
                if is_practitioner:
                    nurse.is_practitioner = True
                nurse.save()
                try:
                    send_mail(
                        "Telemedecine User Creation",
                        "Hi "
                        + user.email
                        + " Welcome to Telemedecine, please use your credentials to log into the system ",
                        " telemedecine@gmail.com",
                        [email],
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        "Nurse created successfully!",
                    )
                except BaseException:
                    pass
            else:
                messages.error(
                    request,
                    "Nurse not created, Please check each field!",
                )
                form = AddNurseForm()
        else:
            form = AddNurseForm()
            return render(
                request,
                "administration/nurse.html",
                context={"form": form, "objects": nurses},
            )
        form = AddReceptionistForm()
        return redirect(
            "administration:nurse",
        )


def delete_nurse(request, id):
    nurse = Nurse.objects.get(id=id)
    if nurse:
        nurse.delete()
        messages.success(
            request,
            "nurse deleted successfully",
        )
    else:
        messages.error(
            request,
            "Couldn't delete nurse",
        )
    return redirect("administration:nurse")


#### NEVER EVER DELETE A PATIENT RECORD
class PatientView(View):
    def get(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        # print(institution)
        logging.debug("INSTITUTION :%s" % institution)
        patients = Patient.objects.filter(institution=institution)
        form = AddPatientForm()
        context = {"objects": patients, "form": form}
        return render(request, "administration/patients.html", context=context)

    def post(self, request):
        institution = get_institution(
            self.request.user.user_role.institution_id
        )
        user = None
        if request.method == "POST":
            form = AddPatientForm(data=request.POST)
            if form.is_valid():
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                # country = request.POST["country"]
                email = request.POST["email"]
                gender = request.POST["gender"]
                address = request.POST["address"]
                phone_number = request.POST["phone_number"]
                age = request.POST["age"]
                # publication = request.POST["publication"]
                # licence_number = request.POST["licence_number"]
                if email:
                    try:
                        user = CustomUser.objects.get(email=email)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()
                    except CustomUser.DoesNotExist:
                        temp_password = uuid.uuid4().hex[:6].upper()
                        user = CustomUser.objects.create_user(
                            email, temp_password
                        )
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()

                    try:
                        send_mail(
                            "Telemedecine Patient Creation",
                            "Hi dear"
                            + user.email
                            + " Your Generated Password is "
                            + temp_password
                            + " Use it to login to our platform",
                            " telemedecine@gmail.com",
                            [email],
                            fail_silently=False,
                        )
                    except BaseException:
                        pass

                    try:
                        existing_role = Role.objects.get(user=user)
                        messages.error(
                            request,
                            "The Email entered already has a role in the system, Kindly check the system users page.",
                        )
                        form = AddPatientForm()
                        return redirect(
                            "administration:patient",
                        )
                    except Role.DoesNotExist:
                        pass

                    try:
                        role = Role.objects.get(
                            user=user,
                            institution=institution,
                            role=Role.PATIENT,
                        )
                    except Role.DoesNotExist:
                        role = Role.objects.create(
                            user=user,
                            institution=institution,
                            role=Role.PATIENT,
                        )
                        role.save()
                patient_code = "PA-" + uuid.uuid4().hex[:6].upper()
                patient = Patient.objects.create(
                    institution=institution,
                    # user=user,
                    patient_code=patient_code,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    country=institution.country,
                    email=email,
                    gender=gender,
                    address=address,
                    phone_number=phone_number,
                )
                if user:
                    patient.user = user
                patient.save()
                messages.success(
                    request,
                    "Patient created successfully",
                )
            else:
                messages.error(
                    request,
                    "Patient not created, Please check each field!",
                )
                form = AddPatientForm()
        else:
            form = AddPatientForm()
            return render(
                request,
                "administration/patient.html",
                context={"form": form, "objects": patients},
            )
        form = AddPatientForm()
        return redirect(
            "administration:patient",
        )


# class UpdatePatient(LoginRequiredMixin, UpdateView):

#     model = Patient
#     template_name = "administration/edit_patient.html"
#     form_class = UpdatePatientForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         con = self.object.pk
#         context["pk"] = con
#         context["patient"] = Patient.objects.get(id=con)
#         return context
