from django import forms
from .models import Document,Input

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',) 

class InputForm(forms.ModelForm):
    class Meta:
    	model = Input
    	fields = ('luX','luY','luZ','rdX','rdY','rdZ',)        
