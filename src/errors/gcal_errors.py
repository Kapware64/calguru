"""Google calendar errors."""


class GoogleCalendarError(Exception):
    """All google calendar errors."""

    def __init__(self, message):
        self.message = message


class InvalidEventTime(GoogleCalendarError):
    """
    Invalid event times were specified during event creation (e.g. start time
    after or equal to end time).
    """

    pass


class MissingEventFields(GoogleCalendarError):
    """
    There was an attempt to create an event with missing mandatory fields.
    """

    pass
