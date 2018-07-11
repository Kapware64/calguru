"""Google calendar errors"""


class GoogleCalendarError(Exception):
    """All google calendar errors"""

    def __init__(self, message):
        self.message = message


class BadCredentials(GoogleCalendarError):
    """Valid credentials could not be found for Google Calendar API"""

    pass
