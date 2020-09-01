from smtplib import SMTPException
from django.conf import settings

from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.contrib.auth import get_user_model

from django.views.generic import FormView, TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.decorators import method_decorator

from .tokens import account_activation_token_generator
from .forms import PasswordChangeUserForm, RegistrationForm

UserModel = get_user_model()

class PasswordChangeView(BasePasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    template_name = 'password_change_form.html'
    form_class = PasswordChangeUserForm

    def get_success_url(self):
        if not self.success_url:
            return self.request.user.get_absolute_url()
        return str(self.success_url)

class RegistrationView(FormView):
    email_template_name = 'accounts/activation_email_body.txt'
    extra_email_context = {
        'expiration_days': settings.PASSWORD_RESET_TIMEOUT_DAYS
    }
    form_class = RegistrationForm
    from_email = None
    html_email_template_name = 'accounts/activation_email_body.html'
    subject_template_name = 'accounts/activation_email_subject.txt'
    success_url = reverse_lazy('register_complete')
    template_name = 'accounts/registration_form.html'
    token_generator = account_activation_token_generator
    disallowed_url = reverse_lazy('register_disallowed')

    # có thể suy nghĩ thêm về việc dùng title tại đây luôn 

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.
        """
        return getattr(settings, "REGISTRATION_OPEN", True)

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        """
        if not self.registration_allowed():
            return HttpResponseRedirect(force_str(self.disallowed_url))
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        try:
            user = form.save(**opts)
        except SMTPException:
            err = ValidationError(_('The email cannot be sent, please check and try again.'))
            form.add_error(None, err)
            return self.form_invalid(form)
        return super().form_valid(form)

INTERNAL_RESET_SESSION_TOKEN = '_account_activation_token'

class ActivationView(TemplateView):
    reset_url_token = 'complete'
    template_name = 'accounts/activation_complete.html'
    token_generator = account_activation_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(
                    INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the success template.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            email_field_name = UserModel.get_email_field_name()
            kwargs = {
                email_field_name: uid
            }

            user = UserModel._default_manager.get(**kwargs)

        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'title': _('Account activation unsuccessful'),
                'validlink': False,
            })
        return context
