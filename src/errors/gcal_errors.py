"""Google calendar errors."""

from src.errors.application_error import ApplicationError


class GoogleCalendarError(ApplicationError):
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
