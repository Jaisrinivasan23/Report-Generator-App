from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.dashboard, name='faculty_dashboard'),
    path('add_event/', views.add_event, name='add_event'),
    path('event-report/<int:event_id>/', views.event_report, name='event_report'),
    path('event/', views.get, name='event'),
    path('view/', views.view, name='view'),
    path('view_event/', views.events, name='view_events'),
    path('report-editor/', views.report_editor, name='report_editor'),
    path('add_field/', views.add_field, name='add_field'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
