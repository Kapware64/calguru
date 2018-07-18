"""Generic error thrown by application."""


class ApplicationError(Exception):
    """Any custom error thrown by application when some check is failed."""

    def __init__(self, message):
        self.message = message
