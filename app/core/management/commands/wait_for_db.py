"""
Django command to wait for the DB to be available
"""
from django.core.management.base import BaseCommand
import time
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        This is the entry point that gets called when you
        run the Django command """
        self.stdout.write('waiting for database ...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(
                    'Database unavailable, will check after 1 second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))
