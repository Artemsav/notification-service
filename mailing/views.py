from django.shortcuts import render
from rest_framework.serializers import ModelSerializer
from mailing.models import Client, MailingList, Message
from rest_framework import viewsets

class ClientSerializers(ModelSerializer):

    class Meta:
        model = Client
        allow_empty = False
        fields = '__all__'


class MailingListSerializers(ModelSerializer):

    class Meta:
        model = MailingList
        allow_empty = False
        fields = '__all__'


class MessageSerializers(ModelSerializer):

    class Meta:
        model = Message
        allow_empty = False
        fields = '__all__'



