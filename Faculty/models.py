from django.db import models

class Event(models.Model):
    faculty = models.ForeignKey('hods.Faculty', on_delete=models.CASCADE)  # Correct reference
    event_name = models.CharField(max_length=255)
    event_title = models.CharField(max_length=255)
    objective = models.TextField()
    event_date_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    gps_image = models.ImageField(upload_to='gps_images/', null=True, blank=True)
    normal_image = models.ImageField(upload_to='normal_images/', null=True, blank=True)
    department_name = models.CharField(max_length=255)
    faculty_coordinator_name = models.CharField(max_length=255)
    no_of_students_attended = models.IntegerField()
    classes_attended = models.CharField(max_length=255)
    approval_letter = models.FileField(upload_to='approval_letters/')
    speaker_details = models.TextField()

    def __str__(self):
        return self.event_name