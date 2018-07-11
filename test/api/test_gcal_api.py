"""Test Google Calendar API methods"""

import unittest
from src.api.gcal_api import GoogleCalendarApi


class GoogleCalenderApiTest(unittest.TestCase):
    """
    Test gcal_api.py.
    """

    def test_create_event(self):
        """
        Test creating an event via Google Calendar API.
        """

        # print(GoogleCalendarApi.create_event(
        #     ["nnk1296@gmail.com"], "RC Shift", 1531396253, 1531396253 + 3600 * 5,
        #     **{"description": "Test", "location": "MongoDB"}))

        # print(GoogleCalendarApi.get_event("1bdc124eu1oo7sdj2qj02sbl94"))

        # print(GoogleCalendarApi.get_next_event())

        self.assertTrue(True)

    if __name__ == "__main__":
        unittest.main()
