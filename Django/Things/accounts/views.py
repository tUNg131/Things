from django.shortcuts import render
from django.contrib.auth.views import LoginView

from .forms import LoginForm

# Create your views here.
class LoginUser(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
