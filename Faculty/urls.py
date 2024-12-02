from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('add_event/', views.add_event, name='add_event'),
    path('event-report/<int:event_id>/', views.event_report, name='event_report'),
    path('event/', views.get, name='event'),
    path('view/', views.view, name='view'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
