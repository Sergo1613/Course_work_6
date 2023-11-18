from users.models import User
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    """
    Модель клиента для рассылки
    """
    email = models.EmailField(max_length=100, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    """
    Модель рассылки. В этой модели содержатся ключи ссылающиеся на все остальные модели
    """
    mailing_datetime = models.DateTimeField(verbose_name='Время и дата рассылки')
    every_day = models.BooleanField(default=False, verbose_name='Ежедневная рассылка')
    every_week = models.BooleanField(default=False, verbose_name='Рассылка раз в неделю')
    every_month = models.BooleanField(default=False, verbose_name='Рассылка раз в месяц')
    status = models.BooleanField(default=True, verbose_name='Активировать рассылку')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)
    date_of_last_sending = models.DateTimeField(**NULLABLE, verbose_name='Время и дата последней рассылки')
    messages = models.ForeignKey('MailText', on_delete=models.CASCADE)
    customers = models.ForeignKey('Customer', on_delete=models.DO_NOTHING, verbose_name='Клиент')
    logs = models.ForeignKey('Logs', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'Рассылка {self.pk} от пользователя {self.creator}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailText(models.Model):
    """
    Модель для текста и темы рассылки
    """
    topic = models.CharField(max_length=100, verbose_name='Тема рассылки')
    message = models.TextField(verbose_name='Текст сообщения')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'Текст рассылки'
        verbose_name_plural = 'Тексты рассылок'


class Logs(models.Model):
    """
    Логи рассылки
    """
    datetime_of_last_mailing = models.DateTimeField(**NULLABLE, verbose_name='Дата и время последней рассылки')
    status = models.BooleanField(**NULLABLE, verbose_name='Статус рассылки')


