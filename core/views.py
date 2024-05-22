from django.shortcuts import render, redirect

def HomePage(request):
  return render(request, 'index.html')
