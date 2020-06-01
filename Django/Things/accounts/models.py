from django.contrib.auth.models import (
    UserManager as BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class UserManager(BaseUserManager):
    def _create_user(self, full_name, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        if not full_name:
            raise ValueError('The given full name must be set')

        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, full_name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(full_name, email, password, **extra_fields)

    def create_superuser(self, full_name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(full_name, email, password, **extra_fields)

class TransactionHistory(models.Manager):
    all_grouping_methods = () # has to be a tuple
    temp_table_name = ''

    class Result:
        def __init__(self, pk):
            self.user_pk = pk

    def _analyse(self, cursor, *methods):
        result = Result(pk)
        if methods is None:
            methods = all_grouping_methods
        for method in methods:
            try:
                attr = getattr(self, method)
                if callable(attr):
                    _result = attr(cursor)
                    setattr(result, method, _result)
                else:
                    raise AttributeError
            except AttributeError:
                print(f"Doesn't have method {method}")
                raise
        return result

    def analyse(self, pk, *methods):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                # Get the tempTable
            """, self.temp_table_name)
            result = self._analyse(cursor=cursor, *methods)
        return result

    def by_type(self, cursor):
        cursor.execute("""
        """)
        return dictfetchall(cursor)

    def by_month(self, cursor):
        cursor.execute("""
        """)
        return dictfetchall(cursor)

    def next_collection(self, cursor):
        cursor.execute("""
        """)
        return dictfetchall(cursor)

class User(AbstractBaseUser, PermissionsMixin):
    full_name       = models.CharField(
        _('Full name'),
        max_length=64,
        help_text=_('Required. 64 characters or fewer.')
    ) #full_name validator missing

    email           = models.EmailField(
        _('Email address'),
         unique=True,
         max_length=64,
         help_text=_('Required. 64 characters or fewer.')
    )

    location        = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True) # related_name

    detail_address  = models.CharField(
        _('Detail address'),
        max_length=256,
        help_text=_('Required for collections. 256 characters or fewer.'),
        blank=True
    )

    phone           = models.CharField(
        _('Phone number'),
        max_length=16,
        blank=True
    )

    is_staff        = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active       = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    transaction_history = TransactionHistory()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name'] # required by create_superuser() in UserManager

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Location(models.Model):
    city            = models.CharField(
        _('City'),
        max_length=32,
        help_text=_(
            'Name of the city.  '
            '32 characters or fewer.'
        )
    )

    district        = models.CharField(
        _('City'),
        max_length=32,
        help_text=_(
            'Name of the district.  '
            '32 characters or fewer.'
        )
    )

    ward            = models.CharField(
        _('City'),
        max_length=32,
        help_text=_(
            'Name of the ward.  '
            '32 characters or fewer.'
        )
    )
