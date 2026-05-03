import json
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Branch, Lead, Student
from .serializers import LeadSerializer, StudentSerializer
from .auth import authenticate_jwt

# --- HTML TEMPLATE RENDERING ---
def index_page(request): return render(request, 'index.html')
def dashboard_page(request): return render(request, 'dashboard.html')
def leads_page(request): return render(request, 'leads.html')
def students_page(request): return render(request, 'students.html')

# --- API ENDPOINTS ---
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            branch = Branch.objects.get(slug=data.get('slug'), password=data.get('password'))
            token = jwt.encode({'branchId': branch.id}, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token, 'branchName': branch.name})
        except Branch.DoesNotExist:
            return JsonResponse({'error': 'Invalid Credentials'}, status=400)

@csrf_exempt
@authenticate_jwt
def leads_api(request):
    if request.method == 'GET':
        leads = Lead.objects.filter(branch_id=request.branch_id).order_by('-created_at')
        serializer = LeadSerializer(leads, many=True)
        return JsonResponse(serializer.data, safe=False)
        
    elif request.method == 'POST':
        data = json.loads(request.body)
        Lead.objects.create(
            branch_id=request.branch_id,
            name=data.get('name'), 
            phone=data.get('phone'), 
            program=data.get('program')
        )
        return JsonResponse({'message': 'Enquiry saved!'}, status=201)

@csrf_exempt
@authenticate_jwt
def students_api(request):
    if request.method == 'GET':
        students = Student.objects.filter(branch_id=request.branch_id).order_by('name')
        serializer = StudentSerializer(students, many=True)
        return JsonResponse(serializer.data, safe=False)
        
    elif request.method == 'POST':
        data = json.loads(request.body)
        Student.objects.create(
            branch_id=request.branch_id,
            name=data.get('name'), 
            beltRank=data.get('beltRank'), 
            phone=data.get('phone')
        )
        return JsonResponse({'message': 'Student registered!'}, status=201)

@authenticate_jwt
def stats_api(request):
    total_students = Student.objects.filter(branch_id=request.branch_id).count()
    active_leads = Lead.objects.filter(branch_id=request.branch_id, status='New').count()
    return JsonResponse({
        'totalStudents': total_students,
        'activeLeads': active_leads,
        'pendingFees': 0 
    })