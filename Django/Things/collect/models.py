from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    user            = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='transaction_set')
    submitted_date  = models.DateTimeField(_('Submitted date'), default=timezone.now)
    finished_date   = models.DateTimeField(_('Finished date'), blank=True, null=True)
    done            = models.BooleanField(_('Is done Transaction?'), blank=True, default=False)

    def __str__(self):
        pass

class ObjectType(models.Model):
    name            = models.CharField(
        _('Object type name'),
        max_length=256,
        help_text=_(
            'The name of the object type.  '
            '256 characters or fewer.'
        )
    )

    price           = models.CharField(
        _('Object type price'),
        max_length=9,
        help_text=_(
            'The price of the type.  '
            'The unit is in VND.  '
            '9 characters or fewer.'
        )
    )

    unit            = models.CharField(
        _('Object type unit'),
        max_length=256,
        help_text=_(
            'The unit of the object type.  '
            '256 characters or fewer.'
        )

    )

    def __str__(self):
        return f"{self.name}: {self.price} VND per {self.unit}."

class Transaction_ObjectType(models.Model):
    transaction         = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='transaction_objecttype')
    objecttype          = models.ForeignKey('ObjectType', on_delete=models.CASCADE, related_name='transaction_objecttype')
    quantity            = models.CharField(
        _('Quantity'),
        max_length=4,
        help_text=_(
            'Transaction - ObjectType quantity.  '
            '4 characters or fewer.'
        )
    )
