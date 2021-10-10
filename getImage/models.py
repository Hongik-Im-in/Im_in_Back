from django.db import models
import os

def image_upload_path(instance, filename):
    return 'face/'+os.path.join(instance.title, filename)

class Image(models.Model):
    title = models.CharField(max_length=200, default='None')
    image = models.ImageField(upload_to=image_upload_path, default='../media/james.jpg')
    
    
    def __str__(self):
        return self.title
