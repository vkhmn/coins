import time

from django.core.management import BaseCommand

from apps.coins.tasks import collect, send_messages


class Command(BaseCommand):
    """Django command to periodically collect coins and send messages."""

    def handle(self, *args, **options):
        while True:
            try:
                collect()
                send_messages()
            except Exception as e:
                print(e)
            print('Sleep 60 * 60')
            time.sleep(60 * 60)
