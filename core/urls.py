from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.HomePage, name="home"),
    path("chat/", views.ChatPage, name="chat"),
    #path("about/", views.AboutView, name="about")
]