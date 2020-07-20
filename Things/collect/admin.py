from django.contrib import admin
from .models import Transaction, Transaction_ObjectType, ObjectType, PublicRecord

admin.site.register(Transaction)
admin.site.register(Transaction_ObjectType)
admin.site.register(ObjectType)
admin.site.register(PublicRecord)
