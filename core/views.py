import os
import uuid

import matplotlib.pyplot as plt
import pandas as pd
from django.shortcuts import redirect, render

from .forms import AnalysisPromptForm, DataAnalysisForm, FileUploadForm

# Define base directories for uploads and charts
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'uploaded_files')
CHART_DIR = os.path.join(settings.BASE_DIR, 'charts')

def handle_uploaded_file(f):
    unique_filename = str(uuid.uuid4()) + '.csv'
    file_path = os.path.join('uploaded_files', unique_filename)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path, unique_filename

def generate_chart(chart_type, data):
    file_path, unique_filename = handle_uploaded_file(data)
    df = pd.read_csv(file_path)
    
    chart_filename = f'{unique_filename.split(".")[0]}.png'  
    chart_path = os.path.join('charts', chart_filename)
    chart_dir = os.path.dirname(chart_path)
    print(chart_path)
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'line':
        df.plot(kind='line')
    elif chart_type == 'bar':
        df.plot(kind='bar')
    elif chart_type == 'scatter':
        df.plot(kind='scatter', x=df.columns[0], y=df.columns[1])
    elif chart_type == 'pie':
        df.plot(kind='pie', y=df.columns[0])
    else:
        raise ValueError("Invalid chart type")
    
    plt.savefig(chart_path)
    plt.close()
    print(f"Chart saved at: {chart_path}")
    return chart_path

def ChatPage(request):
    if request.method == 'POST':
        form = DataAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            chart_type = form.cleaned_data['chart_type']
            data = form.cleaned_data['file'] 
            chart_path = generate_chart(chart_type, data)
            return render(request, 'chat.html', {'form': form, 'chart_path': chart_path})
    else:
        form = DataAnalysisForm()
    return render(request, 'chat.html', {'form': form})


def HomePage(request):
    return render(request, "index.html")



def AboutView(request):
    return render(request, "about.html")
