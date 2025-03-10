from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.medical_history, name='history'),
    path('add/patient/', views.register_patient, name='register'),
    path('analytics', views.AnalyticsView.as_view(), name='analytics'),
    path('filters', views.filter, name='filter'),
    path('treatment/<int:pk>/', views.Medication, name='patient-medicals'),
    path('reports/', views.RevenueByPaymentTypeView.as_view(), name='reports'),
    path('filtered/', views.FilteredMedicalHistoryView.as_view(), name='filtered'),
    path('export/csv/', views.ExportFilteredMedicalHistoryView.as_view(), name='export_csv'),
    path('export/pdf/', views.ExportFilteredMedicalHistoryPDFView.as_view(), name='export_pdf'),
    path('upcoming-follow-up/', views.UpcomingFollowUpView.as_view(), name='upcoming_follow_up'),
    path('analytics/doctors/', views.AnalyticsByDoctorView.as_view(), name='analytics_by_doctor'),
    path('medical/reports/', views.MedicalHistoryReportView.as_view(), name='medical_reports'),
    path('patient/update/<int:pk>/', views.update_patient, name='update_patient'),
    path('patient/delete/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('generate_invoice/<int:history_id>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('medical-history/update/<int:pk>/', views.update_medical_history, name='update_medical_history'),
    path('medical-history/delete/<int:pk>/', views.delete_medical_history, name='delete_medical_history'),
    path('patient/<int:pk>/', views.patient_detail, name='patient-detail'),
]
