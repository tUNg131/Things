from django.urls import path
from .views import UserDetailView, UserSettingsView, LandingPage
from django.views.generic.base import TemplateView

urlpatterns = [
    path('profiles/<pk>', UserDetailView.as_view(), name='user_detail'),
    # path('book', views.TransactionEditView.as_view(), name='trasaction_booking'), 
    path('settings', UserSettingsView.as_view(), name='user_settings'),
    path('', LandingPage.as_view(), name='landing_page'),
    path(
        'contact',
        TemplateView.as_view(
            template_name='collect/contact.html',
        ),
        name='contact',
    ),

    path(
        'about',
        TemplateView.as_view(
            template_name='collect/about_us.html'
        ),
        name='about_us',
    ),

    path(
        'test_login',
        TemplateView.as_view(
            template_name='collect/login_form_bootstrap4.html',
        ),
        name='test_login',
    )
]
