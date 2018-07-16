"""
Authenticates Google Calendar API credentials and stores them in file specified
by src/api/gcal_api's GoogleCalendarApi.credentials_dir.
"""

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from src.api.gcal_api import GoogleCalendarApi

# Credential storage location
store = file.Storage(GoogleCalendarApi.credentials_dir)

# Currently stored credentials (if they exist)
creds = store.get()

# Credentials don't currently exist or are invalid
if not creds or creds.invalid:

    # Facilitate Google OAuth sign-in via browser
    flow = client.flow_from_clientsecrets(
        GoogleCalendarApi.CLIENT_SECRET_DIR, GoogleCalendarApi.SCOPE)
    creds = tools.run_flow(flow, store)

# Ensure we can get Resource object for interfacing with Google Calendar API
discovery.build('calendar', 'v3', http=creds.authorize(Http()))
