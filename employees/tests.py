from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from .models import Employee

class EmployeeModelTestCase(TestCase):
    def setUp(self):
        # We don't save yet in setup
        pass

    def test_employee_id_auto_generation(self):
        """Test that employee_id is auto-generated on save in pattern EMP-XXXX."""
        emp1 = Employee.objects.create(
            full_name="John Doe",
            email="john@example.com",
            phone="1234567890",
            department="IT",
            designation="Developer",
            salary=50000,
            gender="Male",
            date_of_joining=date(2026, 1, 1),
            address="123 Street",
            status="Active"
        )
        emp2 = Employee.objects.create(
            full_name="Jane Smith",
            email="jane@example.com",
            phone="9876543210",
            department="HR",
            designation="Manager",
            salary=60000,
            gender="Female",
            date_of_joining=date(2026, 1, 15),
            address="456 Road",
            status="Active"
        )
        
        self.assertEqual(emp1.employee_id, "EMP-0001")
        self.assertEqual(emp2.employee_id, "EMP-0002")

    def test_string_representation(self):
        """Test string representation of employee."""
        emp = Employee.objects.create(
            full_name="Alice Brown",
            email="alice@example.com",
            phone="1112223333",
            department="Finance",
            designation="Analyst",
            salary=55000,
            gender="Female",
            date_of_joining=date(2026, 2, 1),
            address="789 Lane",
            status="Active"
        )
        self.assertEqual(str(emp), f"Alice Brown ({emp.employee_id})")


class EmployeeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin", 
            email="admin@example.com", 
            password="adminpassword"
        )
        self.employee = Employee.objects.create(
            full_name="Bob Wilson",
            email="bob@example.com",
            phone="5556667777",
            department="Sales",
            designation="Agent",
            salary=45000,
            gender="Male",
            date_of_joining=date(2026, 3, 1),
            address="321 Blvd",
            status="Active"
        )

    def test_unauthenticated_user_redirected_to_login(self):
        """Test that access to protected URLs is restricted and redirects to login."""
        protected_urls = [
            reverse('dashboard'),
            reverse('employee_list'),
            reverse('employee_add'),
            reverse('employee_detail', args=[self.employee.pk]),
            reverse('employee_edit', args=[self.employee.pk]),
            reverse('admin_profile'),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('login'), response.url)

    def test_authenticated_dashboard_load(self):
        """Test that authenticated user can access the dashboard."""
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bob Wilson")
        self.assertContains(response, "1")  # Stats count

    def test_employee_search_ajax(self):
        """Test the AJAX search view returns matching row HTML."""
        self.client.login(username="admin", password="adminpassword")
        
        # Search match
        response = self.client.get(reverse('employee_search'), {'q': 'Bob'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bob Wilson")
        self.assertContains(response, "Sales")

        # Search mismatch
        response = self.client.get(reverse('employee_search'), {'q': 'DoesNotExist'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Bob Wilson")
        self.assertContains(response, "No matching employee records found.")
