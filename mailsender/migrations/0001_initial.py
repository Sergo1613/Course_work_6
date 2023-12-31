# Generated by Django 4.2.3 on 2023-11-06 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Почта')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('middle_name', models.CharField(max_length=50, verbose_name='Отчество')),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_of_last_mailing', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время последней рассылки')),
                ('status', models.BooleanField(blank=True, null=True, verbose_name='Статус рассылки')),
            ],
        ),
        migrations.CreateModel(
            name='MailText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='Тема рассылки')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_datetime', models.DateTimeField(verbose_name='Время и дата рассылки')),
                ('every_day', models.BooleanField(default=False, verbose_name='Ежедневная рассылка')),
                ('every_week', models.BooleanField(default=False, verbose_name='Рассылка раз в неделю')),
                ('every_month', models.BooleanField(default=False, verbose_name='Рассылка раз в месяц')),
                ('status', models.BooleanField(default=True, verbose_name='Активировать рассылку')),
                ('date_of_last_sending', models.DateTimeField(blank=True, null=True, verbose_name='Время и дата последней рассылки')),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mailsender.customer')),
                ('logs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailsender.logs')),
                ('messages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailsender.mailtext')),
            ],
        ),
    ]
