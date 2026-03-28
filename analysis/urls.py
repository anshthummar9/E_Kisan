from django.urls import path
from accounts.views import dashboard_view
from . import views

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard_alt'),
    path('analysis/', views.analysis_view, name='analysis'),
    path('report/<int:report_id>/', views.report_detail_view, name='report_detail'),
    path('report/<int:report_id>/edit/', views.edit_report_view, name='edit_report'),
]
