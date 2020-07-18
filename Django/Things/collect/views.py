from datetime import timedelta
import json

from django.views.generic.base import TemplateView
from django.views.generic import UpdateView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

from collect.models import Transaction, Transaction_ObjectType, PublicRecord
from .forms import TransactionEditForm

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'collect/home.html'

    def get_context_data(self, **kwargs):
        context = {
            'user_full_name': self.request.user.full_name,
            'user_next_collection': self.user_next_collection,
            'user_data': self.user_data,
            'public_data': self.public_data,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    @property
    def user_data(self):
        try:
            by_month = list(self.request.user.completed_transactions.group_by_month())
            by_type = list(self.request.user.completed_transactions.group_by_type())

            data = {
            'by_month': json.dumps(by_month),
            'by_type': json.dumps(by_type),
            }
        except self.request.user.NoTransactionAvailable:
            data = None
        return data

    @property
    def user_next_collection(self):
        try:
            timestamp_next_collection = json.dumps(self.request.user.next_collection.timestamp() * 1000) # for miliseconds
            # maybe better if we get the latest one and validate it in template
        except self.request.user.NoNextCollection:
            timestamp_next_collection = None
        return timestamp_next_collection

    @property
    def public_data(self):
        try:
            latest = PublicRecord.objects.latest('date_added')
            data = {
                'by_type': latest.by_type,
                'by_month': latest.by_month
            }
        except PublicRecord.DoesNotExist:
            data = None
        return data

class TransactionEditView(LoginRequiredMixin, UpdateView):
    template_name = 'collect/booking.html'
    form_class = TransactionEditForm
    success_url = reverse_lazy('collect:index')
    is_update_view = True

    def get_object(self):
        requesting_user = self.request.user
        try:
            transaction = Transaction.objects.filter(user_id=requesting_user.id, is_active=True).get()
        except Transaction.DoesNotExist:
            self.is_update_view = False
            transaction = Transaction(user=requesting_user, address=requesting_user.address, detail_address=requesting_user.detail_address)
            if transaction is None:
                print("Is None!")
            else:
                print("Not None")
        return transaction

    def get_context_data(self, **kwargs):
        context = {
            'is_update_view': self.is_update_view
        }
        context.update(kwargs)
        return super().get_context_data(**context)

class LandingPage(TemplateView):
    template_name = 'collect/landing_page.html'

class LienHe(TemplateView):
    template_name = 'collect/Lien_he.html'

class VeChungToi(TemplateView):
    template_name = 'collect/Ve_chung_toi.html'