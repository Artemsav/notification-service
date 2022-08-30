from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django.utils import timezone
from .models import MailingList, Client, Message
from .tasks import send_message


@receiver(post_save, sender=MailingList, dispatch_uid="create_mailinglist")
def create_message(sender, instance, created, **kwargs):
    time = timezone.now()
    if created:
        mailing = MailingList.objects.filter(id=instance.id).first()
        clients = Client.objects.all()
        for client in clients:
            Message.objects.create(
                status='REG',
                client_id=client.id,
                mailing_id=instance.id
            )
            if instance.registered_at <= time <= instance.closed_at:
                send_message.apply_async(expires=mailing.closed_at)
            else:
                send_message.apply_async(eta=mailing.registered_at, expires=mailing.closed_at)
