from django import forms
from .models import Transaction

class TransactionEditForm(forms.ModelForm):
    full_name       = forms.CharField()
    phone           = forms.CharField()
    class Meta:
        model = Transaction
        fields = ('collecting_date', 'address', 'detail_address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['full_name'].initial = instance.user.full_name
            self.fields['phone'].initial = instance.user.phone

    # def clean_full_name(self):
    #     pass

    # def clean_phone(self):
    #     pass

    def save(self, commit=True):
        transaction = super().save(commit=False)

        # editing user
        requesting_user = transaction.user
        requesting_user.full_name = self.cleaned_data['full_name']
        requesting_user.phone = self.cleaned_data['phone']
        requesting_user.save()

        transaction.save()
        return transaction
        # need to do smt here to update the full_name thing
