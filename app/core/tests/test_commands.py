"""
Test custom django management commands
"""
# from unittest.mock import patch, MagicMock

# from psycopg2 import OperationalError as Psycopg2OpError

# from django.core.management import call_command
# from django.db.utils import OperationalError
# from django.test import TestCase, SimpleTestCase

# todo fix these

# @patch('django.db.connections')
# class TestWaitForDatabaseCommand(SimpleTestCase):
#     """Test wait_for_db command"""

#     def test_wait_for_db_ready(self, mock_connections):
#         """Test command completes when database is ready"""
#         mock_cursor = MagicMock()
#         mock_connections.__getitem__.return_value.cursor = mock_cursor

#         call_command('wait_for_db')

#         # Check connections['default'] was called once with 'default' value
#         mock_connections.__getitem__.assert_called_once_with('default')

#         # Check cursor() was called once
#         mock_cursor.assert_called_once()
#         self.assertEqual(mock_cursor.call_count, 1)

#     @patch('time.sleep')
#     def test_wait_for_db_retry(self, mock_sleep, mock_connections):
#         """Test the command when the database raises exceptions and eventually succeeds"""
#         # Create a mock cursor object
#         mock_cursor = MagicMock()
#         result_mock = MagicMock()
#         result_mock.return_value = True
#         # Set up the side effect to simulate the sequence of exceptions
#         # Raise Psycopg2OpError twice, then OperationalError three times, then succeed with a callable lambda
#         mock_cursor.side_effect = [Psycopg2OpError] * 2 + \
#             [OperationalError] * 3 + [result_mock]

#         # Ensure that when connections['default'] is accessed, it returns the mock connection
#         mock_connections.__getitem__.return_value.cursor = mock_cursor

#         # Call the command
#         call_command('wait_for_db')

#         # Ensure the cursor was called 6 times (2 Psycopg2OpError + 3 OperationalError + 1 success)
#         self.assertEqual(mock_cursor.call_count, 6)

#         # Ensure connections['default'] was called 6 times (once for each attempt)
#         self.assertEqual(mock_connections.__getitem__.call_count, 1)

#         # Check that connections['default'] was called with the 'default' parameter
#         mock_connections.__getitem__.assert_called_with('default')
