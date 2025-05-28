from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('faculty/', views.faculty, name='faculty'),
    path('departments/', views.departments, name='departments'),
    path('students/add/', views.addstudent, name='addstudent'),
    path('faculty/add/', views.addfaculty, name='addfaculty'),
    path('departments/add/', views.adddepartment, name='adddepartment'),
    path('faculty/edit/<str:faculty_id>/', views.edit_faculty, name='edit_faculty'),
    path('departments/edit/<str:dept_id>/', views.edit_department, name='edit_department'),
    path('faculty/delete/<str:faculty_id>/', views.delete_faculty, name='del_faculty'),
    path('departments/delete/<str:dept_id>/', views.delete_department, name='del_department'),
]