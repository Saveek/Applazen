import os
import uuid

import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings
from django.shortcuts import redirect, render

from .forms import AnalysisPromptForm, DataAnalysisForm, FileUploadForm

# Define base directories for uploads and charts
UPLOAD_DIR = os.path.join(settings.STATIC_ROOT, 'uploaded_files')
CHART_DIR = os.path.join(settings.STATIC_ROOT, 'charts')

def handle_uploaded_file(f):
    unique_filename = str(uuid.uuid4()) + '.csv'
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Ensure the upload directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path, unique_filename

def generate_chart(chart_type, data):
    file_path, unique_filename = handle_uploaded_file(data)
    df = pd.read_csv(file_path)
    
    chart_filename = f'{unique_filename.split(".")[0]}.png'  # Use the same filename but with a different extension
    chart_path = os.path.join(CHART_DIR, chart_filename)
    
    # Ensure the chart directory exists
    if not os.path.exists(CHART_DIR):
        os.makedirs(CHART_DIR)
    
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
    return chart_path

def ChatPage(request):
    if request.method == 'POST':
        form = DataAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            chart_type = form.cleaned_data['chart_type']
            data = form.cleaned_data['file'] 
            chart_path = generate_chart(chart_type, data)
            chart_url = f'charts/{os.path.basename(chart_path)}'
            chart_url = os.path.join(settings.STATIC_URL, 'charts', os.path.basename(chart_path))
            return render(request, 'chat.html', {'form': form, 'chart_path': chart_url})
    else:
        form = DataAnalysisForm()
    return render(request, 'chat.html', {'form': form})


def HomePage(request):
    return render(request, "index.html")

def AboutView(request):
    return render(request, "about.html")
