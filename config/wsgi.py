"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


from apscheduler.schedulers.background import BackgroundScheduler
from scripts.task import get_data_from_mailing_model_and_send_mail


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
scheduler = BackgroundScheduler()
scheduler.add_job(get_data_from_mailing_model_and_send_mail, 'interval', seconds=10)
scheduler.start()


