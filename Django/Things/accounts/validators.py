from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class PhoneNumberValidator(RegexValidator):
    regex = '^(\+84\s?|0)(3[2-9]|5[25689]|7[06789]|8[1-9]|9[^\D5])\d{7}$'
    source = 'https://vi.wikipedia.org/wiki/Mã_điện_thoại_Việt_Nam'
    message = _('Invalid vietnamese phone number.')
