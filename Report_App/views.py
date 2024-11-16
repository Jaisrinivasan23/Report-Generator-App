from django.shortcuts import render, redirect, get_object_or_404
from .models import Department
from hods.models import Faculty
import uuid

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

def common_login(request):
    if request.method == "POST":
        role = request.POST['role']
        username = request.POST['username']
        password = request.POST['password']

        # Handle Admin Login
        if role == "Admin" and username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')

        # Handle HOD Login
        elif role == "HOD":
            try:
                hod = Department.objects.get(email=username, password=password)
                request.session['hod_id'] = hod.id
                return redirect('hod_dashboard')
            except Department.DoesNotExist:
                return render(request, 'common_login.html', {'error': 'Invalid HOD credentials'})

        # Handle Faculty Login
        elif role == "Faculty":
            try:
                faculty = Faculty.objects.get(email=username, password=password)
                request.session['faculty_id'] = faculty.id
                return redirect('faculty_dashboard')  # Redirect to Faculty Dashboard
            except Faculty.DoesNotExist:
                return render(request, 'common_login.html', {'error': 'Invalid Faculty credentials'})

        # Invalid credentials
        return render(request, 'common_login.html', {'error': 'Invalid credentials'})

    return render(request, 'common_login.html')


def dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('common_login')
    return render(request, 'dashboard.html')

def add_department(request):
    if not request.session.get('admin_logged_in'):
        return redirect('common_login')

    # Initialize variables for the form
    department_id = request.POST.get('department_id')
    department = None

    # Handle form submission (Add or Edit)
    if request.method == "POST":
        name = request.POST['name']
        hod_name = request.POST['hod_name']
        email = request.POST['email']

        if department_id:  # Edit existing department
            department = get_object_or_404(Department, id=department_id)
            department.name = name
            department.hod_name = hod_name
            department.email = email
            department.save()
        else:  # Add new department
            password = uuid.uuid4().hex[:8]
            Department.objects.create(name=name, hod_name=hod_name, email=email, password=password)

        return redirect('add_department')

    # Get department for editing (if department_id is in GET params)
    if 'edit' in request.GET:
        department_id = request.GET['edit']
        department = get_object_or_404(Department, id=department_id)

    departments = Department.objects.all()
    return render(request, 'add_department.html', {'departments': departments, 'edit_department': department})

def delete_department(request, department_id):
    if not request.session.get('admin_logged_in'):
        return redirect('common_login')

    department = get_object_or_404(Department, id=department_id)
    department.delete()
    return redirect('add_department')

def admin_logout(request):
    request.session.flush()
    return redirect('common_login')

def view_department(request):
    departments = Department.objects.all()
    return render(request, 'department_details.html', {'departments': departments})

def department_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    return render(request, 'department_detail.html', {'department': department})
