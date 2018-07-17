import unittest
import arrow
import calguru
from webtest import TestApp


class CalGuruTest(unittest.TestCase):
    """Test calguru.py"""

    # Milliseconds in an hour
    HOURS_MILLIS = 3600

    def setUp(self):
        """Setup method for testing"""

        self.app = TestApp(calguru)

    def tst_create_gcal_events(self):
        """Test we can add event via POST /gcal_events REST API endpoint"""

        # UTC timestamp representing 2pm, January 2nd, 2017
        utc_timestamp_jan_2 = arrow.get(2017, 1, 2, 14).timestamp

        # Event to create
        event = {
            'summary': "Test",
            'start': utc_timestamp_jan_2,
            'end': utc_timestamp_jan_2 + 5 * CalGuruTest.HOURS_MILLIS,
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

        # Make invalid post-add request
        invalid_resp = self.app.post_json(
            '/gcal/events', {'events': [event_missing_fields]})

        # Assert failed status code
        self.assertEqual(invalid_resp.status_code, 400)

    if __name__ == "__main__":
        unittest.main()
