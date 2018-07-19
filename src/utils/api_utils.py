"""Methods commonly used across REST API calls."""

from bottle import response
import bson
from bson import json_util
from src.errors.calguru_error import CalGuruError


class APIUtils(object):
    """Class for implementing API utility methods."""

    @staticmethod
    def api_decorator(func):
        """
        A decorator that wraps the passed in function and redirects to success
        and failure accordingly.
        """

        def make_request(*args, **kwargs):
            """
            Function that makes the actual request and redirects to success
            or failure depending on error exceptions.
            """

            # Try the function and return to success
            try:
                return APIUtils.success(func(*args, **kwargs))

            # Except any errors and call failure
            except Exception as err:
                return APIUtils.failure(err)

        return make_request

    @staticmethod
    def success(data=None):
        """ Method for returning successful API request."""

        # Dictionary to be returned
        ret = {'status': 'success', 'data': data}

        # Set response status
        response.status = 200

        # Return ret as json
        return bson.json_util.dumps(ret)

    @staticmethod
    def failure(error):
        """ Method for returning failed API Request."""

        # If error is custom error thrown by application
        if isinstance(error, CalGuruError):
            ret = {'status': 'error', 'message': error.message}

            # We know application has failed a check and thrown a custom error;
            # set response status for client making a bad request
            response.status = 400

        else:
            ret = {'status': 'error', 'message': str(error)}

            # Set response status for internal service error
            response.status = 500

        # Return error as json
        return bson.json_util.dumps(ret)

    @staticmethod
    def get_body(data):
        """Method to decode and return request body."""

        return bson.json_util.loads(data.body.read().decode('utf-8'))
