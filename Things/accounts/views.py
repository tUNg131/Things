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
from .forms import (
    LoginForm, 
    RegisterForm, 
    SettingsForm, 
    PasswordChangeUserForm, 
    PasswordResetUserForm, 
    SetPasswordUserForm,
)

class LoginUser(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

class RegisterUser(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    
    def form_valid(self, form):
        # send_email()
        return super().form_valid(form)

class Settings(UpdateView):
    template_name = 'accounts/settings.html'
    model = User
    form_class = SettingsForm

class LogoutUser(LogoutView):
    next_page = reverse_lazy('landing_page')

class PasswordChangeUser(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    template_name = 'change_password_form.html'
    form_class = PasswordChangeUserForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(context['form'].fields['old_password'].label)
        print(context['form'].as_p())
        return context

    def get_success_url(self):
        try:
            url = super().get_success_url()
        except ImproperlyConfigured:
            url = self.request.user.get_absolute_url()
        return url


class PasswordChangeDoneUser(PasswordChangeDoneView):
    template_name = 'password_change_success.html'
    
class PasswordResetUser(PasswordResetView):
    template_name = 'password_reset.html'
    form_class = PasswordResetUserForm

class PasswordResetDoneUser(PasswordResetDoneView):
    template_name = 'password_reset_letter.html'

class PasswordResetConfirmUser(PasswordResetConfirmView):
    template_name = 'enter_new_password.html'
    form_class = SetPasswordUserForm

class PasswordResetCompletleUser(PasswordResetCompleteView):
    template_name = 'password_reset_success.html'
