from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('view/<uuid:key>/', views.view_image_by_key, name='view_image_by_key'),
    path('gallery/', views.view_images, name='view_images'),
    path('delete/<uuid:key>/', views.delete_one, name='delete_one'),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('api/upload/', views.api_upload_image, name='api_upload_image'),
    path('api/images/', views.api_view_all_images, name='api_view_all_images'),
    path('api/image/<uuid:key>/', views.api_view_image, name='api_view_image'),
    path('api/delete/<uuid:key>/', views.api_delete_one, name='api_delete_one'),
    path('api/delete_all/', views.api_delete_all, name='api_delete_all'),
    # mediahandler/urls.py
    path('image/<uuid:key>/', views.image_redirect_view, name='image_redirect'),
]
