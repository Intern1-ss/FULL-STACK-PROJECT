from django.contrib import admin
from .models import Department, Campus, Faculty, Program, Student

# Register your models here.
admin.site.register(Department)
admin.site.register(Campus)
admin.site.register(Faculty)
admin.site.register(Program)
admin.site.register(Student)