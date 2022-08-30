# Generated by Django 4.0.7 on 2022-08-30 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_alter_client_client_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='deliver_time',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='Время отравки сообщения'),
        ),
        migrations.AlterField(
            model_name='message',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Зарегистрирован'),
        ),
    ]