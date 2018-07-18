import unittest
import arrow
import calguru
import bson
import bson.json_util
from webtest import TestApp
from src.api.gcal_api import GoogleCalendarApi
from test.test_helpers.test_utils import TestUtils


class CalGuruTest(unittest.TestCase):
    """Test calguru.py"""

    def setUp(self):
        """Executed before each test."""

        # Create test app to mimic calguru.py
        self.app = TestApp(calguru.app)

        # Change GoogleCalendarApi class attributes for testing purposes
        TestUtils.configure_gcal_for_testing()

    def tearDown(self):
        """Executed after each test."""

        # Change GoogleCalendarApi class attributes back to their normal values
        TestUtils.configure_gcal_main()

    def test_create_gcal_events(self):
        """Test we can add event via POST /gcal_events REST API endpoint"""

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

        # Event to create
        event_missing_fields = {
            'summary': "Test"
        }

        # Make valid post-add request
        valid_resp = self.app.post_json(
            '/gcal/events', {'events': [event]})

        # Assert successful status code
        self.assertEqual(valid_resp.status_code, 200)

        # Get event in calendar
        event_in_cal_id = bson.json_util.loads(valid_resp.body.decode(
            "utf-8"))['data']['calendar_events'][0]['id']
        event_in_cal = GoogleCalendarApi.get_event(event_in_cal_id)

        # UTC timestamps of created event in Google Calendar
        start_time_in_cal, end_time_in_cal = \
            TestUtils.get_gcal_event_timestamps(event_in_cal)

        # Ensure event added to calendar is correct
        self.assertEqual(event_in_cal.get('summary'), "Test")
        self.assertEqual(event_in_cal.get('attendees')[0].get('email'),
                         "test.thecalguru@gmail.com")
        self.assertEqual(start_time_in_cal, utc_timestamp_jan_2)
        self.assertEqual(
            end_time_in_cal, utc_timestamp_jan_2 + 5 * TestUtils.HOURS_MILLIS)
        self.assertEqual(event_in_cal.get('description'), "A test event")
        self.assertEqual(event_in_cal.get('location'), "MongoDB")

        # Remove added event from Google Calendar
        GoogleCalendarApi.delete_event(event_in_cal_id)

        # Make invalid post-add request
        invalid_resp = self.app.post_json(
            '/gcal/events', {'events': [event_missing_fields]}, expect_errors=True)

        # Assert failed status code
        self.assertEqual(invalid_resp.status_code, 400)

    if __name__ == "__main__":
        unittest.main()
