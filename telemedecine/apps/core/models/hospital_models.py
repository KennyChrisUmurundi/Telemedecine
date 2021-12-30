from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.postgres.fields import JSONField
from telemedecine.apps.authentication.models import CustomUser
from django.urls import reverse


MALE = "M"
FEMALE = "F"
GENDER_CHOICES = ((MALE, _("Male")), (FEMALE, _("Female")))


class Institution(models.Model):
    institution_name = models.CharField(max_length=200)
    country = CountryField()
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    licence = models.FileField(
        upload_to="media/licenses", blank=True, null=True
    )
    default_admin = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, null=True
    )
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.institution_name

    def get_absolute_url(self):
        return reverse("administration:providers")


class Speciality(models.Model):
    speciality = models.CharField(max_length=200)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.speciality


class Doctor(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = CountryField()
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    speciality = models.ForeignKey(
        Speciality, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    publication = models.JSONField(blank=True, null=True)
    licence_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.first_name + "" + self.last_name


class Nurse(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = CountryField()
    email = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # publication = models.JSONField(blank=True, null=True)
    # licence_number = models.CharField(max_length=200, blank=True, null=True)
    is_practitioner = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + "" + self.last_name


class Pharmacist(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = CountryField()
    email = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # publication = models.JSONField(blank=True, null=True)
    licence_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.first_name + "" + self.last_name


class LabSpecialist(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="sys_user",
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = CountryField()
    email = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # publication = models.JSONField(blank=True, null=True)
    licence_number = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.first_name + "" + self.last_name


class Receptionist(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = CountryField()
    email = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
