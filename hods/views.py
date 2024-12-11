from django.shortcuts import render, redirect, get_object_or_404
from Report_App.models import Department
from .models import Faculty
import uuid
from django.contrib import messages
from Faculty.models import Event 

def hod_dashboard(request):
    hod_id = request.session.get('hod_id')
    if not hod_id:
        return redirect('common_login')  # Redirect to login if not authenticated

    hod = Department.objects.get(id=hod_id)
    return render(request, 'hod_dashboard.html', {'hod': hod})

def add_faculty(request):
    hod_id = request.session.get('hod_id')  # Get the HOD ID from session
    if not hod_id:
        return redirect('common_login')  # Redirect to login if not authenticated

    department = Department.objects.get(id=hod_id)  # Get the department of the logged-in HOD

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        role = request.POST['role']
        password = uuid.uuid4().hex[:8]  # Random password for Faculty
        
        # Create Faculty and associate with the logged-in HOD's department
        faculty = Faculty.objects.create(
            name=name, 
            email=email, 
            password=password, 
            department=department,
            role=role
        )
        messages.success(request, 'Faculty added successfully!')
        return redirect('add_faculty')  # Redirect to Add Faculty page after saving

    return render(request, 'add_faculty.html')

def view_faculties(request):
    faculties = Faculty.objects.all()
    return render(request, 'view_faculties.html', {'faculties': faculties})

def Department_Events(request):
    id = request.session.get('hod_id')
    department = Department.objects.filter(id=id).first()
    events = Event.objects.filter(department_name=department.name)
    return render(request, 'Department_Events.html', {'events': events})

def Dept_Details(request,event_details):
    events = Event.objects.filter(event_title=event_details)
    print(events)
    return render(request,'Dept_event_Details.html',{'event':events})

def View_Report_HOD(request, ReportID):
    # Get the event object
    event = get_object_or_404(Event, id=ReportID)

    if request.method == 'POST':
        # Get data from the form
        remarks = request.POST.get('remarks', '').strip()
        status = request.POST.get('status', 'Pending')

        # Update the event object
        event.remarks = remarks
        event.status = status
        event.save()

        # Redirect back to the same page or to another page
        return redirect('View_Report_HOD', ReportID=ReportID)

    return render(request, 'view_report.html', {'event': event})