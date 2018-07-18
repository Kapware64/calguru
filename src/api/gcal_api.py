"""Methods for interacting with Google Calendar API."""

import arrow
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from os.path import join, dirname, realpath
import src.errors.gcal_errors as gcal_errors


class GoogleCalendarApi(object):
    """All methods for interacting with Google Calendar API."""

    # Specifies read/write access to Google Calendar via service account
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # id of calendar that Google Calendar API calls access.
    # Every calendar in Google Calendar has a unique id.
    calendar_id = '9bd42tmt32q8sk200sappvmm6s@group.calendar.google.com'

    # Location of Google service account credentials file. This file specifies
    # the Google service account that CalGuru uses for making authenticated
    # calls to Google Calendar API.
    service_account_dir = join(dirname(realpath(__file__)),
                               '../../conf/gcal_service_account.json')

    @staticmethod
    def get_service():
        """
        Returns Resource object for interacting with Google Calendar
        API or throws error if valid Google credentials are not found.

        Looks for credentials in file specified by CREDENTIALS_DIR.
        """

        # Get Google service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            GoogleCalendarApi.service_account_dir,
            scopes=GoogleCalendarApi.SCOPES)

        # Return Resource object
        return discovery.build('calendar', 'v3', credentials=credentials,
                               cache_discovery=False)

    @classmethod
    def batch_create_events(cls, event_dicts, send_notifications=True):
        """
        Creates Google Calendar events and returns list of dicts containing
        events' ids, summaries, and links.

        :param event_dicts: List of dicts, where each dict specifies an event.
           The following dict keys are supported (keys match Google Calendar API
           keys for event creation):
           'summary': Event summary. Required.
           'start': UTC timestamp of event starting time. Required.
           'end': UTC timestamp of event ending time. Required.
           'attendees' = List of attendee emails.
           'description' = Event description.
           'location' = Event location.
        :param send_notifications: Boolean specifying whether to send
           notifications about creation of events (includes invitations).
           Defaults to true.
        :return: List of dicts containing created events' ids, summaries, and
           links.
        """

        # Mandatory fields that need to be specified for each event
        mandatory_event_fields = ['summary', 'start', 'end']

        # All valid event fields supported in batch_create_events
        all_event_fields = mandatory_event_fields + ['description', 'location', 'attendees']

        # Resource object for interacting with Google Calendar API
        service = cls.get_service()

        # List of dicts containing created events' ids and links; returned at
        # end of method
        ret_events_info = []

        # Initialize batch create event operation with callback for assigning ret_events_info
        def event_created(_, response, exception):  # Called every time event is created
            if exception:
                raise exception
            ret_events_info.append({'id': response.get('id'), 'summary': response.get('summary'),
                                    'link': response.get('htmlLink')})
        batch = service.new_batch_http_request(callback=event_created)

        # Iterate through each input event dict
        for event_dict in event_dicts:

            # Mandatory event fields aren't all specified for input event dict; raise error
            if not set(mandatory_event_fields).issubset(set(event_dict.keys())):
                raise gcal_errors.MissingEventFields(
                    "Mandatory fields (summary, start time, and end time) "
                    "weren't all specified for event.")

            # Input event dict has invalid times; raise error
            if event_dict.get('start') >= event_dict.get('end'):
                raise gcal_errors.InvalidEventTime(
                    "Google Calendar event creation with start time after or "
                    "equal to end time was attempted.")

            # Event to be added to Google Calendar
            gcal_event = {}

            # Add fields to gcal_event
            for key, value in event_dict.items():
                if value and key in all_event_fields:
                    if key == 'attendees':
                        value = [{'email': email} for email in value]
                    if key == 'start' or key == 'end':
                        value = {
                            'dateTime': arrow.get(value).isoformat('T'),  # RFC3339 format
                            'timeZone': 'UTC',
                        }
                    gcal_event[key] = value

            # Add create event operation to batch operation
            batch.add(service.events().insert(
                calendarId=GoogleCalendarApi.calendar_id, body=gcal_event,
                sendNotifications=send_notifications))

        # Batch create events (batch.execute() will call event_created for every
        # single event creation operation before returning)
        batch.execute()

        # Returns created events' _ids, summaries, and links
        return ret_events_info

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
            return service.events().get(calendarId=GoogleCalendarApi.calendar_id,
                                        eventId=id).execute()
        except HttpError:

            # Event with input id couldn't be found; return None
            return None

    @classmethod
    def delete_event(cls, id):
        """
        Deletes event with input event id from Google Calendar.
        Throws googleapiclient.errors.HttpError if event with input id
        doesn't exist or has already been deleted.
        """

        # Resource object for interacting with Google Calendar API
        service = cls.get_service()

        # Delete event with input event id from Google Calendar
        service.events().delete(calendarId=GoogleCalendarApi.calendar_id,
                                eventId=id).execute()
