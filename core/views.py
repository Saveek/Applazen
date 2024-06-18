import os
import uuid

import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings
from django.shortcuts import redirect, render

genai.configure(api_key=settings.GEMINI_API_KEY)
model=genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a cat. Your name is Neko.")



from .forms import AnalysisPromptForm, DataAnalysisForm, FileUploadForm

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

def generate_chart(chart_type, file_path):
    df = pd.read_csv(file_path)
    
    chart_filename = f'{os.path.basename(file_path).split(".")[0]}.png'  # Use the same filename but with a different extension
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
    responses = []
    chart_path = None
    
    if request.method == 'POST':
        form = DataAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            prompt = form.cleaned_data.get('prompt')
            uploaded_file = request.FILES.get('file')
            chart_type = form.cleaned_data.get('chart_type')
            
            if uploaded_file and prompt:
                file_content = uploaded_file.read().decode('utf-8')
                system_instruction = f"You are a data analyst with over 20 years of experience. Your task is to execute the following prompt based on the given file:\n\n{file_content}"
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                file_path, unique_filename = handle_uploaded_file(uploaded_file)
                chart_path = generate_chart(chart_type, file_path)
                print(chart_path + "I am chart path")
                chart_url = os.path.join(settings.STATIC_URL, 'charts', os.path.basename(chart_path))
                print(chart_url + "I am chart url")
                responses.append({
                    'chart_type': chart_type,
                    'chart_path': chart_path,
                    'filename': chart_path.split('/')[-1]
                })
                
            else:
                system_instruction = f"You are a data analyst with over 20 years of experience."
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
                responses.append(response.text)   
                request.session['responses'] = responses
            context = {
                    'chart_type': chart_type,
                    'chart_path': chart_path,
                    #'filename': chart_path.split('/')[-1],
                    'form': form, 
                    # 'responses': responses,
                }
    else:
        print(responses)
        form = DataAnalysisForm()
    
    return render(request, 'chat.html',context = context)

def HomePage(request):
    return render(request, "index.html")

def AboutView(request):
    return render(request, "about.html")

def HomeView(request):
    return render(request, "home.html")