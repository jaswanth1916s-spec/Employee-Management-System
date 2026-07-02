from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import Employee
from .forms import EmployeeForm, AdminProfileForm

# --- Authentication Views ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# --- Dashboard View ---

@login_required
def dashboard_view(request):
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='Active').count()
    inactive_employees = Employee.objects.filter(status='Inactive').count()
    recent_employees = Employee.objects.all().order_by('-created_at')[:5]
    
    # Get counts by department for dashboard metrics
    departments = Employee.objects.values('department').distinct().count()

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'recent_employees': recent_employees,
        'departments_count': departments,
    }
    return render(request, 'dashboard.html', context)


# --- Employee CRUD Views ---

@login_required
def employee_list_view(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', '-created_at')
    
    # Restrict sorting columns for security
    allowed_sort_fields = ['employee_id', 'full_name', 'department', 'designation', 'phone', 'status', '-created_at']
    if sort_by not in allowed_sort_fields:
        sort_by = '-created_at'

    employees = Employee.objects.all()

    # Apply search filter
    if query:
        employees = employees.filter(
            Q(full_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(department__icontains=query) |
            Q(designation__icontains=query)
        )

    # Apply sorting
    employees = employees.order_by(sort_by)

    # Pagination: 10 employees per page
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'employees/list.html', context)


@login_required
def employee_search_view(request):
    """
    Dedicated AJAX endpoint for instant search.
    Returns partial HTML table rows.
    """
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', '-created_at')
    
    allowed_sort_fields = ['employee_id', 'full_name', 'department', 'designation', 'phone', 'status', '-created_at']
    if sort_by not in allowed_sort_fields:
        sort_by = '-created_at'

    employees = Employee.objects.all()

    if query:
        employees = employees.filter(
            Q(full_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(department__icontains=query) |
            Q(designation__icontains=query)
        )

    employees = employees.order_by(sort_by)
    
    # We paginate the AJAX results identically
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'employees/partial_list_rows.html', context)


@login_required
def employee_detail_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/detail.html', {'employee': employee})


@login_required
def employee_create_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee {employee.full_name} Added Successfully!")
            return redirect('employee_list')
        else:
            messages.error(request, "Failed to add employee. Please correct the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'employees/form.html', {'form': form, 'action': 'Add'})


@login_required
def employee_update_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee {employee.full_name} Updated Successfully!")
            return redirect('employee_detail', pk=employee.pk)
        else:
            messages.error(request, "Failed to update employee. Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/form.html', {'form': form, 'action': 'Update', 'employee': employee})


@login_required
def employee_delete_view(request, pk):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=pk)
        name = employee.full_name
        employee.delete()
        messages.success(request, f"Employee {name} Deleted Successfully!")
    return redirect('employee_list')


# --- Admin Profile View ---

@login_required
def admin_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin Profile Updated Successfully!")
            return redirect('admin_profile')
        else:
            messages.error(request, "Failed to update profile. Please correct the errors.")
    else:
        form = AdminProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})


# --- Custom 404 handler ---

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
