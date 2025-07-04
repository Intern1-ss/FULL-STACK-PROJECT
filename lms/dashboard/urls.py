from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('faculty/', views.faculty, name='faculty'),
    path('departments/', views.departments, name='departments'),
    path('campus/', views.campus, name='campus'),
    path('programs/', views.programs, name='programs'),
    path('courses/', views.courses_page, name='courses'),
    path('courses/view/<str:programme_code>/<int:batch>/', views.view_courses, name='view_courses'),

    path('courses/edit/<int:program_id>/', views.edit_courses, name='edit_courses'),
     
    path('add-course/<str:programme_code>/<int:batch>/', views.add_course, name='add_course'),

    path('students/add/', views.addstudent, name='addstudent'),
    path('faculty/add/', views.addfaculty, name='addfaculty'),
    path('programs/add/', views.addprogram, name='addprogram'),
    path('faculty/upload/', views.uploadfaculty, name='uploadfaculty'),
    path('departments/upload/', views.uploaddepartment, name='uploaddepartment'),
    path('campus/upload/', views.uploadcampus, name='uploadcampus'),
    path('students/upload/', views.uploadstudent, name='uploadstudent'),
    path('programs/upload/', views.uploadprogram, name='uploadprogram'),
    path('departments/add/', views.adddepartment, name='adddepartment'),
    path('campus/add/', views.addcampus, name='addcampus'),
    path('students/edit/<str:regd_no>/', views.edit_student, name='edit_student'),
    path('students/delete/<str:regd_no>/', views.delete_student, name='del_student'),
    path('faculty/edit/<str:faculty_id>/', views.edit_faculty, name='edit_faculty'),
    path('departments/edit/<str:dept_id>/', views.edit_department, name='edit_department'),
    path('campus/edit/<str:campus_id>/', views.edit_campus, name='edit_campus'),
    path('faculty/delete/<str:faculty_id>/', views.delete_faculty, name='del_faculty'),
    path('departments/delete/<str:dept_id>/', views.delete_department, name='del_department'),
    path('campus/delete/<str:campus_id>/', views.delete_campus, name='del_campus'),
    path('programs/edit/<int:program_id>/', views.edit_program, name='edit_program'),
    path('programs/delete/<int:program_id>/', views.delete_program, name='del_program'),


    path('courses/pdf/<str:programme_code>/<int:batch>/', views.download_course_pdf, name='download_course_pdf'),

]