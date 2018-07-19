"""Methods commonly used across unit tests."""

import arrow
from src.api.gcal_api import GoogleCalendarApi
from os.path import join, dirname, realpath


class TestUtils(object):
    """Class for implementing unit test utility methods."""

    # Location of main Google service account's credentials.
    # Used to reassign GoogleCalendarApi.service_account_dir back to its normal
    # value after it's temporarily changed for testing.
    GCAL_MAIN_CREDENTIALS_DIR = GoogleCalendarApi.service_account_dir

    # The main calendar gcal_api.py accesses.
    # Used to reassign GoogleCalendarApi.calendar back to its normal value after
    # it's temporarily changed for testing.
    GCAL_MAIN_CALENDAR = GoogleCalendarApi.calendar_id

    # Milliseconds in an hour
    HOURS_MILLIS = 3600

    @staticmethod
    def configure_gcal_for_testing():
        """
        Change GoogleCalendarApi class attributes for testing purposes.
        """

        # Change Google service account credentials for testing purposes
        GoogleCalendarApi.service_account_dir = \
            join(dirname(realpath(__file__)),
                 '../../conf/test_gcal_service_account.json')

        # Change the calendar gcal_api.py accesses for testing purposes.
        # 'primary' means the primary calendar of the Google service account
        # being used.
        GoogleCalendarApi.calendar_id = 'primary'

    @staticmethod
    def configure_gcal_main():
        """
        Change GoogleCalendarApi class attributes back to their normal values.
        Should be called after configure_gcal_for_testing.
        """

        # Change Google service account credentials back to main service account
        GoogleCalendarApi.credentials_dir = TestUtils.GCAL_MAIN_CREDENTIALS_DIR

        # Change the calendar gcal_api.py accesses back to main calendar
        GoogleCalendarApi.calendar_id = TestUtils.GCAL_MAIN_CALENDAR

    @staticmethod
    def get_gcal_event_timestamps(event):
        """
        Returns an input Google Calendar event's start and end times as UTC
        timestamps.
        Input event should be a dict following how events are represented in Google
        Calendar API (https://developers.google.com/calendar/v3/reference/events#resource).
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
