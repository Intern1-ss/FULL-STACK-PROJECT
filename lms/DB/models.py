from django.db import models

# Create your models here.

# Department Table
class Department(models.Model):
    dept_id = models.CharField(max_length=10, primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    hod = models.OneToOneField('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dept_name

#Campus Table
class Campus(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    campus_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.campus_name
    
from django.core.exceptions import ValidationError

def validate_fixed_length(value):
    if len(value) != 4:
        raise ValidationError('This field must be exactly 4 characters long.')

# Faculty Table
class Faculty(models.Model):
    faculty_id = models.CharField(max_length=4, primary_key=True, validators=[validate_fixed_length])
    dob = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL,null=True, related_name='campus_faculty')
    qualification = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,null=True, related_name='faculty')
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

from datetime import datetime

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    duration_years = models.IntegerField(default=4)
    
    class Meta:
        db_table = 'program'

    def __str__(self):
        return self.code

class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('detention', 'Detention'),
        ('graduated', 'Graduated'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    regd_no = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    district_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    prev_degree1_name = models.CharField(max_length=255, blank=True, null=True)
    prev_degree1_university = models.CharField(max_length=255, blank=True,  null=True)
    prev_degree1_gpa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    prev_degree2_name = models.CharField(max_length=255, blank=True, null=True)
    prev_degree2_university = models.CharField(max_length=255, blank=True, null=True)
    prev_degree2_gpa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, null=True)
    birthday = models.DateField(null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    batch = models.IntegerField(default=datetime.now().year)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return f"{self.regd_no} - {self.name}"
