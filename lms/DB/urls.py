team-gj
from django.urls import path, include
from . import views
urlpatterns = []

from  django.urls import path, include
from . import views

urlpatterns = [
    path('',views.student,name='student'),
]
main
