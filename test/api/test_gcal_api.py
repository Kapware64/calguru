"""Test Google Calendar API methods"""

import unittest
import arrow
from os.path import join, dirname, realpath
from src.api.gcal_api import GoogleCalendarApi
from test.test_helpers.assertions import Assertions
import src.errors.gcal_errors as gcal_errors


class GoogleCalenderApiTest(unittest.TestCase):
    """
    Test gcal_api.py.
    """

    # Google Calendar credentials location pointing to credentials
    # of main Google account. Used to reassign CREDENTIALS_DIR back to normal
    # value after it is temporarily changed for testing.
    MAIN_CREDENTIALS_DIR = GoogleCalendarApi.credentials_dir

    def setUp(self):
        """
        Executed before each test.
        """

        # Temporarily change Google Calendar credentials directory location to
        # use credentials of Google account utilized just for testing
        # (test.thecalguru@gmail.com).
        GoogleCalendarApi.credentials_dir = \
            join(dirname(realpath(__file__)), '../../conf/test_gcal_credentials.json')

    def tearDown(self):
        """
        Executed after each test.
        """

        # Change Google Calendar credentials directory location to point back
        # to credentials of main Google account.
        GoogleCalendarApi.credentials_dir = GoogleCalenderApiTest.MAIN_CREDENTIALS_DIR

    def test_create_event(self):
        """
        Test creating an event via Google Calendar API.
        """

        # Milliseconds in an hour
        hour_millis = 3600

        # UTC timestamp representing May 9th, 2018 at 10am
        utc_timestamp_may_9 = 1525860000

        # Attempt to create Google Calendar event with invalid times;
        # ensure correct error is thrown
        Assertions.assert_bad_op_error(
            self, GoogleCalendarApi.create_event, gcal_errors.InvalidEventTime,
            "Error: event with invalid start times was successfully created.",
            **{'attendee_emails': ["test.thecalguru@gmail.com"],
               'summary': "Test Invalid",
               'start_time': utc_timestamp_may_9 + 1 * hour_millis,
               'end_time': utc_timestamp_may_9})

        # Create Google Calendar event
        event = GoogleCalendarApi.create_event(
            ["test.thecalguru@gmail.com"], "Test", utc_timestamp_may_9,
            utc_timestamp_may_9 + 5 * hour_millis,
            **{'description': 'A test event', 'location': 'MongoDB'})

        # Created event in Google Calendar
        event_in_cal = GoogleCalendarApi.get_event(event.get('id'))

        # UTC timestamps of created event in Google Calendar
        start_time_in_cal, end_time_in_cal = \
            GoogleCalenderApiTest.get_event_timestamps(event_in_cal)

        # Ensure created event is correct
        self.assertEqual(event_in_cal.get('attendees')[0].get('email'),
                         "test.thecalguru@gmail.com")
        self.assertEqual(event_in_cal.get('summary'), "Test")
        self.assertEqual(start_time_in_cal, utc_timestamp_may_9)
        self.assertEqual(end_time_in_cal, utc_timestamp_may_9 + 5 * hour_millis)
        self.assertEqual(event_in_cal.get('description'), "A test event")
        self.assertEqual(event_in_cal.get('location'), "MongoDB")

        # Delete created event
        GoogleCalendarApi.delete_event(event.get('id'))

    @staticmethod
    def get_event_timestamps(event):
        """
        Returns an input event's start and end times as UTC timestamps.
        """

        start_time = arrow.get(event.get('start').get('dateTime'))
        start_time_timezone = event.get('start').get('timeZone')
        if start_time_timezone:
            start_time.replace(tzinfo=start_time_timezone)

        end_time = arrow.get(event.get('end').get('dateTime'))
        end_time_timezone = event.get('end').get('timeZone')
        if end_time_timezone:
            end_time.replace(tzinfo=end_time_timezone)

        return start_time.timestamp, end_time.timestamp

    if __name__ == "__main__":
        unittest.main()
