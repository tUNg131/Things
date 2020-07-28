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
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured

from .models import User
from .forms import LoginForm, RegisterForm

class LoginUser(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

class RegisterUser(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

class Settings(UpdateView):
    template_name = 'accounts/settings.html'
    model = User
    fields = ['full_name', 'email', 'phone', 'address', 'detail_address']

class LogoutUser(LogoutView):
    next_page = reverse_lazy('landing_page')

class PasswordChangeUser(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')

    def get_success_url(self):
        try:
            url = super().get_success_url()
        except ImproperlyConfigured:
            url = self.request.user.get_absolute_url()
        return url


class PasswordChangeDoneUser(PasswordChangeDoneView):
    pass

class PasswordResetUser(PasswordResetView):
    pass

class PasswordResetDoneUser(PasswordResetDoneView):
    pass

class PasswordResetConfirmUser(PasswordResetConfirmView):
    pass

class PasswordResetCompletleUser(PasswordResetCompleteView):
    pass