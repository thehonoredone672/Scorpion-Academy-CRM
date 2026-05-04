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


# Add this to the bottom of crm/views.py
from django.views.decorators.http import require_http_methods

@csrf_exempt
def lead_detail_api(request, lead_id):
    # This checks the token to make sure the user is logged in
    token = request.headers.get('Authorization')
    if not token: return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        lead = Lead.objects.get(id=lead_id)
        
        # Handle the PUT request to update the status
        if request.method == 'PUT':
            data = json.loads(request.body)
            lead.status = data.get('status', lead.status)
            lead.save()
            return JsonResponse({'message': 'Lead updated successfully'})
            
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'Lead not found'}, status=404)

@csrf_exempt
def student_detail_api(request, student_id):
    token = request.headers.get('Authorization')
    if not token: return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        student = Student.objects.get(id=student_id)
        
        # Handle the DELETE request to remove a student
        if request.method == 'DELETE':
            student.delete()
            return JsonResponse({'message': 'Student deleted successfully'})
            
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
