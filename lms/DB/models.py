from django.db import models

# Create your models here.

# Department Table
class Department(models.Model):
    dept_id = models.CharField(max_length=10, primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    hod = models.OneToOneField('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dept_name

#Campus Table
class Campus(models.Model):
    campus_id = models.CharField(max_length=10, primary_key=True)
    campus_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
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
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='campus_faculty')
    qualification = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty')
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
