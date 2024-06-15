from django import forms

from .models import DataFile

CHART_CHOICES = [
    ('line', 'Line Chart'),
    ('bar', 'Bar Chart'),
    ('scatter', 'Scatter Plot'),
    ('pie', 'Pie Chart'),
]

class FileUploadForm(forms.ModelForm):
   class Meta:
    model = DataFile
    fields = ('file',)
    
class AnalysisPromptForm(forms.Form):
  prompt = forms.CharField(widget=forms.Textarea)
      
class DataAnalysisForm(forms.Form):
    file = forms.FileField(label='Upload CSV File')
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label='Select Chart Type')


