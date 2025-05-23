from django.contrib import admin
from .models import Department, Campus, Faculty

# Register your models here.
admin.site.register(Department)
admin.site.register(Campus)
admin.site.register(Faculty)