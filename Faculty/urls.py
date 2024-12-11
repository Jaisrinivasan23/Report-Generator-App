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
<<<<<<< HEAD
    path('Faculty_Events/', views.View_all_events, name='view_events'),
    path('submit-for-approval/<int:event_id>/', views.submit_for_approval, name='submit_for_approval'),
    path('View-Report/<int:ReportID>',views.View_Report,name='View_Report')

=======
    path('view_event/', views.events, name='view_events'),
    path('report-editor/', views.report_editor, name='report_editor'),
    path('add_field/', views.add_field, name='add_field'),
>>>>>>> 60bc854ee3376eac3ed6e9be840041feae58d7f8
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
