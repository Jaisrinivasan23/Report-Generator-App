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
class ProductTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Image field

    def __str__(self):
        return self.name
class ReportTemplate(models.Model):
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    college_name = models.CharField(max_length=255, default="Your College Name")
    faculty = models.ForeignKey('hods.Faculty', on_delete=models.CASCADE)  # Reference to Faculty model
    event_name = models.CharField(max_length=255, null=True, blank=True)
    event_title = models.CharField(max_length=255, null=True, blank=True)
    objective = models.TextField(null=True, blank=True)
    event_date_time = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    gps_image = models.ImageField(upload_to='gps_images/', null=True, blank=True)
    normal_image = models.ImageField(upload_to='normal_images/', null=True, blank=True)
    department_name = models.CharField(max_length=255, null=True, blank=True)
    faculty_coordinator_name = models.CharField(max_length=255, null=True, blank=True)
    no_of_students_attended = models.IntegerField(null=True, blank=True)
    classes_attended = models.CharField(max_length=255, null=True, blank=True)
    approval_letter = models.FileField(upload_to='approval_letters/', null=True, blank=True)
    speaker_details = models.TextField(null=True, blank=True)
    extra_fields = models.JSONField(default=dict)  # To store user-added fields
class UploadedTemplate(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Template owner
    template_name = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='uploaded_templates/')
    generated_form = models.JSONField(default=dict)  # Store generated form fields
    filled_data = models.JSONField(default=dict, blank=True)  # Store form data filled by the user

    def __str__(self):
        return self.template_name