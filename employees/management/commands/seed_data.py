from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import Employee
from datetime import date
import decimal

class Command(BaseCommand):
    help = 'Seeds the database with initial admin and employee data'

    def handle(self, *args, **kwargs):
        # 1. Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user admin/admin123 created'))
        else:
            self.stdout.write('Admin user already exists')

        # 2. Clear old employees
        Employee.objects.all().delete()
        self.stdout.write('Cleared existing employees')

        # 3. Create mock employees
        employees_data = [
            {
                'full_name': 'Eleanor Vance',
                'email': 'eleanor.vance@example.com',
                'phone': '123-456-7890',
                'department': 'Engineering',
                'designation': 'Senior Software Engineer',
                'salary': decimal.Decimal('95000.00'),
                'gender': 'Female',
                'date_of_joining': date(2023, 3, 15),
                'address': '104 High Street, Boston, MA',
                'status': 'Active'
            },
            {
                'full_name': 'Marcus Brody',
                'email': 'marcus.brody@example.com',
                'phone': '555-019-2834',
                'department': 'Human Resources',
                'designation': 'HR Director',
                'salary': decimal.Decimal('85000.00'),
                'gender': 'Male',
                'date_of_joining': date(2021, 6, 1),
                'address': '402 Oak Lane, Austin, TX',
                'status': 'Active'
            },
            {
                'full_name': 'Sophia Al-Aziz',
                'email': 'sophia.aziz@example.com',
                'phone': '512-555-0143',
                'department': 'Engineering',
                'designation': 'Frontend Engineer',
                'salary': decimal.Decimal('72000.00'),
                'gender': 'Female',
                'date_of_joining': date(2024, 1, 10),
                'address': '708 Maple Avenue, Seattle, WA',
                'status': 'Active'
            },
            {
                'full_name': 'Alistair Sterling',
                'email': 'alistair.s@example.com',
                'phone': '617-555-0182',
                'department': 'Finance',
                'designation': 'Chief Financial Officer',
                'salary': decimal.Decimal('120000.00'),
                'gender': 'Male',
                'date_of_joining': date(2020, 11, 1),
                'address': '12 Wall Street, New York, NY',
                'status': 'Active'
            },
            {
                'full_name': 'Carlos Mendez',
                'email': 'carlos.mendez@example.com',
                'phone': '305-555-0199',
                'department': 'Marketing',
                'designation': 'Creative Designer',
                'salary': decimal.Decimal('65000.00'),
                'gender': 'Male',
                'date_of_joining': date(2024, 5, 20),
                'address': '303 Ocean Drive, Miami, FL',
                'status': 'Active'
            },
            {
                'full_name': 'Diana Prince',
                'email': 'diana.prince@example.com',
                'phone': '703-555-0101',
                'department': 'Operations',
                'designation': 'Operations Manager',
                'salary': decimal.Decimal('90000.00'),
                'gender': 'Female',
                'date_of_joining': date(2022, 8, 12),
                'address': '1776 Constitution Ave, Washington, DC',
                'status': 'Active'
            },
            {
                'full_name': 'Thomas Wayne',
                'email': 'thomas.wayne@example.com',
                'phone': '201-555-0177',
                'department': 'Operations',
                'designation': 'Facilities Analyst',
                'salary': decimal.Decimal('58000.00'),
                'gender': 'Male',
                'date_of_joining': date(2025, 2, 28),
                'address': '1007 Mountain Drive, Gotham, NJ',
                'status': 'Inactive'
            },
            {
                'full_name': 'Sarah Connor',
                'email': 'sarah.connor@example.com',
                'phone': '213-555-0144',
                'department': 'Security',
                'designation': 'Information Security Specialist',
                'salary': decimal.Decimal('80000.00'),
                'gender': 'Female',
                'date_of_joining': date(2023, 10, 31),
                'address': '42 Cyberdyne Way, Los Angeles, CA',
                'status': 'Active'
            }
        ]

        for emp_data in employees_data:
            emp = Employee.objects.create(**emp_data)
            self.stdout.write(self.style.SUCCESS(f'Created employee {emp.full_name} ({emp.employee_id})'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with sample records!'))
