from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from mailing.timezones import USER_POSSIBLE_TIMEZONES

class MailingList(models.Model):
    registered_at = models.DateTimeField(
        'Зарегистрирован',
        db_index=True
        )
    message = models.TextField('Сообщение клиенту')
    closed_at = models.DateTimeField(
        'Дата и время окончания рассылки',
        db_index=True
        )
    sending_time_start = models.TimeField('Время начала рассылки')
    sending_time_end = models.TimeField('Время окончания рассылки')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        short_message = self.message[:20]
        return f'{self.registered_at} {short_message}'


class Client(models.Model):
    TIMEZONES = tuple(zip(USER_POSSIBLE_TIMEZONES, USER_POSSIBLE_TIMEZONES))
    phonenumber = PhoneNumberField(
        'Номер телефона',
        region='RU'
    )
    mobile_operator_code = models.CharField('Код мобильного оператора', max_length=10)
    tag = models.SlugField('Тег')
    client_timezone = models.CharField(
        'Часовой пояс',
        max_length=32,
        choices=TIMEZONES,
        default='UTC'
        )


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
        db_index=True,
        auto_now_add=True
        )
    deliver_time = models.TimeField(
        'Время отравки сообщения',
        db_index=True,
        null=True
        )
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=REGISTERED
    )
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        related_name='messages',
        on_delete=models.CASCADE
        )
    mailing = models.ForeignKey(
        MailingList,
        verbose_name='Рассылки',
        related_name='messages',
        on_delete=models.CASCADE
        )
