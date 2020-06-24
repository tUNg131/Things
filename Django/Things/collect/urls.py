from django.urls import path

from . import views

urlpatterns = [
    path('home', views.Index.as_view(), name='index'),
    path('book', views.TransactionEditView.as_view(), name='trasaction_booking'),
    path('', views.LandingPage.as_view(), name='landing_page'),
]
