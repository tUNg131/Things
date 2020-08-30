from django.urls import path, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView
from .views import PasswordChangeView, RegistrationView, ActivationView
from .models import User

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .forms import (
    LoginForm,
    RegisterForm,
    SettingsForm,
    PasswordResetUserForm,
    SetPasswordUserForm,
)

# from django_registration.backends.activation.views import ActivationView

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='accounts/login.html',
            form_class=LoginForm,
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(
            next_page=reverse_lazy('landing_page'),
        ), 
        name='logout',
    ),

    path(
        'register/',
        RegistrationView.as_view(
            template_name='accounts/registration_form.html',
            form_class=RegisterForm,
            success_url=reverse_lazy('register_complete'),
            disallowed_url=reverse_lazy("register_disallowed"),
        ),
        name='register',
    ),

    path(
        "register/complete/",
        TemplateView.as_view(
            template_name="accounts/registration_complete.html"
        ),
        name="register_complete",
    ),

    path(
        "activate/complete/",
        TemplateView.as_view(
            template_name="accounts/activation_complete.html"
        ),
        name="activation_complete",
    ),

    path(
        "activate/<str:activation_key>/",
        ActivationView.as_view(
    
        ),
        name="activate",
    ),

    path(
        "register/closed/",
        TemplateView.as_view(
            template_name="django_registration/registration_closed.html"
        ),
        name="register_disallowed",
    ),

    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name='password_change',
    ),

    path(
        "password/change/done/",
        PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ), 
        name='password_change_done',
    ),

    path(
        "password/reset/",
        PasswordResetView.as_view(
            template_name='password_reset_form.html',
            form_class=PasswordResetUserForm,
        ), 
        name='password_reset',
    ),

    path(
        "password/reset/done/",
        PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html',
        ), 
        name='password_reset_done',
    ),

    path(
        "password/reset/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            form_class=SetPasswordUserForm,
        ), 
        name='password_reset_confirm',
    ),

    path(
        "password/reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ), 
        name='password_reset_complete',
    ),
    
    path(
        "<int:pk>/settings/",
        UpdateView.as_view(
            template_name='accounts/settings.html',
            model=User,
            form_class=SettingsForm,
        ), 
        name='settings',
    ),

]
