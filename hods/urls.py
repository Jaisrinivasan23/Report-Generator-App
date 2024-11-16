from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('add-faculty/', views.add_faculty, name='add_faculty'),
    path('view-faculties/', views.view_faculties, name='view_faculties'),
]