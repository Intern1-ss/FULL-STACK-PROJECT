import os
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from .models import UploadedImage
from .forms import ImageUploadForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(f"Image uploaded successfully. Access key: <b>{instance.key}</b><br>"
                                f"View it at: <a href='/mediahandler/view/{instance.key}/'>Link</a>")
    else:
        form = ImageUploadForm()
    return render(request, 'mediahandler/upload.html', {'form': form})


def view_images(request):
    images = UploadedImage.objects.all()
    return render(request, 'mediahandler/gallery.html', {'images': images})

def view_image_by_key(request, key):
    image = get_object_or_404(UploadedImage, key=key)
    return render(request, 'mediahandler/view_image.html', {'image': image})

def delete_one(request, key):
    # Find the image object by key (UUIDField)
    image = get_object_or_404(UploadedImage, key=key)
    
    # Delete the file from disk
    if image.image and os.path.isfile(image.image.path):
        os.remove(image.image.path)
    
    # Delete the DB record
    image.delete()
    
    return HttpResponse(f"Image with key {key} deleted successfully.")

# mediahandler/views.py
def delete_all(request):
    images = UploadedImage.objects.all()
    count = images.count()
    
    for image in images:
        # Delete file from disk
        if image.image and os.path.isfile(image.image.path):
            os.remove(image.image.path)
        # Delete DB record
        image.delete()
    
    return HttpResponse(f"Deleted all {count} images successfully.")

@csrf_exempt
def api_upload_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    form = ImageUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)
    if form.is_valid():
        instance = form.save()
        data = {
            'message': 'Image uploaded successfully',
            'key': str(instance.key),
            'url': request.build_absolute_uri(instance.image.url)
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'errors': form.errors}, status=400)


def api_view_image(request, key):
    image = get_object_or_404(UploadedImage, key=key)
    data = {
        'key': str(image.key),
        'url': request.build_absolute_uri(image.image.url),
        'uploaded_at': image.uploaded_at.isoformat(),
    }
    return JsonResponse(data)


def api_view_all_images(request):
    images = UploadedImage.objects.all()
    data = []
    for image in images:
        data.append({
            'key': str(image.key),
            'url': request.build_absolute_uri(image.image.url),
            'uploaded_at': image.uploaded_at.isoformat(),
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def api_delete_one(request, key):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'DELETE request required'}, status=405)

    image = get_object_or_404(UploadedImage, key=key)
    if image.image and os.path.isfile(image.image.path):
        os.remove(image.image.path)
    image.delete()
    return JsonResponse({'message': f'Image with key {key} deleted successfully.'})


@csrf_exempt
def api_delete_all(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'DELETE request required'}, status=405)

    images = UploadedImage.objects.all()
    count = images.count()
    for image in images:
        if image.image and os.path.isfile(image.image.path):
            os.remove(image.image.path)
        image.delete()
    return JsonResponse({'message': f'Deleted all {count} images successfully.'})

def image_redirect_view(request, key):
    image = get_object_or_404(UploadedImage, key=key)
    return redirect(image.image.url)