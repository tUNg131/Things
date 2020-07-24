# from django import forms
# from .models import Transaction
# from django.core.exceptions import ValidationError

# class TransactionEditForm(forms.ModelForm):
#     full_name       = forms.CharField(required=True)
#     phone           = forms.CharField(required=True)
#     class Meta:
#         model = Transaction
#         fields = ('collecting_datetime', 'address', 'detail_address')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         instance = getattr(self, 'instance', None)
#         if instance:
#             self.fields['full_name'].initial = instance.user.full_name
#             self.fields['full_name'].help_text = instance.user._meta.model.full_name.field.help_text
#             self.fields['phone'].initial = instance.user.phone
#             self.fields['phone'].help_text = instance.user._meta.model.phone.field.help_text

#     def _post_clean(self):
#         super()._post_clean()
#         try:
#             self.instance.user.full_clean()
#         except ValidationError as e:
#             self._update_errors(e)

#     def save(self, commit=True):
#         self.instance.user.full_name = self.cleaned_data['full_name']
#         self.instance.user.phone = self.cleaned_data['phone']
#         self.instance.user.save()
#         return super().save()
