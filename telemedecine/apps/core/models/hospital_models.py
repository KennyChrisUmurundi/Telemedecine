from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.postgres.fields import JSONField
from telemedecine.apps.authentication.models import CustomUser
from django.urls import reverse

# from .administration import PaymentOption

# from telemedecine.apps.core.models.administration import PaymentOption


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
    consultation_fee = models.DecimalField(
        default="0.0", null=True, decimal_places=2, max_digits=8
    )

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
    speciality = models.CharField(max_length=200, blank=True, null=True)
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


class Patient(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    patient_code = models.CharField(
        max_length=200, unique=True, null=True, blank=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = CountryField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)


class PatientMedicalInfo(models.Model):
    pass


class Appointment(models.Model):

    PENDING = "P"
    FOLLOW_UP = "C"
    DONE = "D"
    # EXPIRED = "E"

    STATUS = (
        (PENDING, _("Pending")),
        (FOLLOW_UP, _("Follow Up")),
        (DONE, _("Done")),
    )
    institution = models.ForeignKey(
        Institution, on_delete=models.DO_NOTHING, null=True
    )
    appointment_date = models.DateTimeField(null=True)
    appointment_code = models.CharField(max_length=30, null=True)
    department = models.ForeignKey(
        Speciality, on_delete=models.DO_NOTHING, null=True
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    appointment_status = models.CharField(
        choices=STATUS, max_length=1, default=PENDING, null=True
    )
    payment_option = models.ForeignKey(
        "core.PaymentOption", on_delete=models.DO_NOTHING, null=True
    )
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.appointment_code + "" + self.patient.first_name


class AvailableTest(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    test_name = models.CharField(max_length=200)
    test_code = models.CharField(max_length=200)
    test_fee = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.test_code


class LabTest(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    date_taken = models.DateTimeField()
    test_name = models.ForeignKey(AvailableTest, on_delete=models.DO_NOTHING)
    patient = models.ForeignKey("core.Patient", on_delete=models.DO_NOTHING)
    payment_option = models.ForeignKey(
        "core.PaymentOption", on_delete=models.DO_NOTHING
    )
    test_done = models.BooleanField(default=False)
    test_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.test.test_name


# class PatientMedicalHistory(models.Model):
#     appointment = models.ForeignKey(
#         Appointment, on_delete=models.DO_NOTHING, null=True
#     )
