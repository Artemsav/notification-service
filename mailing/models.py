from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    phonenumber = PhoneNumberField(
        'Номер телефона',
        region='RU'
    )
    mobile_operator_code = models.CharField('Код мобильного оператора', max_length=10)
    tag = models.SlugField('Тег')
    client_timezone = models.CharField('Часовой пояс', max_length=20)


class MailingList(models.Model):
    registered_at = models.DateTimeField(
        'Зарегистрирован',
        db_index=True
        )
    message = models.TextField('Сообщение клиенту')
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        related_name='mailings',
        on_delete=models.SET_NULL,  # can be kind of draft of mailing without clients? needs to think about
        null=True
        )
    end_time = models.DateTimeField(
        'Время окончания рассылки',
        db_index=True
        )
    time_start = models.TimeField('Время начала рассылки')
    time_end = models.TimeField('Время окончания рассылки')


class Message(models.Model):
    REGISTERED = 'REG'
    POSTPONED = 'PO'
    DELIVERED = 'DE'
    STATUS_CHOICES = [
        (REGISTERED, 'Зерегистрировано'),
        (POSTPONED, 'Ожидает отправки'),
        (DELIVERED, 'Отправлено')
    ]
    registered_at = models.DateTimeField(
        'Зарегистрирован',
        db_index=True
        )
    deliver_time = models.DateTimeField(
        'Время отравки сообщения',
        db_index=True
        )
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=REGISTERED
    )
    client = models.ForeignKey('Клиент', related_name='messages', on_delete=models.CASCADE)
    mailing = models.ForeignKey('Рассылки', related_name='messages', on_delete=models.CASCADE)