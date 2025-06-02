from django.urls import path
from . import views

urlpatterns = [
    path('', views.studenthome, name='studenthome'),
    path('add-student/', views.add_student, name='add_student'),
    path('student/update/<int:regd_no>/', views.update_student, name='update_student'),
    path('get_districts/<int:state_id>/', views.get_districts_by_state, name='get_districts_by_state'),

    path('bulk_upload/', views.bulk_upload_students, name='bulk_upload'),
]
