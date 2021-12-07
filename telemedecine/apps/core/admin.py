from django.contrib import admin
from .models.hospital_models import *
from .models.administration import *

# Register your models here.
admin.site.register(Institution)
admin.site.register(Speciality)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Pharmacist)
admin.site.register(LabSpecialist)
admin.site.register(Role)

admin.site.site_header = "Telemedecine Administration"
