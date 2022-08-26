from django.contrib import admin
from mailing.models import Client, MailingList, Message


class ClientInline(admin.TabularInline):
    model = Client
    extra = 0


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(MailingList)
class MailingAdmin(admin.ModelAdmin):

    list_filter = [
        'clients',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'clients',
        'clients__tag',
    ]

    inlines = [
        ClientInline,
        MessageInline

    ]
