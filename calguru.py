"""Main app."""

from bottle import Bottle, route, request
from src.api.gcal_api import GoogleCalendarApi
from src.utils.api_utils import APIUtils


def index():
    """Home page."""

    return "CalGuru"


@APIUtils.api_decorator
def create_gcal_events():
    """
    Called when endpoint for creating Google Calendar events is invoked.

    Content-Type: application/json
    Input body: Json with "events" field containing Json array of events to be
    created. Each item in array specifies an event and should follow these keys:
       "summary": Event summary. Required.
       "start": UTC timestamp of event starting time. Required.
       "end": UTC timestamp of event ending time. Required.
       "attendees": List of attendee emails.
       "description": Event description.
       "location": Event location.
    Output: Created events' ids, summaries, and links in json.
    """

    # Create events and store Google Calendar info of created events
    gcal_events_info = GoogleCalendarApi.batch_create_events(
        APIUtils.get_body(request)['events'])

    # Return created events' ids, summaries, and links
    return {'calendar_events': gcal_events_info}


# Initialize main app
app = Bottle()

# Route homepage
app.get("/", callback=index)

# Route for creating Google Calendar events
app.post("/gcal/events", callback=create_gcal_events)


if __name__ == '__main__':

    # Run the application from http://192.168.50.1:8080.
    # Should match scheduling tool's
    # src/utils/calendar_utils.CalendarUtils.CALGURU_BASE_URL.
    app.run(host='192.168.50.1', port=8080)
