from django.contrib.auth.forms import AuthenticationForm
from django.forms import BooleanField

class LoginForm(AuthenticationForm):
    remember = BooleanField(label="Remember me")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': "Username"})
        self.fields['password'].widget.attrs.update({'placeholder': "Password"})
