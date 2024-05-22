from django.shortcuts import render, redirect

def HomePage(request):
  return render(request, 'index.html')


def ChatPage(request):
  return render(request, "chat.html")

def AboutView(request):
  return render(request, "about.html")