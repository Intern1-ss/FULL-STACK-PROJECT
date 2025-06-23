from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


# Department Table
class Department(models.Model):
    """Model representing an academic department."""
    dept_id = models.CharField(max_length=10, primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    hod = models.OneToOneField('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dept_name


# Campus Table
class Campus(models.Model):
    """Model representing a campus."""
    id = models.CharField(max_length=10, primary_key=True)
    campus_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.campus_name


def validate_fixed_length(value):
    if len(value) != 4:
        raise ValidationError('This field must be exactly 4 characters long.')


# Faculty Table
class Faculty(models.Model):
    """Model representing a faculty member."""
    faculty_id = models.CharField(max_length=4, primary_key=True, validators=[validate_fixed_length])
    dp_key = models.UUIDField(default=None, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, related_name='campus_faculty')
    qualification = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='faculty')
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Program Table
class Program(models.Model):
    """Model representing an academic program under a department."""
    programme_code = models.CharField(max_length=20)
    batch = models.IntegerField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE, db_column='department_id')
    programme_short_name = models.CharField(max_length=100)
    programme_full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PROGRAMME_DATA'
        unique_together = ('programme_code', 'batch')

    def __str__(self):
        return f"{self.programme_code} ({self.batch})"


# Student Table
class Student(models.Model):
    """Model representing a student enrolled in a program."""
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
    dp_key = models.UUIDField(default=None, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, default="Male", blank=True, null=True)
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


# Course Table
class Course(models.Model):
    """Model representing a course (paper) under a program and batch."""
    CATEGORY_CHOICES = [
        ('Theory', 'Theory'),
        ('Practical', 'Practical'),
        ('Core', 'Core'),
        ('Elective', 'Elective'),
    ]

    programme_code = models.CharField(max_length=20)
    batch = models.IntegerField()
    paper_code = models.CharField(max_length=20)
    paper_title = models.CharField(max_length=150)
    sequence = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    cie_max = models.IntegerField()
    cie_max_atp = models.IntegerField(null=True, blank=True)
    cie_max_psn = models.IntegerField(null=True, blank=True)
    cie_max_brn = models.IntegerField(null=True, blank=True)
    cie_max_ndg = models.IntegerField(null=True, blank=True)
    ese_max = models.IntegerField()
    ese_max_atp = models.IntegerField(null=True, blank=True)
    ese_max_psn = models.IntegerField(null=True, blank=True)
    ese_max_brn = models.IntegerField(null=True, blank=True)
    ese_max_ndg = models.IntegerField(null=True, blank=True)
    cie_wtg = models.DecimalField(max_digits=5, decimal_places=2)
    ese_wtg = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('programme_code', 'batch', 'paper_code')

    def __str__(self):
        return self.paper_code
