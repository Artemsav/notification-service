import requests
import pytz
import datetime
from celery.utils.log import get_task_logger

from .models import Message, Client, MailingList
from testfeed.celery import app
import testfeed.settings as setting
from mailing.exceptions import EndPointServerError


logger = get_task_logger(__name__)


@app.task
def say_hello():
    logger.info(f"I say hello")


@app.task(bind=True, autoretry_for=(EndPointServerError,), retry_backoff=True)
def send_message(self):
    url = setting.END_POINT_URL
    token = setting.API_TOKEN
    status_to_be_send = ['PO', 'REG']
    mailings = (
        MailingList.objects.prefetch_related('messages')
                           .filter(messages__status__in=status_to_be_send)
                    )
    for mailing in mailings:
        for message in mailing.messages.all():
            client = message.client
            timezone = pytz.timezone(client.client_timezone)
            now = datetime.datetime.now(timezone)
            data = {}
            data['id'] = client.id
            data['phone'] = str(client.phonenumber)
            data['text'] = mailing.message
            message_id = message.id
            if mailing.sending_time_start <= now.time() <= mailing.sending_time_end:
                header = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'}
                try:
                    requests.post(url=f'{url}{message_id}', headers=header, json=data)
                    Message.objects.filter(pk=message.id).update(status='DE')
                    deliver_time = now.time().strftime('%H:%M:%S')
                    Message.objects.filter(pk=message.id).update(deliver_time=deliver_time)
                    logger.info(f"Message id: {message.id}, message status: 'DELIVERED'")
                except EndPointServerError as exc:
                    logger.error(f'Message {message.id} is not sent, error is {exc}')
                    raise self.retry(exc=exc)
            else:
                time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                             int(mailing.sending_time_start.strftime('%H:%M:%S')[:2]))
                Message.objects.filter(pk=message_id).update(status='PO')
                logger.info(f"Message id: {data['id']}, \
                        message status: 'POSTPONED', \
                        will be sent in {60*60*time} seconds")
                return self.retry(countdown=60*60*time)
