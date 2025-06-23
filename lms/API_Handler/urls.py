from django.urls import path
from . import views

urlpatterns = [
    path('students/<str:regd_no>/', views.view_student, name='view_student'),
    path('faculty/<str:faculty_id>/', views.view_faculty, name='view_faculty'),
    path('departments/<str:dept_id>/', views.view_department, name='view_department'),
    path('campus/<str:campus_id>/', views.view_campus, name='view_campus'),
    path('programs/<int:program_id>/', views.view_program, name='view_program'),
]