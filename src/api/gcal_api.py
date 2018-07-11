"""Methods for interacting with Google Calendar API."""

from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file
from os.path import join, dirname, realpath
from datetime import datetime, timezone
from googleapiclient.errors import HttpError
import src.errors.gcal_errors as gcal_errors


class GoogleCalendarApi(object):
    """All methods for interacting with Google Calendar API."""

    # Specifies read/write access to Google Calendar
    SCOPE = 'https://www.googleapis.com/auth/calendar'

    # Location of Google Calendar API credential storage
    CREDENTIALS_DIR = join(dirname(realpath(__file__)),
                           '../../conf/gcal_credentials.json')

    # Location of Google Calendar API OAuth client secret
    CLIENT_SECRET_DIR = join(dirname(realpath(__file__)),
                             '../../conf/gcal_client_secret.json')

    # Which calendar Google Calendar API calls interface with.
    # 'primary' specifies primary calendar.
    CALENDAR = 'primary'

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
        return discovery.build('calendar', 'v3', http=creds.authorize(Http()),
                               cache_discovery=False)

    @classmethod
    def get_next_event(cls):
        """
        Retrieves dict representing next event in Google Calendar.
        """

        # Resource object for interacting with Google Calendar API
        service = cls.get_service()

        # Present time in UTC
        now = datetime.utcnow().isoformat() + 'Z'

        # Next event in Google Calendar (list of size 0 or 1)
        event_result = service.events().list(calendarId=GoogleCalendarApi.CALENDAR,
                                             timeMin=now, maxResults=1, singleEvents=True,
                                             orderBy='startTime').execute()
        event_list = event_result.get('items', [])

        # Create event to return
        event = {}
        if len(event_list) > 0:
            start = event_list[0]['start'].get('dateTime', event_list[0]['start'].get('date'))
            event = {'id': event_list[0]['id'], 'start': start, 'summary': event_list[0]['summary']}
        return event

    @classmethod
    def get_event(cls, id):
        """
        Returns dict containing all information about Google Calendar event with
        input event id.
        Returns None if no such event could be found.
        """

        # Resource object for interacting with Google Calendar API
        service = cls.get_service()

        try:

            # Retrieve and return event with input event id
            return service.events().get(calendarId=GoogleCalendarApi.CALENDAR,
                                        eventId=id).execute()
        except HttpError:

            # Event with input id couldn't be found, return None
            return None

    @classmethod
    def create_event(cls, attendee_emails, summary, start_time, end_time,
                     send_notifications=True, **kwargs):
        """
        Creates a Google Calendar event and returns event's id and link.

                         ====Possible kwargs inputs===

        :param attendee_emails: Emails of all people attending event.
        :param summary: Event summary.
        :param start_time: UTC timestamp of event starting time.
        :param end_time: UTC timestamp of event ending time.
        :param send_notifications: Boolean specifying whether to send
        notifications about creation of event (includes invitations).
        Defaults to true.
        :param kwargs: Supported args:
           'description' = Event description
           'location' = Event location
        :return: Created event's id and link.
        """

        # All of kwargs' valid keys. Matches Google Calendar API keys for
        # insert operation body argument.
        valid_kwargs_keys = ['description', 'location']

        # Resource object for interacting with Google Calendar API
        service = cls.get_service()

        # Event to be added to Google Calendar
        event = {
            'summary': summary,
            'start': {
                'dateTime': datetime.fromtimestamp(start_time, timezone.utc).isoformat('T'),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': datetime.fromtimestamp(end_time, timezone.utc).isoformat('T'),
                'timeZone': 'UTC',
            },
            'attendees': list(map(lambda x: {'email': x}, attendee_emails))
        }

        # Add kwargs args to event
        for key, value in kwargs.items():
            if value and (key in valid_kwargs_keys):
                event[key] = value

        # Do the insertion
        event = service.events().insert(
            calendarId=GoogleCalendarApi.CALENDAR, body=event,
            sendNotifications=send_notifications).execute()

        # Return link to created event
        return {'id': event.get('id'), 'link': event.get('htmlLink')}
