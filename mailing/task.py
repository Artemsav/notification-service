import requests
import pytz
import datetime
from celery.utils.log import get_task_logger

from .models import Message, Client, MailingList
from testfeed.celery import app
import testfeed.settings as setting


logger = get_task_logger(__name__)


@app.task(bind=True, retry_backoff=True)
def send_message(self, data, client_id, mailing_id):
    url = setting.END_POINT_URL
    token = setting.API_TOKEN
    mail = MailingList.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    timezone = pytz.timezone(client.client_timezone)
    now = datetime.datetime.now(timezone)

    if mail.time_start <= now.time() <= mail.time_end:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
        except requests.exceptions.RequestException as exc:
            logger.error(f'Message {data["id"]} is not sent, error is {exc}')
            raise self.retry(exc=exc)
        else:
            logger.info(f"Message id: {data['id']}, message status: 'DELIVERED'")
            Message.objects.filter(pk=data['id']).update(status='DELIVERED')
    else:
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                     int(mail.time_start.strftime('%H:%M:%S')[:2]))
        Message.objects.filter(pk=data['id']).update(status='POSTPONED')
        logger.info(f"Message id: {data['id']}, \
                     message status: 'POSTPONED', \
                     will be sent in {60*60*time} seconds")
        return self.retry(countdown=60*60*time)
