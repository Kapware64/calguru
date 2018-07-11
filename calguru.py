from bottle import route, run
from src.api.gcal_api import GoogleCalendarApi


@route('/')
def index():
    """Home page"""

    return "CalGuru"


@route('/upcoming')
def upcoming():
    """Get the upcoming events in Google Calendar"""

    return GoogleCalendarApi.get_next_event()


# Should match valid redirect uris in OAuth client secret files
run(host='localhost', port=8080, debug=True)
