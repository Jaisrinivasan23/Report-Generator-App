from django import forms
from .models import Event, ProductTemplate
from .models import UploadedTemplate
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__' # Exclude faculty field
class ProductTemplateForm(forms.ModelForm):
    class Meta:
        model = ProductTemplate
        fields = ['name', 'description', 'image']  # Include the image field

class UploadTemplateForm(forms.ModelForm):
    class Meta:
        model = UploadedTemplate
        fields = ['template_name', 'uploaded_file']
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

class UploadTemplateForm(forms.ModelForm):
    class Meta:
        model = UploadedTemplate
        fields = ['template_name', 'uploaded_file']