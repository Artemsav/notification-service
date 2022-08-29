from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from mailing.models import Client, MailingList, Message
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer
from django.urls import reverse
from django.http import HttpResponseRedirect


def redirect2admin(request):
    return HttpResponseRedirect(reverse('admin:index'))


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        allow_empty = False
        fields = '__all__'


class MailingListSerializer(ModelSerializer):

    class Meta:
        model = MailingList
        allow_empty = False
        fields = '__all__'


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        allow_empty = False
        fields = '__all__'


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()

    @action(detail=True)
    def get_info(self, request, pk=None):
        get_object_or_404(MailingList, pk=pk)
        messages = Message.objects.filter(mailing_id=pk)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_fullinfo(self, request):
        total_count = MailingList.objects.count()
        mailings = MailingList.objects.all()
        content = {'Total number of mailings': total_count,
                   'The number of messages sent': ''}
        result = {}

        for mailing in mailings:
            mailing_summary = {}
            mail = Message.objects.filter(mailing_id=mailing.id)
            group_sent = mail.filter(status='DELIVERED').count()
            group_no_sent = mail.filter(status='POSTPONED').count()
            group_registered = mail.filter(status='REGISTERED').count()
            mailing_summary['Total messages'] = len(mail)
            mailing_summary['DELIVERED'] = group_sent
            mailing_summary['POSTPONED'] = group_no_sent
            mailing_summary['REGISTERED'] = group_registered
            result[f'MailingList#id:{mailing.id}'] = mailing_summary

        content['The number of messages sent'] = result
        return Response(content)
