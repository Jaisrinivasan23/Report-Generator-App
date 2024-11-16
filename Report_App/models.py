from django.db import models
import uuid

class Department(models.Model):
    name = models.CharField(max_length=255)
    hod_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default=uuid.uuid4)
    
    def __str__(self):
        return self.name

