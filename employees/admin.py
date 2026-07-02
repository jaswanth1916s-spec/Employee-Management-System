from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'email', 'phone', 'department', 'designation', 'status', 'date_of_joining')
    list_filter = ('status', 'gender', 'department')
    search_fields = ('employee_id', 'full_name', 'email', 'department', 'designation')
    ordering = ('-created_at',)
    readonly_fields = ('employee_id', 'created_at')
