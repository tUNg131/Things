from django.contrib.auth.models import (
    UserManager as BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .validators import phone_number_validator, email_validator

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
         validators=[email_validator],
         help_text=_('Required. 64 characters or fewer.')
    )

    phone           = models.CharField(
        _('Phone number'),
        max_length=16,
        blank=True,
        validators=[phone_number_validator],
        help_text=_('Vietnamese phone number only e.g: +84 999999999, +84999999999 or 0999999999')
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

    address        = models.ForeignKey('accounts.Location', on_delete=models.CASCADE, null=True, blank=True) # related_name

    detail_address  = models.CharField(
        _('Detail address'),
        max_length=256,
        help_text=_('Required for collections. 256 characters or fewer.'),
        blank=True
        )

    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    collecting_day = models.ForeignKey("accounts.Day", verbose_name=_("The day to collect weekly"), on_delete=models.CASCADE, null=True, blank=True)

    collecting_time = models.TimeField(_("Collecting time"), auto_now=False, auto_now_add=False, null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name'] # required by create_superuser() in UserManager

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    class NoTransactionAvailable(Exception):
        pass

    class NoNextCollection(Exception):
        pass

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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("user_detail", kwargs={"pk": self.pk})
    
    @property
    def completed_transactions(self):
        from collect.models import Transaction_ObjectType
        qs = Transaction_ObjectType.objects.filter(transaction__user_id=self.id, transaction__is_active=False)
        if not qs.exists():
            raise type(self).NoTransactionAvailable
        return qs

    @property
    def next_collection(self):
        from collect.models import Transaction
        try:
            colleting_datetime = self.transactions.get(is_active=True).collecting_datetime
        except Transaction.DoesNotExist:
            raise type(self).NoNextCollection
        return colleting_datetime

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

class Day(models.Model):
    name = models.CharField(_("Name of the day"), max_length=15, help_text=_("Name of the day"))
    isoday = models.IntegerField(_("ISO Weekday"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Week'
        managed = True

        verbose_name = 'Day'
        verbose_name_plural = 'Days'
