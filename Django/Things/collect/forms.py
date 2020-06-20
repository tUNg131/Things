from django.forms import ModelForm
from .models import Transaction

class TransactionCreationForm(ModelForm):
    class Meta:
        model = Transaction
        
