from django.urls import path
from . import views

urlpatterns = [
    path('profiles/<pk>', views.UserDetailView.as_view(), name='user_detail'),
    # path('book', views.TransactionEditView.as_view(), name='trasaction_booking'), 
    path('settings', views.UserSettingsView.as_view(), name='user_settings'),
    path('', views.LandingPage.as_view(), name='landing_page'),
    path('contact', views.Contact.as_view(), name='contact'),
    path('about-us', views.AboutUs.as_view(), name='about_us'),
]
