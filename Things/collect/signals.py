from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver
from collect.models import PublicRecord, Transaction

def create_new_transaction(instance):
    Transaction.objects.create(user=instance.user)

def create_new_public_record():
    PublicRecord.objects.create()

@receiver(pre_save, sender=Transaction)
def pre_save_check(sender, instance, **kwargs):
    try:
        origin = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # initialize collecting date for newly created Transaction.
        instance._update_collecting_date()
    else:
        # check if the transaction turn into not active (becoming a finished transaction). 
        # If so, create new public record and new transaction.
        if origin.is_active == True and instance.is_active == False:
            #Change is_active from True to False
            create_new_public_record()
            create_new_transaction(instance)

    
