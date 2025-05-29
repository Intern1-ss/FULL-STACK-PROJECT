from django.db import models
from datetime import datetime

class Program(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'program'

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        unique_together = ('name', 'state')

    def __str__(self):
        return f"{self.name}, {self.state.name}"

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
    state_name = models.CharField(max_length=100, blank=True, null=True)
    district_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    prev_degree1_name = models.CharField(max_length=255, blank=True, null=True)
    prev_degree1_university = models.CharField(max_length=255, blank=True, null=True)
    prev_degree1_gpa = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    prev_degree2_name = models.CharField(max_length=255, blank=True, null=True)
    prev_degree2_university = models.CharField(max_length=255, blank=True, null=True)
    prev_degree2_gpa = models.DecimalField(max_digits=5, decimal_places=2, null=True)
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
