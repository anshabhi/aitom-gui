from django.db import models
from django2_resumable.fields import ResumableFileField


class Document(models.Model):
    #input form for resumeable.js
    #description = models.CharField(max_length=255, blank=True)
    #document = models.FileField(upload_to='')
    document = ResumableFileField(chunks_upload_to='mrc/')

    #can optionally add the timestamp of file upload
    #uploaded_at = models.DateTimeField(auto_now_add=True) 
    

class Input(models.Model):
    #define a form with 6 input fields for coordinates
    luX = models.IntegerField(default=0)
    luY = models.IntegerField(default=0)
    luZ = models.IntegerField(default=0)
    
    rdX = models.IntegerField(default=0)
    rdY = models.IntegerField(default=0)
    rdZ = models.IntegerField(default=0)

