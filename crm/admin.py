from django.contrib import admin
from .models import Branch, Lead, Student

# Registering models so they appear in the Django Admin Dashboard (http://localhost:3000/admin)
admin.site.register(Branch)
admin.site.register(Lead)
admin.site.register(Student)