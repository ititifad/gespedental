from django.contrib import admin

from .models import *

admin.site.register(Patient)
admin.site.register(MedicalHistory)
admin.site.register(Treatment)
admin.site.register(ReviewofSystem)
admin.site.register(Examination)
admin.site.register(Diagnosis)
admin.site.register(Investgation)
admin.site.register(Medication)
admin.site.register(PaymentType)
admin.site.register(Doctor)

admin.site.site_header = "GEITA SPECIALIZED DENTAL CLINIC"
admin.site.site_title = "GEITA SPECIALIZED DENTAL CLINIC Admin Portal"
admin.site.index_title = "Welcome to GEITA SPECIALIZED DENTAL CLINIC EPR System"