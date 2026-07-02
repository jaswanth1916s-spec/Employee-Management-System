from django.db import models

class Employee(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    employee_id = models.CharField(max_length=15, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_joining = models.DateField()
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_emp = Employee.objects.all().order_by('id').last()
            if not last_emp:
                self.employee_id = 'EMP-0001'
            else:
                try:
                    last_id_num = int(last_emp.employee_id.split('-')[1])
                    new_id_num = last_id_num + 1
                    self.employee_id = f'EMP-{new_id_num:04d}'
                except (IndexError, ValueError):
                    # Fallback to standard auto ID count
                    self.employee_id = f'EMP-{last_emp.id + 1:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    class Meta:
        ordering = ['-created_at']
