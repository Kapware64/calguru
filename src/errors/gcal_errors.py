"""Google calendar errors."""

from src.errors.calguru_error import CalGuruError


class GoogleCalendarError(CalGuruError):
    """All google calendar errors."""

    pass


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
