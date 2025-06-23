# mediahandler/utils.py
from .models import UploadedImage

def handle_image_upload(file_obj, title=None):
    """
    Accepts a file object, creates an UploadedImage, and returns the instance.
    """
    image = UploadedImage(title=title, image=file_obj)
    image.save()
    return image

def delete_image(title):
    """
    Deletes an image by its title.
    Returns True if the image was deleted, False if it did not exist.
    """
    try:
        image = UploadedImage.objects.get(title=title)
        # Delete file from disk
        if image.image and image.image.path:
            image.image.delete(save=False)  # Deletes the file from disk
        image.delete()
        return True
    except UploadedImage.DoesNotExist:
        return False