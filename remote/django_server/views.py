from django.shortcuts import render
from django.conf import settings

import os.path
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from django_server.models import Document
from django_server.forms import DocumentForm,InputForm
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django import forms
import glob
import json


PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP_PATH = os.path.abspath(os.path.join(PROJECT_APP_PATH, os.pardir))

def index(request):
    #form = DocumentForm()
    return render(request, PROJECT_APP_PATH + '/frontend/templates/frontend/index.html')

    
@xframe_options_exempt
 
def display(request):
     
    return render(request,PROJECT_APP_PATH + '/frontend/templates/frontend/display.html')     
    
#https://stackoverflow.com/questions/43591440/django-1-11-download-file-chunk-by-chunk     
def download(request):

    file_path = PROJECT_APP_PATH + request.GET["path"]
    print(file_path)
    chunk_size = 8192#DEFINE_A_CHUNK_SIZE_AS_INTEGER
    filename = os.path.basename(file_path)
    print(filename)
    response = StreamingHttpResponse(
        FileWrapper(open(file_path, 'rb'), chunk_size),
        content_type="application/octet-stream"
    )
    response['Content-Length'] = os.path.getsize(file_path)    
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def getUploadForm(request):
    form = DocumentForm()	
    return render(request, PROJECT_APP_PATH + '/frontend/templates/frontend/upload.html', {
        'form': form
    })

class MyForm(forms.Form):
    names = []
    
# To browse your saved file, get the containing models
    documents = glob.glob(PROJECT_APP_PATH + "/uploads/mrc/*.mrc")
    
    for doc in documents:    
     name = doc.split('/')[-1]
     #print(name)
     names.append([name,name])
	
    select = forms.ChoiceField(widget=forms.Select, choices=names)
    
def getLibrary(request):
    
    return render(request, PROJECT_APP_PATH + '/frontend/templates/frontend/list.html', {
        'form': MyForm()
    })

def getInputForm(request):
    form = InputForm()
   # print(dict(request.POST).keys()[0]) #using this non standard approach cause I can't figure out why dictionary is not loading properly
    return render(request, PROJECT_APP_PATH + '/frontend/templates/frontend/input.html', {
        'form': form,'filename':list(dict(request.POST).keys())[0]
    })    
