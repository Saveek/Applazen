import matplotlib.pyplot as plt
import pandas as pd
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
    unique_filename = str(uuid.uuid4()) + '.png'
    file_path = os.path.join('static', unique_filename)

    if chart_type == 'line':
        plt.figure(figsize=(10, 6))
        data.plot(kind='line')
    elif chart_type == 'bar':
        plt.figure(figsize=(10, 6))
        data.plot(kind='bar')
    elif chart_type == 'scatter':
        plt.figure(figsize=(10, 6))
        data.plot(kind='scatter', x=data.columns[0], y=data.columns[1])
    elif chart_type == 'pie':
        plt.figure(figsize=(10, 6))
        data.plot(kind='pie', y=data.columns[0])

    plt.savefig(file_path)
    plt.close()
    
    return file_path

def HomePage(request):
    return render(request, "index.html")


def ChatPage(request):
    if request.method == 'POST':
        form = DataAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['data']  # Assuming data is in a format suitable for plotting
            chart_path = generate_chart(chart_type, data)
            handle_uploaded_file(data)
            chart_type = form.cleaned_data['chart_type']
            data = pd.read_csv('uploaded_file.csv')
            generate_chart(chart_type, data)
            return render(request, 'chat.html', {'form': form, 'chart': 'chart.png'})
    else:
        form = DataAnalysisForm()
    return render(request, 'chat.html', {'form': form})


def AboutView(request):
    return render(request, "about.html")
