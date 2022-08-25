from django.contrib import admin
from mailing.models import Client, MailingList, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(MailingList)
class MailingAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
