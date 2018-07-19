"""Generic error thrown by application."""


class CalGuruError(Exception):
    """Any custom error thrown by CalGuru when some check is failed."""

    def __init__(self, message):
        self.message = message
