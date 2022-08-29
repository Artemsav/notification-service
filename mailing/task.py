import requests
import pytz
import datetime
from celery.utils.log import get_task_logger

from .models import Message, Client, MailingList
from testfeed.celery import app
import testfeed.settings as setting
from mailing.exceptions import EndPointServerError


logger = get_task_logger(__name__)


@app.task(bind=True, autoretry_for=(EndPointServerError,), retry_backoff=True)
def send_message(self):
    url = setting.END_POINT_URL
    token = setting.API_TOKEN
    mailings = MailingList.objects.all
    for mailing in mailings:
        clients = Client.objects.all()
        for client in clients:
            timezone = pytz.timezone(client.client_timezone)
            now = datetime.datetime.now(timezone)
            data = {}
            data['id']=client.id
            data['phone']=client.phonenumber
            data['text']=mailing.message
            message_id = 1###
            if mailing.sending_time_start <= now.time() <= mailing.sending_time_end:
                header = {
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'}
                try:
                    requests.post(url=url + message_id, headers=header, json=data)
                    logger.info(f"Message id: {data['id']}, message status: 'DELIVERED'")
                    Message.objects.filter(pk=data['id']).update(status='DELIVERED')
                except EndPointServerError as exc:
                    logger.error(f'Message {data["id"]} is not sent, error is {exc}')
                    raise self.retry(exc=exc)
            else:
                time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                             int(mailing.sending_time_start.strftime('%H:%M:%S')[:2]))
                Message.objects.filter(pk=data['id']).update(status='POSTPONED')
                logger.info(f"Message id: {data['id']}, \
                        message status: 'POSTPONED', \
                        will be sent in {60*60*time} seconds")
                return self.retry(countdown=60*60*time)

@app.task(bind=True, autoretry_for=(EndPointServerError,), retry_backoff=True)
def send_message(self, data, client_id, mailing_id):
    url = setting.END_POINT_URL
    token = setting.API_TOKEN
    mailing = MailingList.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    timezone = pytz.timezone(client.client_timezone)
    now = datetime.datetime.now(timezone)

    if mailing.sending_time_start <= now.time() <= mailing.sending_time_end:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
            logger.info(f"Message id: {data['id']}, message status: 'DELIVERED'")
            Message.objects.filter(pk=data['id']).update(status='DELIVERED')
        except EndPointServerError as exc:
            logger.error(f'Message {data["id"]} is not sent, error is {exc}')
            raise self.retry(exc=exc)
    else:
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                     int(mailing.sending_time_start.strftime('%H:%M:%S')[:2]))
        Message.objects.filter(pk=data['id']).update(status='POSTPONED')
        logger.info(f"Message id: {data['id']}, \
                     message status: 'POSTPONED', \
                     will be sent in {60*60*time} seconds")
        return self.retry(countdown=60*60*time)