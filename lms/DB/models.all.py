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

# Student Table
class Student(models.Model):
    regd_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100, blank=True)
    prev_degree_name = models.CharField(max_length=100, blank=True)
    prev_degree_university = models.CharField(max_length=100, blank=True)
    prev_degree_gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    programme = models.CharField(max_length=100)
    batch = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.regd_no})"


# Paper Table
class Paper(models.Model):
    paper_code = models.CharField(max_length=20, primary_key=True)
    paper_title = models.CharField(max_length=255)
    credit = models.IntegerField()
    cie_max = models.IntegerField()
    ese_max = models.IntegerField()
    cie_weight = models.IntegerField()
    ese_weight = models.IntegerField()
    primary_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='primary_papers')
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.paper_title


# PaperDepartmentAccess Table (Many-to-Many)
class PaperDepartmentAccess(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_managing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('paper', 'department')

    def __str__(self):
        return f"{self.department} - {self.paper}"


# Faculty-Paper Assignment
class FacultyPaperAssignment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.faculty} - {self.paper}"


# Student-Paper Enrollment
class StudentPaperEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"{self.student} - {self.paper}"


# Attendance Table
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.paper} - {self.date}"


# Assessment Table
class Assessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    component = models.CharField(max_length=10, choices=[('CIE', 'CIE'), ('ESE', 'ESE')])
    marks = models.FloatField()
    session_id = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student} - {self.paper} - {self.component}"

# Feedback Table
class Feedback(models.Model):
    submitted_by_student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    submitted_by_faculty = models.ForeignKey(Faculty, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    response = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='open')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {'Student' if self.submitted_by_student else 'Faculty'}"
