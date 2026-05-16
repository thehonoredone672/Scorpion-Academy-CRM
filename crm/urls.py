from django.urls import path
from . import views

urlpatterns = [
    # --- Frontend Pages ---
    path('', views.index_page, name='index'),
    path('dashboard', views.dashboard_page, name='dashboard'),
    path('leads', views.leads_page, name='leads'),
    path('students', views.students_page, name='students'),
    path('team', views.team_page, name='team'), # <--- The missing frontend route!

    # --- Core APIs ---
    path('api/login', views.login_api, name='api_login'),
    path('api/stats', views.stats_api, name='api_stats'),
    
    # --- Data APIs ---
    path('api/leads', views.leads_api, name='api_leads'),
    path('api/students', views.students_api, name='api_students'),
    path('api/staff', views.staff_api, name='api_staff'), # <--- The missing API route!

    # --- Targeted Detail APIs (Updates & Deletes) ---
    path('api/leads/<int:lead_id>', views.lead_detail_api, name='api_lead_detail'),
    path('api/students/<int:student_id>', views.student_detail_api, name='api_student_detail'),
    path('api/staff/<int:staff_id>', views.staff_detail_api, name='api_staff_detail'), # <--- The missing Detail API!
]
