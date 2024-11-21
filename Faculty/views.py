from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from hods.models import Faculty
from PIL import Image
import piexif
from .models import Event 
from django.contrib.auth.decorators import login_required

def faculty_dashboard(request):
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
