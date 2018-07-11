"""Methods for interacting with Google Calendar API"""

from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file
from os.path import join, dirname, realpath
import datetime
import src.errors.gcal_errors as gcal_errors


class GoogleCalendarApi(object):
    """All methods for interacting with Google Calendar API"""

    # Specifies read/write access to Google Calendar
    SCOPE = 'https://www.googleapis.com/auth/calendar'

    # Location of Google Calendar API credential storage
    CREDENTIALS_DIR = join(dirname(realpath(__file__)),
                           '../../conf/gcal_credentials.json')

    # Location of Google Calendar API OAuth client secret
    CLIENT_SECRET_DIR = join(dirname(realpath(__file__)),
                             '../../conf/gcal_client_secret.json')

    @staticmethod
    def get_service():
        """
        Returns Resource object for interacting with Google Calendar
        API or throws error if valid Google credentials are not found.
        """

        # Get credentials
        store = file.Storage(GoogleCalendarApi.CREDENTIALS_DIR)
        creds = store.get()

        # Raise error if credentials are invalid
        if not creds or creds.invalid:
            raise gcal_errors.BadCredentials(
                "Valid credentials could not be found for Google Calendar API")

        # Return Resource object
        return discovery.build('calendar', 'v3', http=creds.authorize(Http()))

    @classmethod
    def get_next_event(cls):
        """
        Retrieves dict representing next event in Google Calendar.
        """

        # Resource object for interacting with Google Calendar API
        service = cls.get_service()

        # Present time in UTC
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        # Next event in Google Calendar (list of size 0 or 1)
        event_result = service.events().list(calendarId='primary', timeMin=now,
                                             maxResults=1, singleEvents=True,
                                             orderBy='startTime').execute()
        event_list = event_result.get('items', [])

        # Create event to return
        event = {}
        if len(event_list) > 0:
            start = event_list[0]['start'].get('dateTime', event_list[0]['start'].get('date'))
            event = {'start': start, 'summary': event_list[0]['summary']}
        return event
