# crm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Frontend Routes
    path('', views.index_page, name='index'),
    path('dashboard', views.dashboard_page, name='dashboard'),
    path('leads', views.leads_page, name='leads'),
    path('students', views.students_page, name='students'),
    
    # General API Routes
    path('api/login', views.login_api, name='api_login'),
    path('api/leads', views.leads_api, name='api_leads'),
    path('api/students', views.students_api, name='api_students'),
    path('api/stats', views.stats_api, name='api_stats'),

    # NEW: Targeted API Routes for Updating and Deleting
    path('api/leads/<int:lead_id>', views.lead_detail_api, name='api_lead_detail'),
    path('api/students/<int:student_id>', views.student_detail_api, name='api_student_detail'),
]
