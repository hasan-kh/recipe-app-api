"""
Django command to wait for the database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Django command to wait for database'

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        connection = connections['default']
        counter = 1
        while db_up is False:
            try:
                # Try to establish a connection to database
                # This will raise an exception if the database is down
                print('counter= ', counter)
                counter += 1
                connection.cursor()
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
