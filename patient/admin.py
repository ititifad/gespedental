from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Patient, MedicalHistory, Treatment, ReviewofSystem,
    Examination, Diagnosis, Investgation, Medication,
    PaymentType, Doctor
)

# Enable Import/Export for Patient
@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for MedicalHistory
@admin.register(MedicalHistory)
class MedicalHistoryAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for Treatment
@admin.register(Treatment)
class TreatmentAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for ReviewofSystem
@admin.register(ReviewofSystem)
class ReviewofSystemAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for Examination
@admin.register(Examination)
class ExaminationAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for Diagnosis
@admin.register(Diagnosis)
class DiagnosisAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for Investgation
@admin.register(Investgation)
class InvestgationAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for Medication
@admin.register(Medication)
class MedicationAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for PaymentType
@admin.register(PaymentType)
class PaymentTypeAdmin(ImportExportModelAdmin):
    pass

# Enable Import/Export for Doctor
@admin.register(Doctor)
class DoctorAdmin(ImportExportModelAdmin):
    pass

admin.site.site_header = "GEITA SPECIALIZED DENTAL CLINIC"
admin.site.site_title = "GEITA SPECIALIZED DENTAL CLINIC Admin Portal"
admin.site.index_title = "Welcome to GEITA SPECIALIZED DENTAL CLINIC EPR System"