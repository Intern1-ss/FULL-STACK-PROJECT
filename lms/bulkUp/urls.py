from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='bulkUp_home'),
    
    # Department
    path('download/department/', views.download_department_template, name='download_department_template'),
    path('upload/department/', views.upload_department_excel, name='upload_department_excel'),

    # Campus
    path('download/campus/', views.download_campus_template, name='download_campus_template'),
    path('upload/campus/', views.upload_campus_excel, name='upload_campus_excel'),

    # Faculty
    path('download/faculty/', views.download_faculty_template, name='download_faculty_template'),
    path('upload/faculty/', views.upload_faculty_excel, name='upload_faculty_excel'),

    # Program
    path('download/program/', views.download_program_template, name='download_program_template'),
    path('upload/program/', views.upload_program_excel, name='upload_program_excel'),

    # Student
    path('download/student/', views.download_student_template, name='download_student_template'),
    path('upload/student/', views.upload_student_excel, name='upload_student_excel'),

    path('report/', views.generate_error_pdf, name='bulkUp_report'),
]
