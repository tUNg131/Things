import os
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class PhoneNumberValidator(RegexValidator):
    """
    Validate whether the phone number has correct Vietnamese form.
    Source: https://vi.wikipedia.org/wiki/Mã_điện_thoại_Việt_Nam
    """
    regex = r'^(\+84\s?|0)(3[2-9]|5[25689]|7[06789]|8[1-9]|9[^\D5])\d{7}$'
    message = _('Invalid vietnamese phone number.')

class EmailValidator(RegexValidator):
    """
    Validate whether the email has a suitable address.
    Source: http://www.ex-parrot.com/~pdw/Mail-RFC822-Address.html
    """
    DEFAULT_EMAIL_REGEX_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'email-regex.txt'
    )
    message = _('Invalid email address.')

    def __init__(self, *args, email_regex_path=DEFAULT_EMAIL_REGEX_PATH, **kwargs):
        with open(email_regex_path, 'r') as file:
            self.regex = file.read().replace('\n', '')
        super().__init__(*args, **kwargs)


phone_number_validator = PhoneNumberValidator()
email_validator = EmailValidator()
