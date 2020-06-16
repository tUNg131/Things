from datetime import timedelta
import json as _json

from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q, Sum
from django.db.models.functions import (
    ExtractYear, ExtractMonth
)
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User
from collect.models import Transaction, Transaction_ObjectType

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'collect/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        transaction_history = {
            'by_type_json':          self._get_json_by_type(),
            'by_month_json':         self._get_json_by_month(),
            'next_collection_json':  self._get_json_next_collection()
        }
        context['transaction_history'] = transaction_history
        return context

    def _get_json_next_collection(self):
        try:
            timestamp_next_collection = User.objects\
                .get(pk=self.request.user.id)\
                .transactions.get(is_active=True)\
                .collecting_date.timestamp() * 1000 # for miliseconds # maybe better if we get the latest one and validate it in template
            json = _json.dumps(
                {'data': timestamp_next_collection}
            )
        except Transaction.DoesNotExist:
            json = None
        return json

    def _get_json_by_type(self):
        try:
            by_type = self.request.user.pre_transactions()\
                .values(type_name=F('objecttype__type_name'))\
                .annotate(total_quantity=Sum('quantity'))\
                .order_by('-total_quantity')
            json = _json.dumps(
                {'data': list(by_type)},
                cls=DjangoJSONEncoder,
                ensure_ascii=False
            )
        except Transaction_ObjectType.DoesNotExist:
            json = None
        return json

    def _get_json_by_month(self):
        try:
            by_month = self.request.user.pre_transactions()\
                .annotate(month=ExtractMonth('transaction__collecting_date'), year=ExtractYear('transaction__collecting_date'))\
                .values('month', 'year').order_by('year', 'month')\
                .annotate(total_quantity=Sum('quantity'))
            json = _json.dumps(
                {'data': list(by_month)},
                cls=DjangoJSONEncoder,
                ensure_ascii=False
            )
        except Transaction_ObjectType.DoesNotExist:
            json = None
        return json
