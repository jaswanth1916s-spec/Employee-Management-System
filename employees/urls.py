from django.urls import path
from . import views

urlpatterns = [
    # Dashboard (Homepage when logged in)
    path('', views.dashboard_view, name='dashboard'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Employee Management
    path('employees/', views.employee_list_view, name='employee_list'),
    path('employees/search/', views.employee_search_view, name='employee_search'),
    path('employees/add/', views.employee_create_view, name='employee_add'),
    path('employees/<int:pk>/', views.employee_detail_view, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_update_view, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete_view, name='employee_delete'),
    
    # Admin Profile
    path('profile/', views.admin_profile_view, name='admin_profile'),
]
