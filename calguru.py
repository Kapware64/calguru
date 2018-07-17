from bottle import Bottle, route, run, request
from src.api.gcal_api import GoogleCalendarApi
from src.utils.api_utils import APIUtils


@route('/')
def index():
    """Home page."""

    return "CalGuru"


@APIUtils.api_decorator
def create_gcal_events():
    """
    Called when endpoint for creating Google Calendar events is invoked.

    Content-Type: application/json
    Input body: Json with 'events' field containing Json array. Each
    item in array specifies an event and should follow these keys:
       'summary': Event summary. Required.
       'start': UTC timestamp of event starting time. Required.
       'end': UTC timestamp of event ending time. Required.
       'attendees' = List of attendee emails.
       'description' = Event description.
       'location' = Event location.
    Output: Created events' ids, summaries, and links in json.
    """

    # Create events and store Google Calendar info of created events
    gcal_events_info = GoogleCalendarApi.batch_create_events(
        APIUtils.get_body(request)['events'])

    # Return created events' ids, summaries, and links
    return {'calendar_events': gcal_events_info}


@route('/upcoming')
def upcoming():
    """
    Returns json describing next upcoming event in Google Calendar.

    Used as simple sanity check for connection to Google Calendar.
    TODO: Remove before deployment.
    """

    return GoogleCalendarApi.get_next_event()


# Route for creating Google Calendar events
Bottle().post("/gcal/events", callback=create_gcal_events)

# Should match valid redirect uris in OAuth client secret files
run(host='localhost', port=8080, debug=True)
