from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/patient/', views.register_patient, name='register'),
    path('analytics', views.AnalyticsView.as_view(), name='analytics'),
    path('filters', views.filter, name='filter'),
    path('patient/<int:pk>/treatment', views.Medication, name='patient-medicals'),
    path('reports/', views.RevenueByPaymentTypeView.as_view(), name='reports'),
    path('patient/<int:pk>/', views.patient_detail, name='patient-detail'),
    path('filtered/', views.FilteredMedicalHistoryView.as_view(), name='filtered'),
    path('export/csv/', views.ExportFilteredMedicalHistoryView.as_view(), name='export_csv'),
    path('export/pdf/', views.ExportFilteredMedicalHistoryPDFView.as_view(), name='export_pdf'),
]
