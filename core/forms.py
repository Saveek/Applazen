from django import forms
from .models import DataFile

class FileUploadForm(forms.ModelForm):
   class Meta:
    model = DataFile
    fields = ('file',)
        

class AnalysisPromptForm(forms.Form):
  prompt = forms.CharField(widget=forms.Textarea)