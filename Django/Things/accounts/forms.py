from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import BooleanField
from .models import User

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': "Email"})
        self.fields['password'].widget.attrs.update({'placeholder': "Password"})

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'email')
