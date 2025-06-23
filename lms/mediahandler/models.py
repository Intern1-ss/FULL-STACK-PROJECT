import uuid
import os
from datetime import datetime
from django.db import models

def rename_uploaded_file(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}--{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{ext}"  # Rename to UUID + original extension
    return os.path.join('uploads/', new_filename)

class UploadedImage(models.Model):
    title = models.CharField(max_length=100)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to=rename_uploaded_file)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
