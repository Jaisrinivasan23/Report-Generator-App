from django.shortcuts import render, redirect
from hods.models import Faculty
from PIL import Image
import piexif
from .forms import EventForm
from django.contrib import messages 

def faculty_dashboard(request):
    faculty_id = request.session.get('faculty_id')
    if not faculty_id:
        return redirect('common_login')  # Redirect to login if not authenticated

    faculty = Faculty.objects.get(id=faculty_id)
    return render(request, 'faculty_dashboard.html', {'faculty': faculty})

def is_gps_tagged_image(image_path):
    """Check if the uploaded image has GPS EXIF data."""
    try:
        # Open the image file using Pillow
        img = Image.open(image_path)
        
        # Extract EXIF data
        exif_data = piexif.load(img.info.get('exif', b''))
        
        # Check if GPS data is available
        if piexif.GPSIFD.GPSLatitude in exif_data['GPS'] and piexif.GPSIFD.GPSLongitude in exif_data['GPS']:
            return True  # GPS tag found
        return False
    except Exception as e:
        return False

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            gps_image = request.FILES.get('gps_image')
            normal_image = request.FILES.get('normal_image')
            
            # Check if the GPS image has the GPS tag
            if gps_image and is_gps_tagged_image(gps_image):
                event.gps_image = gps_image
            elif normal_image:
                event.normal_image = normal_image
            
            # Save the department and coordinator names
            event.faculty = request.user.faculty  # Assuming faculty is logged in and attached to the event
            event.department_name = event.faculty.department.name  # Automatically get department name
            event.faculty_coordinator_name = event.faculty.name  # Assuming the faculty coordinator is the faculty itself
            
            event.save()
            messages.success(request, "Event added successfully!")
            return redirect('faculty_dashboard')
    else:
        form = EventForm()

    return render(request, 'add_event.html', {'form': form})