from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.views.generic import FormView
from django_registration.backends.activation.views import (
    RegistrationView as BaseRegistrationView, 
    ActivationView as BaseActivationView,
    )   
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

from .forms import PasswordChangeUserForm, RegistrationForm

class PasswordChangeView(BasePasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    template_name = 'password_change_form.html'
    form_class = PasswordChangeUserForm

    def get_success_url(self):
        try:
            url = super().get_success_url()
        except ImproperlyConfigured:
            url = self.request.user.get_absolute_url()
        return url

# class RegistrationView(BaseRegistrationView):
#     email_body_html_template = 'accounts/activation_email_body.html'
#     email_body_template = 'accounts/activation_email_body.txt'
#     email_subject_template = 'accounts/activation_email_subject.txt'

#     def send_activation_email(self, user):
#         """
#         Send the activation email. The activation key is the username,
#         signed using TimestampSigner.
#         """
#         activation_key = self.get_activation_key(user)
#         context = self.get_email_context(activation_key)
#         context["user"] = user
#         subject = render_to_string(
#             template_name=self.email_subject_template,
#             context=context,
#             request=self.request,
#         )
#         # Force subject to a single line to avoid header-injection
#         # issues.
#         subject = "".join(subject.splitlines())
#         body = render_to_string(
#             template_name=self.email_body_template,
#             context=context,
#             request=self.request,
#         )

#         html_message = render_to_string(
#             template_name=self.email_body_html_template,
#             context=context,
#             request=self.request,
#         )

#         user.email_user(subject, body, html_message=html_message)

class ActivationView(BaseActivationView):
    template_name = 'accounts/activation_failed.html',
    success_url = reverse_lazy('activation_complete')

    def activate(self, *args, **kwargs):
        try:
            user = super().activate(*args, **kwargs)
        except:
            print('error!')
        else:
            print('-----------------No error----------------')


class RegistrationView(FormView):
    form_class = RegistrationForm
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
