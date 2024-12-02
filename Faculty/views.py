from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from hods.models import Faculty
from bs4 import BeautifulSoup 
from PIL import Image
import piexif
from .models import Event , UploadedTemplate
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .forms import ProductTemplateForm, UploadTemplateForm
def dashboard(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('common_login')  # Redirect to login if not authenticated

    faculty = Faculty.objects.get(id=faculty_id)
    return render(request, 'faculty_dashboard.html', {'faculty': faculty})


def is_gps_tagged_image(image_path):
    """Check if the uploaded image has GPS EXIF data."""
    try:
        img = Image.open(image_path)
        exif_data = piexif.load(img.info.get('exif', b''))
        if piexif.GPSIFD.GPSLatitude in exif_data['GPS'] and piexif.GPSIFD.GPSLongitude in exif_data['GPS']:
            return True
        return False
    except Exception:
        return False


def add_event(request):
    # Fetch the faculty's details based on the session or logged-in context
    faculty_id = request.session.get('faculty_id')
    faculty = Faculty.objects.get(id=faculty_id)
    department = faculty.department
    print(faculty)
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_title = request.POST.get('event_title')
        objective = request.POST.get('objective')
        event_date_time = request.POST.get('event_date_time')
        venue = request.POST.get('venue')
        gps_image = request.FILES.get('gps_image')
        normal_image = request.FILES.get('normal_image')
        no_of_students_attended = request.POST.get('no_of_students_attended')
        classes_attended = request.POST.get('classes_attended')
        approval_letter = request.FILES.get('approval_letter')
        speaker_details = request.POST.get('speaker_details')

        # Save the event
        event = Event(
            faculty= faculty, # Assuming 'name' is the field in Faculty model
            event_name=event_name,
            event_title=event_title,
            objective=objective,
            event_date_time=event_date_time,
            venue=venue,
            gps_image=gps_image,
            normal_image=normal_image,
            department_name=department,  # Use department from the logged-in faculty
            faculty_coordinator_name=faculty,
            no_of_students_attended=no_of_students_attended,
            classes_attended=classes_attended,
            approval_letter=approval_letter,
            speaker_details=speaker_details
        )
        event.save()

        messages.success(request, "Event added successfully!")
        return redirect('event_report', event_id=event.id)  # Redirect to the event report page

    return render(request, 'add_event.html')  # Render the form if the request is GET

def event_report(request, event_id):
    """Display the details of the submitted event."""
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_report.html', {'event': event})

def get(request):
    event = EventForm()
    if request.method == 'POST':
        event = EventForm(request.POST)
        if event.is_valid():
            event.save()
            print(event)
            return redirect('event_report')
        else:
            return render(request, 'forms.html', {'event': event})
    return render(request, 'forms.html', {'event': event})
def view(request):
    return render(request,'view.html')
def events(request):
    var=Event.objects.all()
    return render(request,'events.html',{'var':var})
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def report_editor(request):
    # Here you can create the default template or fetch the existing template from the database
    return render(request, 'report_editor.html')

@csrf_exempt
def add_field(request):
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        # Save extra field logic here
        return JsonResponse({"success": True, "field_name": field_name})
def update_template(request):
    success_message = None  # Initialize the success message variable

    if request.method == 'POST':
        form = ProductTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            success_message = "Template added successfully!"  # Set success message
            form = ProductTemplateForm()  # Reset the form after successful submission
    else:
        form = ProductTemplateForm()

    # Pass the form and success message to the template
    return render(request, 'update_template.html', {'form': form, 'success_message': success_message})
