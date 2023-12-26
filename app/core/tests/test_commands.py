from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


"""
This indicates that the behaviour of the check method call in the
Command class is modified. A call to check method within the test
is replaced with patched_check.
"""


@patch('core.management.commands.wait_for_db.Command.check')
class CommandsTest(SimpleTestCase):

    def test_wait_for_db(self, patched_check):
        """ Test waiting for the DB till the DB is ready """
        # patched_check is the mocked check method from the Command class
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    # we add patch at the method level as the patched sleep method is used
    # only within this method
    # the args are applied inside out - method level first, then the class
    # level
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test exception thrown when waiting for the DB to start """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEquals(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
