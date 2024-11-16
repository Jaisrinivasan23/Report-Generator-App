from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('common_login')),
     path('login/', views.common_login, name='common_login'),
    path('admin-dashboard/', views.dashboard, name='admin_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-department/', views.add_department, name='add_department'),
    path('delete-department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('view-departments/', views.view_department, name='view_departments'),
    path('department/<int:department_id>/', views.department_detail, name='department_detail'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
