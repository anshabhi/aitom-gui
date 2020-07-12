from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import json
from ..util import request_check
from .contour import contour
from urllib.parse import urljoin

def process(request: HttpRequest):
    check = request_check(request)
    if check: return check


    if request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('test.mrc', myfile.file)
        obj = contour(filename, filename.replace(".mrc",".vtk"))
        #filename = fs.save('test.vtk', obj)
     #   uploaded_file_url = fs.url(filename)
        uploaded_file_url = urljoin('/mrc/', filename.replace(".mrc",".vtk"))
        return render(request, PROJECT_APP_PATH + '/templates/gui/index.html', {
            'uploaded_file_url': uploaded_file_url
        })