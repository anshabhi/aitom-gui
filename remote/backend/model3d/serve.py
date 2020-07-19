from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import json
from ..util import request_check
from .contour import contour
from .MrcLoader import MrcLoader
from urllib.parse import urljoin
import os.path

from django_server.models import Document
from django_server.forms import DocumentForm

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y', 'z'])

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

def process_json(request: HttpRequest):
    check = request_check(request)
    if check: return check

    # extract data from json
    try:
        file_path = eval(request.POST['filename'])[0]
        lu = Point(*map(int, (request.POST['luX'], request.POST['luY'], request.POST['luZ'])))
        rd = Point(*map(int, (request.POST['rdX'], request.POST['rdY'], request.POST['rdZ'])))
    except Exception as e:
        return HttpResponse('key error: {}'.format(str(e)), status=400)

    # check data
    base_mrc_folder = os.path.join(PROJECT_APP_PATH, 'uploads', 'mrc')
    base_vtk_folder = os.path.join(PROJECT_APP_PATH, 'uploads', 'vtk')
    base_temp_folder = os.path.join(PROJECT_APP_PATH, 'uploads', 'temp')
    abs_file_path = os.path.join(PROJECT_APP_PATH, 'uploads', file_path)
    print(abs_file_path)
    if not os.path.exists(abs_file_path): # check file exists
        return HttpResponse('file not exists on server', status=400)
    if any([lu.x >= rd.x, lu.y >= rd.y, lu.z >= rd.z]): # check point
        return HttpResponse('left-up point should be smaller than right-down point', status=400)

    try:
        scaled_mrc_name = MrcLoader(abs_file_path).read(lu, rd, scale=0, base_path=base_temp_folder)
        obj_path = os.path.join(base_vtk_folder, scaled_mrc_name.replace('.mrc', '.vtk'))
        contour(os.path.join(base_temp_folder, scaled_mrc_name), obj_path)
        uploaded_file_url = urljoin('/uploads/vtk/', scaled_mrc_name.replace('.mrc', '.vtk'))
    except Exception as e:
        return HttpResponse('error occured when processing files:{}'.format(str(e)), status=400)


    return HttpResponse(uploaded_file_url, status=201)
