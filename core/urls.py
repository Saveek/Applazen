from django.urls import path
from . import views

from django.conf import settings

from django.conf.urls.static import static
app_name = "core"
urlpatterns = [
    path("", views.HomePage, name="index"),
    path("chat/", views.ChatPage, name="chat"),
    path("home/", views.HomeView, name="home"),
    path("about/", views.AboutView, name="about"),
    path("accounts/", views.AccountsView, name="accounts"),
    path("base/", views.BaseView, name="base"),
    path("budget/", views.BudgetView, name="budget"),
    path("feature/", views.FeaturesView, name="features"),
    path("goals/", views.GoalsView, name="goals"),
    path("intelligence/", views.IntelligenceView, name="intelligence"),
    path("investments/", views.InvestmentsView, name="investments"),
    path("landing1/", views.LandingView, name="landing"),
    #path("landing1/", views.Transactions, name="landing"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)