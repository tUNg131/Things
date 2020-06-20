from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy

from .models import User
from .forms import LoginForm, RegisterForm

class LoginUser(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

class RegisterUser(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')

class Settings(UpdateView):
    template_name = 'accounts/settings.html'
    model = User
    fields = ['full_name', 'email', 'location', 'detail_address', 'phone']

class LogoutUser(LogoutView):
    next_page = reverse_lazy('accounts:login')
    template_name = 'accounts/logout.html'
