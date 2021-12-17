import time

from django.db import connections

from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django commands to pause execution till database is available"""

    def handle(self, *args, **kwargs):
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                time.sleep(1)
