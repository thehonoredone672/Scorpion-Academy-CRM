# crm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Clean URLs for Frontend
    path('', views.index_page, name='index'),
    path('dashboard', views.dashboard_page, name='dashboard'),
    path('leads', views.leads_page, name='leads'),
    path('students', views.students_page, name='students'),
    
    # API Routes
    path('api/login', views.login_api, name='api_login'),
    path('api/leads', views.leads_api, name='api_leads'),
    path('api/students', views.students_api, name='api_students'),
    path('api/stats', views.stats_api, name='api_stats'),
]