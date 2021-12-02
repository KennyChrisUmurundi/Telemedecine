from django.contrib import admin
from .models.hospital_models import *

# Register your models here.
admin.site.register(Institution)
admin.site.register(Speciality)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Pharmacist)
admin.site.register(LabSpecialist)

admin.site.site_header = "Telemedecine Administration"
