from django.contrib import admin
from mailing.models import Client, MailingList, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(MailingList)
class MailingAdmin(admin.ModelAdmin):

    inlines = [
        MessageInline

    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass