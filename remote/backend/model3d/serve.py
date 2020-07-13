from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import json
from ..util import request_check
from .contour import contour
from urllib.parse import urljoin
import os.path

from django_server.models import Document
from django_server.forms import DocumentForm

PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP_PATH = os.path.abspath(os.path.join(PROJECT_APP_PATH, os.pardir)) #1 level parent
PROJECT_APP_PATH = os.path.abspath(os.path.join(PROJECT_APP_PATH, os.pardir)) #2 level parent (root directory)
"""
def process(request: HttpRequest):
    #check = request_check(request)
    #if check: return check


    if request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('test.mrc', myfile.file)
        obj = contour(filename, filename.replace(".mrc",".vtk"))
        #print('here')
        #filename = fs.save('test.vtk', obj)
     #   uploaded_file_url = fs.url(filename)
        uploaded_file_url = urljoin('/uploads/', filename.replace(".mrc",".vtk"))
        print(uploaded_file_url)
        return render(request, PROJECT_APP_PATH + '/frontend/templates/frontend/index.html', {
            'uploaded_file_url': uploaded_file_url
        })

#New model field based process()
def process(request):
    if request.method == 'POST':

        form = DocumentForm(request.POST, request.FILES)
       # print(form.is_valid())
        if form.is_valid():
        #if True:
            filename = str(form.save().document)
            
            
            obj = contour(filename, filename.replace(".mrc",".vtk"))
            uploaded_file_url = urljoin('/uploads/', filename.replace(".mrc",".vtk"))
            #print(uploaded_file_url)
            return render(request, PROJECT_APP_PATH + '/frontend/templates/frontend/index.html', {'uploaded_file_url': uploaded_file_url},{
        'form': form
    })
    else:
        form = DocumentForm()
    return render(request, PROJECT_APP_PATH + '/frontend/templates/frontend/index.html', {
        'form': form
    })    
    
"""    

from django2_resumable.files import ResumableFile, get_storage, get_chunks_upload_to


def process(request):
    upload_to = get_chunks_upload_to(request)
    storage = get_storage(upload_to)
    if request.method == 'POST':
        chunk = request.FILES.get('file')
        r = ResumableFile(storage, request.POST)
        if not r.chunk_exists:
            r.process_chunk(chunk)
        if r.is_complete:
            filename =  str(storage.save(r.filename, r.file))
            r.delete_chunks()
            #print(filename)
            base = PROJECT_APP_PATH + '/uploads'
            obj = contour(base + '/mrc/' + filename, base + '/vtk/' + filename.replace(".mrc",".vtk"))
            uploaded_file_url = urljoin('/uploads/vtk/', filename.replace(".mrc",".vtk"))
            #print(uploaded_file_url)

            return HttpResponse(uploaded_file_url, status=201) 
        return HttpResponse('chunk uploaded')
    elif request.method == 'GET':
        r = ResumableFile(storage, request.GET)
        if not r.chunk_exists:
            return HttpResponse('chunk not found', status=404)
        if r.is_complete:
            actual_filename = storage.save(r.filename, r.file)
            r.delete_chunks()
            return HttpResponse(storage.url(actual_filename), status=201)
        return HttpResponse('chunk exists', status=200) 
