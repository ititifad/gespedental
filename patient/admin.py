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