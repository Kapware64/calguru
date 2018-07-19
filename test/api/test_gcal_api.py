"""Test Google Calendar API methods."""

import unittest
import arrow
from src.api.gcal_api import GoogleCalendarApi
from test.test_helpers.assertions import Assertions
from test.test_helpers.test_utils import TestUtils
import src.errors.gcal_errors as gcal_errors


class GoogleCalenderApiTest(unittest.TestCase):
    """
    Test gcal_api.py.
    """

    def setUp(self):
        """Executed before each test."""

        # Change GoogleCalendarApi class attributes for testing purposes
        TestUtils.configure_gcal_for_testing()

    def tearDown(self):
        """Executed after each test."""

        # Change GoogleCalendarApi class attributes back to their normal values
        TestUtils.configure_gcal_main()

    def test_batch_create_get_event(self):
        """
        Test creating events in batches and getting events via Google Calendar
        API.
        """

        # UTC timestamp representing 10am, May 9th, 2018
        utc_timestamp_may_9 = arrow.get(2018, 5, 9, 10).timestamp

        # UTC timestamp representing now
        utc_timestamp_now = arrow.utcnow().timestamp

        # Attempt to create Google Calendar event without all mandatory fields
        # specified; ensure correct error is thrown
        event_missing_fields = \
            {'summary': "Event With Missing Fields"}
        Assertions.assert_bad_op_error(
            self, GoogleCalendarApi.batch_create_events,
            gcal_errors.MissingEventFields,
            "Error: event with missing mandatory fields was successfully created.",
            **{'event_dicts': [event_missing_fields]})

        # Attempt to create Google Calendar event with invalid times;
        # ensure correct error is thrown
        event_invalid_times = \
            {'summary': "Test Invalid",
             'start': utc_timestamp_may_9 + 1 * TestUtils.HOURS_MILLIS,
             'end': utc_timestamp_may_9}
        Assertions.assert_bad_op_error(
            self, GoogleCalendarApi.batch_create_events, gcal_errors.InvalidEventTime,
            "Error: event with invalid start times was successfully created.",
            **{'event_dicts': [event_invalid_times]})

        # Valid events to add to Google Calendar
        event_past = {
            'summary': "Test 1",
            'start': utc_timestamp_may_9,
            'end': utc_timestamp_may_9 + 5 * TestUtils.HOURS_MILLIS,
            'attendees': ["test.thecalguru@gmail.com"],
            'description': 'A test event #1',
            'location': 'MongoDB'
        }
        event_future = {
            'summary': "Test 2",
            'start': utc_timestamp_now + 2 * TestUtils.HOURS_MILLIS,
            'end': utc_timestamp_now + 7 * TestUtils.HOURS_MILLIS,
            'attendees': ["test.thecalguru@gmail.com"],
            'description': 'A test event #2',
            'location': 'MongoDB'
        }

        # Batch create Google Calendar events and store returned events info
        events_gcal_info = GoogleCalendarApi.batch_create_events([event_past, event_future])

        # Iterate through event info of created events
        for event_gcal_info in events_gcal_info:

            # Get created event in Google Calendar
            event_in_cal = GoogleCalendarApi.get_event(event_gcal_info.get('id'))

            # UTC timestamps of created event in Google Calendar
            start_time_in_cal, end_time_in_cal = \
                TestUtils.get_gcal_event_timestamps(event_in_cal)

            # Ensure created event is correct
            if event_in_cal.get('summary') == "Test 1":
                self.assertEqual(event_in_cal.get('attendees')[0].get('email'),
                                 "test.thecalguru@gmail.com")
                self.assertEqual(start_time_in_cal, utc_timestamp_may_9)
                self.assertEqual(
                    end_time_in_cal, utc_timestamp_may_9 + 5 * TestUtils.HOURS_MILLIS)
                self.assertEqual(event_in_cal.get('description'), "A test event #1")
                self.assertEqual(event_in_cal.get('location'), "MongoDB")
            elif event_in_cal.get('summary') == "Test 2":
                self.assertEqual(event_in_cal.get('attendees')[0].get('email'),
                                 "test.thecalguru@gmail.com")
                self.assertEqual(
                    start_time_in_cal, utc_timestamp_now + 2 * TestUtils.HOURS_MILLIS)
                self.assertEqual(
                    end_time_in_cal, utc_timestamp_now + 7 * TestUtils.HOURS_MILLIS)
                self.assertEqual(event_in_cal.get('description'), "A test event #2")
                self.assertEqual(event_in_cal.get('location'), "MongoDB")
            else:
                self.assertTrue(False, msg="Event was created with incorrect summary.")

            # Delete created event
            GoogleCalendarApi.delete_event(event_in_cal.get('id'))

    def test_delete_event(self):
        """
        Test deleting an event via Google Calendar API.
        """

        # UTC timestamp representing 2pm, January 2nd, 2017
        utc_timestamp_jan_2 = arrow.get(2017, 1, 2, 14).timestamp

        # Event to create
        event = {
            'summary': "Test",
            'start': utc_timestamp_jan_2,
            'end': utc_timestamp_jan_2 + 5 * TestUtils.HOURS_MILLIS,
            'attendees': ["test.thecalguru@gmail.com"],
            'description': 'A test event',
            'location': 'MongoDB'
        }

        # Create event in Google Calendar and store returned event info
        event_gcal_info = GoogleCalendarApi.batch_create_events([event])[0]

        # Delete created event
        GoogleCalendarApi.delete_event(event_gcal_info.get('id'))

        # Get deleted event in Google Calendar
        deleted_event = GoogleCalendarApi.get_event(event_gcal_info.get('id'))

        # Event's status field should be 'cancelled' if event is not None
        if deleted_event:
            self.assertEqual('cancelled', deleted_event.get('status'))

    if __name__ == "__main__":
        unittest.main()
