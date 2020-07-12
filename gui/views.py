from django.shortcuts import render
from django.conf import settings

import os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings

PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
def index(request):
    return render(request,PROJECT_APP_PATH + '/templates/gui/index.html')
    
@xframe_options_exempt
 
def display(request):
     
    return render(request,PROJECT_APP_PATH + '/templates/gui/display.html')     
     




   
