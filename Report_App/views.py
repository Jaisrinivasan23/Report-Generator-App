from django.shortcuts import render, redirect, get_object_or_404
from .models import Department
from hods.models import Faculty
import uuid
from django.core.files.storage import FileSystemStorage
import pandas as pd

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

    departments = Department.objects.all()

    if request.method == "POST":
        # Check if a file was uploaded
        file_uploaded = 'file' in request.FILES
        form_filled = all(
            key in request.POST and request.POST[key]
            for key in ['name', 'hod_name', 'email']
        )

        if not file_uploaded and not form_filled:
            return render(request, 'add_department.html', {
                'departments': departments,
                'error': 'Please either fill out the form or upload a file.'
            })

        # Handle file upload
        if file_uploaded:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)
            file_full_path = fs.path(file_path)

            try:
                # Read uploaded file using pandas
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_full_path)
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_full_path)
                else:
                    return render(request, 'add_department.html', {
                        'departments': departments,
                        'error': 'Unsupported file format. Please upload CSV or Excel files.'
                    })

                # Validate data before insertion
                existing_emails = set(Department.objects.values_list('email', flat=True))
                new_departments = []

                for _, row in df.iterrows():
                    if 'name' not in row or 'hod_name' not in row or 'email' not in row:
                        return render(request, 'add_department.html', {
                            'departments': departments,
                            'error': 'Uploaded file is missing required columns: name, hod_name, email.'
                        })

                    email = row['email']

                    if email in existing_emails:
                        return render(request, 'add_department.html', {
                            'departments': departments,
                            'error': f"Duplicate email found: {email}."
                        })

                    # Prepare new department object
                    new_departments.append(Department(
                        name=row['name'],
                        hod_name=row['hod_name'],
                        email=email,
                        password=uuid.uuid4().hex[:8]
                    ))

                # Bulk create departments
                Department.objects.bulk_create(new_departments)
            except Exception as e:
                return render(request, 'add_department.html', {
                    'departments': departments,
                    'error': f'Error processing file: {str(e)}'
                })

            return redirect('add_department')

        # Handle form submission (Add manually)
        name = request.POST.get('name')
        hod_name = request.POST.get('hod_name')
        email = request.POST.get('email')

        # Check for duplicates in manual entry
        if Department.objects.filter(email=email).exists():
            return render(request, 'add_department.html', {
                'departments': departments,
                'error': f"Email already exists: {email}"
            })

        password = uuid.uuid4().hex[:8]
        Department.objects.create(name=name, hod_name=hod_name, email=email, password=password)
        return redirect('add_department')

    return render(request, 'add_department.html', {
        'departments': departments
    })

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
