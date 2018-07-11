from bottle import route, run
from src.api.gcal_api import GoogleCalendarApi


@route('/')
def index():
    """Home page."""

    return "CalGuru"


@route('/upcoming')
def upcoming():
    """
    Returns json describing next upcoming event in Google Calendar.
    Can be used as simple sanity check for connection to Google Calendar.
    """

    return GoogleCalendarApi.get_next_event()


# Should match valid redirect uris in OAuth client secret files
run(host='localhost', port=8080, debug=True)
