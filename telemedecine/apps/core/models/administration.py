from django.db import models
from telemedecine.apps.authentication.models import CustomUser
from telemedecine.apps.core.models import Institution
from django.utils.translation import gettext_lazy as _


class Role(models.Model):

    ADMIN = "A"
    DOCTOR = "D"
    PHARMACIST = "P"
    NURSE = "N"
    RECEPTIONIST = "R"
    PATIENT = "C"
    DEFAULT = "Z"

    ROLES = (
        (ADMIN, _("Admin")),
        (DOCTOR, _("Doctor")),
        (PHARMACIST, _("Pharmacist")),
        (NURSE, _("Nurse")),
        (RECEPTIONIST, _("Receptionist")),
        (PATIENT, _("Patient")),
    )

    user = models.OneToOneField(
        CustomUser, on_delete=models.DO_NOTHING, related_name="user_role"
    )
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=1, choices=ROLES, default=DEFAULT)

    def __str__(self):
        return self.role
