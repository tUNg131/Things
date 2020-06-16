from django.db.models.signals import post_save
from django.dispatch import receiver
from collect.models import PublicRecord, Transaction_ObjectType

@receiver(post_save, sender=Transaction_ObjectType)
def update_public_record(sender, **kwargs):
    PublicRecord.objects.create()
    # Create 3 PublicRecord for 3 Transaction_ObjectType when actually only 1 transation select_related
    # better to write Callback when active transaction turn into in-active 
