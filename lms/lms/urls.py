"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
 team-sc
    path('', include('student.urls')),

    path('', include('DB.urls')),
    path('', include('dashboard.urls')),
    path('bulkUp/', include('bulkUp.urls')),
    path('mediahandler/', include('mediahandler.urls')),
    path('apis/', include('API_Handler.urls')),
 main
]

# Force Django to serve media files even when DEBUG = False
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Serve static files in production
