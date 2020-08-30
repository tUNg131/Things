import json
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from collect.models import Transaction, PublicRecord
# from .forms import TransactionEditForm
from django.shortcuts import redirect

from accounts.models import User

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "collect/user_detail.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = {
            'user_next_collection': self.user_next_collection,
            'user_data': self.user_data,
            'public_data': self.public_data,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    @property
    def user_data(self):
        try:
            by_month = list(self.object.completed_transactions.group_by_month())
            by_type = list(self.object.completed_transactions.group_by_type())

            data = {
            'by_month': json.dumps(by_month),
            'by_type': json.dumps(by_type),
            }
        except User.NoTransactionAvailable:
            data = None
        return data

    @property
    def user_next_collection(self):
        try:
            timestamp_next_collection = json.dumps(self.object.next_collection.timestamp() * 1000) # for miliseconds
            # maybe better if we get the latest one and validate it in template
        except User.NoNextCollection:
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

class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "collect/user_settings.html"

# class TransactionEditView(LoginRequiredMixin, UpdateView):
#     template_name = 'collect/booking.html'
#     form_class = TransactionEditForm
#     success_url = reverse_lazy('index')
#     is_update_view = True

#     def get_object(self):
#         requesting_user = self.request.user
#         try:
#             transaction = Transaction.objects.filter(user_id=requesting_user.id, is_active=True).get()
#         except Transaction.DoesNotExist:
#             self.is_update_view = False
#             transaction = Transaction(user=requesting_user, address=requesting_user.address, detail_address=requesting_user.detail_address)
#             if transaction is None:
#                 print("Is None!")
#             else:
#                 print("Not None")
#         return transaction

#     def get_context_data(self, **kwargs):
#         context = {
#             'is_update_view': self.is_update_view
#         }
#         context.update(kwargs)
#         return super().get_context_data(**context)

class LandingPage(TemplateView):
    template_name = 'collect/landing_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.user)
        else:
            return super().get(request, *args, **kwargs)

