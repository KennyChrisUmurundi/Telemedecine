from django.db import models
from telemedecine.apps.authentication.models import CustomUser

# from .hospital_models import Institution
from django.utils.translation import gettext_lazy as _


class Role(models.Model):

    ADMIN = "A"
    DOCTOR = "D"
    PHARMACIST = "P"
    NURSE = "N"
    RECEPTIONIST = "R"
    PATIENT = "C"
    LAB_SPECIALIST = "L"
    DEFAULT = "Z"

    ROLES = (
        (ADMIN, _("Admin")),
        (DOCTOR, _("Doctor")),
        (PHARMACIST, _("Pharmacist")),
        (NURSE, _("Nurse")),
        (RECEPTIONIST, _("Receptionist")),
        (PATIENT, _("Patient")),
        (LAB_SPECIALIST, _("Lab Specialist")),
    )

    user = models.OneToOneField(
        CustomUser, on_delete=models.DO_NOTHING, related_name="user_role"
    )
    institution = models.ForeignKey(
        "core.Institution", on_delete=models.DO_NOTHING
    )
    role = models.CharField(max_length=1, choices=ROLES, default=DEFAULT)

    def __str__(self):
        return self.role


class PaymentOption(models.Model):
    payment_option = models.CharField(max_length=200)
    payment_code = models.CharField(max_length=200, unique=True)
    percentage_off_payment = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_code
