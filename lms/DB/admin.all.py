from django.contrib import admin
from .models import Department, Campus, Faculty, Student, Paper, PaperDepartmentAccess, FacultyPaperAssignment, StudentPaperEnrollment, Assessment, Feedback

# Register your models here.
admin.site.register(Department)
admin.site.register(Campus)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Paper)
admin.site.register(PaperDepartmentAccess)
admin.site.register(FacultyPaperAssignment)
admin.site.register(StudentPaperEnrollment)
admin.site.register(Assessment)
admin.site.register(Feedback)
