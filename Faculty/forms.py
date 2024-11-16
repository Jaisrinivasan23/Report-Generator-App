from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'event_name', 'event_title', 'objective', 'event_date_time', 'venue',
            'gps_image', 'normal_image', 'department_name', 'faculty_coordinator_name',
            'no_of_students_attended', 'classes_attended', 'approval_letter', 'speaker_details'
        ]
