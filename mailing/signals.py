from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import MailingList, Client, Message
from .tasks import send_message


@receiver(post_save, sender=MailingList, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        mailing = MailingList.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(Q(mobile_operator_code=mailing.mobile_operator_code) |
                                        Q(tag=mailing.tag))
        for client in clients:
            Message.objects.create(
                sending_status="No sent",
                client_id=client.id,
                mailing_id=instance.id
            )
            if instance.to_send:
                send_message.apply_async(expires=mailing.closed_at)
            else:
                send_message.apply_async(eta=mailing.registered_at, expires=mailing.closed_at)
