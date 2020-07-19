import json

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import (
    ExtractYear, ExtractMonth
)
from django.db.models import F, Sum

class Transaction(models.Model):
    user            = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='transactions')
    date_added  = models.DateTimeField(_('Date added'), default=timezone.now)
    collecting_date = models.DateTimeField(_('Collecting date'))
    is_active       = models.BooleanField(_('Is active transaction? Required.'), default=True)
    address        = models.ForeignKey('accounts.Location', on_delete=models.CASCADE, null=True, blank=True) # related_name
    detail_address  = models.CharField(
        _('Detail address'),
        max_length=256,
        help_text=_('Required for collections. 256 characters or fewer.'),
        blank=True
        )

    def __str__(self):
        transaction_objecttype_list = ""
        for _transaction_objectype in self.transaction_objecttype.all():
            transaction_objecttype_list += f"[{_transaction_objectype.objecttype.type_name}: {_transaction_objectype.quantity} {_transaction_objectype.objecttype.unit}]"
        return f"({self.user}) submitted: {self.date_added} - " + transaction_objecttype_list


class ObjectType(models.Model):
    type_name            = models.CharField(
        _('Object type name'),
        max_length=256,
        help_text=_(
            'The name of the object type.  '
            '256 characters or fewer.'
        )
    )

    price_max           = models.CharField(
        _('Maximum object type price'),
        max_length=9,
        help_text=_(
            'The price of the type.  '
            'The unit is in VND.  '
            '9 characters or fewer.'
        )
    )

    price_min           = models.CharField(
        _('Minimum object type price'),
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
        return f"{self.type_name}: {self.price_min} - {self.price_max} VND per {self.unit}."

class TransactionQuerySet(models.QuerySet):
    def group_by_type(self):
        return self.select_related('object_type')\
        .defer(
            'transaction_id',
            'objecttype__price_max',
            'objecttype__price_min',
        ).values(type_name=F('objecttype__type_name'))\
        .annotate(total_quantity=Sum('quantity'))\
        .order_by('-total_quantity')

    def group_by_month(self):
        return self.select_related('object_type')\
        .defer(
            'transaction_id',
            'objecttype__price_max',
            'objecttype__price_min',
        )\
        .annotate(month=ExtractMonth('transaction__collecting_date'), year=ExtractYear('transaction__collecting_date'))\
        .values('month', 'year').order_by('year', 'month')\
        .annotate(total_quantity=Sum('quantity'))

class Transaction_ObjectType(models.Model):
    transaction         = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='transaction_objecttype')
    objecttype          = models.ForeignKey('ObjectType', on_delete=models.CASCADE, related_name='transaction_objecttype')
    quantity            = models.IntegerField(
        _('Quantity'),
        help_text=_(
            'Transaction - ObjectType quantity.'
        )
    )

    def __str__(self):
        return f"({self.transaction.user}) submitted: {self.transaction.date_added} - {self.objecttype.type_name}: {self.quantity} {self.objecttype.unit}"

    objects = TransactionQuerySet.as_manager()

    @classmethod
    def get_public_by_type(cls):
        try:
            by_type = Transaction_ObjectType.objects.filter(transaction__is_active=False).group_by_type()
            data = json.dumps(list(by_type))
        except Transaction_ObjectType.DoesNotExist:
            data = 'No data are available'
        return data

    @classmethod
    def get_public_by_month(cls):
        try:
            by_month = Transaction_ObjectType.objects.filter(transaction__is_active=False).group_by_month()
            data = json.dumps(list(by_month))
        except Transaction_ObjectType.DoesNotExist:
            data = 'No data are available'
        return data

class PublicRecord(models.Model):
    by_type = models.TextField(
        _('Public record grouped by type'),
        default=Transaction_ObjectType.get_public_by_type
    )
    by_month = models.TextField(
        _('Public record grouped by month'),
        default=Transaction_ObjectType.get_public_by_month
    )
    date_added = models.DateTimeField(_('Time added'),default=timezone.now)

    def __str__(self):
        return f"Public record at {self.date_added}"
