from django.shortcuts import redirect, render

from .forms import AnalysisPromptForm, FileUploadForm


def HomePage(request):
    return render(request, "index.html")


def ChatPage(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # return redirect('analyze_file', file_id=uploaded_file.id)
    else:
        form = FileUploadForm()
    return render(request, "chat.html", {"form": form})


def AboutView(request):
    return render(request, "about.html")
