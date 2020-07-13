from django.db import models
from django2_resumable.fields import ResumableFileField


class Document(models.Model):
    #description = models.CharField(max_length=255, blank=True)
    #document = models.FileField(upload_to='')
    document = ResumableFileField(chunks_upload_to='mrc/')

    #uploaded_at = models.DateTimeField(auto_now_add=True) 
    

class Input(models.Model):
    #description = models.CharField(max_length=255, blank=True)
    #document = models.FileField(upload_to='')
    luX = models.IntegerField(default=0)
    luY = models.IntegerField(default=0)
    luZ = models.IntegerField(default=0)
    
    rdX = models.IntegerField(default=0)
    rdY = models.IntegerField(default=0)
    rdZ = models.IntegerField(default=0)

    #uploaded_at = models.DateTimeField(auto_now_add=True)     
