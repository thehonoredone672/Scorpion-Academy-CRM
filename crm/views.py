import json
import jwt
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from crm.models import Branch, Staff, Lead, Student, Invoice

# --- FRONTEND PAGE RENDERERS ---
def index_page(request):
    return render(request, 'index.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')

def leads_page(request):
    return render(request, 'leads.html')

def students_page(request):
    return render(request, 'students.html')

def team_page(request):
    return render(request, 'team.html')


# --- AUTHENTICATION API ---
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username_input = data.get('slug')
        password_input = data.get('password')

        # 1. Check if it's the Dojo Owner (Admin Master)
        branch = Branch.objects.filter(slug=username_input, password=password_input).first()
        if branch:
            payload = {
                'branch_id': branch.id,
                'role': 'Admin Master',
                'branch_name': branch.name,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            return JsonResponse({'token': token, 'branchName': branch.name, 'role': 'Admin Master'})

        # 2. Check if it's Staff (Master)
        staff = Staff.objects.filter(username=username_input, password=password_input).first()
        if staff:
            payload = {
                'branch_id': staff.branch.id,
                'staff_id': staff.id,
                'role': staff.role, 
                'branch_name': staff.branch.name,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            return JsonResponse({'token': token, 'branchName': staff.branch.name, 'role': staff.role})

        return JsonResponse({'error': 'Invalid Credentials'}, status=400)


# --- HELPER FUNCTION: TOKEN VALIDATION ---
def get_user_from_token(request):
    token = request.headers.get('Authorization')
    if not token: return None
    try:
        return jwt.decode(token, 'secret_key', algorithms=['HS256'])
    except:
        return None


# --- STATS API ---
@csrf_exempt
def stats_api(request):
    user = get_user_from_token(request)
    if not user: return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    b_id = user.get('branch_id')
    total_students = Student.objects.filter(branch_id=b_id).count()
    active_leads = Lead.objects.filter(branch_id=b_id).exclude(status='Follow Up').count()
    
    return JsonResponse({'totalStudents': total_students, 'activeLeads': active_leads})


# --- LEADS API ---
@csrf_exempt
def leads_api(request):
    user = get_user_from_token(request)
    if not user: return JsonResponse({'error': 'Unauthorized'}, status=401)
    b_id = user.get('branch_id')

    if request.method == 'GET':
        leads = Lead.objects.filter(branch_id=b_id)
        data = [{'id': l.id, 'name': l.name, 'phone': l.phone, 'program': l.program, 'status': l.status} for l in leads]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        Lead.objects.create(branch_id=b_id, name=data.get('name'), phone=data.get('phone'), program=data.get('program'))
        return JsonResponse({'message': 'Lead created'})

@csrf_exempt
def lead_detail_api(request, lead_id):
    user = get_user_from_token(request)
    if not user: return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        lead = Lead.objects.get(id=lead_id)
        if lead.branch_id != user.get('branch_id'):
            return JsonResponse({'error': 'Forbidden'}, status=403)
            
        if request.method == 'PUT':
            data = json.loads(request.body)
            lead.status = data.get('status', lead.status)
            lead.save()
            return JsonResponse({'message': 'Lead updated'})
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'Lead not found'}, status=404)


# --- STUDENTS API ---
@csrf_exempt
def students_api(request):
    user = get_user_from_token(request)
    if not user: return JsonResponse({'error': 'Unauthorized'}, status=401)
    b_id = user.get('branch_id')

    if request.method == 'GET':
        students = Student.objects.filter(branch_id=b_id)
        data = [{'id': s.id, 'name': s.name, 'beltRank': s.beltRank, 'phone': s.phone} for s in students]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        Student.objects.create(branch_id=b_id, name=data.get('name'), beltRank=data.get('beltRank'), phone=data.get('phone'))
        return JsonResponse({'message': 'Student created'})

@csrf_exempt
def student_detail_api(request, student_id):
    user = get_user_from_token(request)
    if not user: return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        student = Student.objects.get(id=student_id)
        if student.branch_id != user.get('branch_id'):
            return JsonResponse({'error': 'Forbidden'}, status=403)
            
        if request.method == 'PUT':
            data = json.loads(request.body)
            student.name = data.get('name', student.name)
            student.beltRank = data.get('beltRank', student.beltRank)
            student.phone = data.get('phone', student.phone)
            student.save()
            return JsonResponse({'message': 'Student updated'})

        elif request.method == 'DELETE':
            student.delete()
            return JsonResponse({'message': 'Student deleted'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


# --- STAFF/TEAM API (ADMIN MASTER ONLY) ---
@csrf_exempt
def staff_api(request):
    user = get_user_from_token(request)
    if not user: return JsonResponse({'error': 'Unauthorized'}, status=401)
    if user.get('role') != 'Admin Master':
        return JsonResponse({'error': 'Forbidden: Admin Master only'}, status=403)
        
    b_id = user.get('branch_id')

    if request.method == 'GET':
        staff = Staff.objects.filter(branch_id=b_id)
        data = [{'id': s.id, 'name': s.name, 'username': s.username, 'role': s.role} for s in staff]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        if Staff.objects.filter(username=data.get('username')).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
            
        Staff.objects.create(
            branch_id=b_id,
            name=data.get('name'),
            username=data.get('username'),
            password=data.get('password'),
            role=data.get('role', 'Master')
        )
        return JsonResponse({'message': 'Staff created'})

@csrf_exempt
def staff_detail_api(request, staff_id):
    user = get_user_from_token(request)
    if not user: return JsonResponse({'error': 'Unauthorized'}, status=401)
    if user.get('role') != 'Admin Master':
        return JsonResponse({'error': 'Forbidden: Admin Master only'}, status=403)

    try:
        staff = Staff.objects.get(id=staff_id)
        if staff.branch_id != user.get('branch_id'):
            return JsonResponse({'error': 'Forbidden'}, status=403)
            
        if request.method == 'DELETE':
            staff.delete()
            return JsonResponse({'message': 'Staff deleted'})
    except Staff.DoesNotExist:
        return JsonResponse({'error': 'Staff not found'}, status=404)
