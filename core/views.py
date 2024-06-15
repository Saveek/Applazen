import matplotlib.pyplot as plt
import pandas as pd
import uuid
import os
from django.shortcuts import redirect, render

from .forms import AnalysisPromptForm, DataAnalysisForm, FileUploadForm


def handle_uploaded_file(f):
    unique_filename = str(uuid.uuid4()) + '.csv'
    file_path = os.path.join('uploaded_files', unique_filename)  # Make sure the uploaded_files directory exists
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def generate_chart(chart_type, data):
    file_path = handle_uploaded_file(data)
    df = pd.read_csv(file_path)
    
    chart_path = os.path.join('charts', f'{uuid.uuid4()}.png')  # Use a different file path with a supported image format
    
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

def HomePage(request):
    return render(request, "index.html")


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


def AboutView(request):
    return render(request, "about.html")
