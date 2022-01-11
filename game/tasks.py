from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.management import call_command


@shared_task(name='update_db')
def update_db():
    """Celery task for database update"""

    call_command("update_db", )
