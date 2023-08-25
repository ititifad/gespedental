from django.contrib import admin

from .models import *

admin.site.register(Patient)
admin.site.register(MedicalHistory)
admin.site.register(Treatment)
admin.site.register(PaymentType)