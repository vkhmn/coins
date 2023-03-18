import time

from django.core.management import BaseCommand

from apps.coins.tasks import collect, send_messages
from config.settings.dev import logger


class Command(BaseCommand):
    """Django command to periodically collect coins and send messages."""

    def handle(self, *args, **options):
        while True:
            try:
                collect()
                send_messages()
            except Exception as e:
                logger.error(e)
            logger.info('Sleep 60 * 60')
            time.sleep(60 * 60)
