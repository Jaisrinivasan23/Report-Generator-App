from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, UploadedTemplate
from .forms import EventForm, UploadTemplateForm
from bs4 import BeautifulSoup

def dashboard(request):
    return render(request, 'view.html')

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully!")
            return redirect('view_events')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

def view_events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def event_report(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_report.html', {'event': event})

def upload_template(request):
    if request.method == 'POST':
        form = UploadTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_template = form.save(commit=False)
            html_content = request.FILES['uploaded_file'].read().decode('utf-8')
            soup = BeautifulSoup(html_content, 'html.parser')

            form_fields = {}
            for input_tag in soup.find_all(['input', 'textarea']):
                field_name = input_tag.get('name', f'field_{len(form_fields) + 1}')
                field_type = input_tag.get('type', 'text')
                form_fields[field_name] = {'type': field_type}

            uploaded_template.generated_form = form_fields
            uploaded_template.save()
            return redirect('fill_template', pk=uploaded_template.pk)
    else:
        form = UploadTemplateForm()
    return render(request, 'upload_template.html', {'form': form})

def fill_template(request, pk):
    template = get_object_or_404(UploadedTemplate, pk=pk)
    form_data = template.generated_form
    if request.method == 'POST':
        filled_data = {field: request.POST.get(field, '') for field in form_data.keys()}
        template.filled_data = filled_data
        template.save()
        messages.success(request, "Template updated successfully!")
        return redirect('dashboard')
    return render(request, 'fill_template.html', {'template': template})

def report_editor(request):
    return render(request, 'report_editor.html')

def update_template(request):
    return render(request, 'update_template.html')
