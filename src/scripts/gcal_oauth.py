"""
Authenticates Google Calendar API credentials and stores them in
gcal_credentials.json. Account used to sign in with here is used for all Google
Calendar API calls.
"""

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from src.api.gcal_api import GoogleCalendarApi

# Location credentials will be stored
store = file.Storage(GoogleCalendarApi.credentials_dir)

# Currently stored credentials (if they exist)
creds = store.get()

# Check if credentials don't currently exist or are invalid
if not creds or creds.invalid:

    # Facilitate Google OAuth sign-in via browser
    flow = client.flow_from_clientsecrets(
        GoogleCalendarApi.CLIENT_SECRET_DIR, GoogleCalendarApi.SCOPE)
    creds = tools.run_flow(flow, store)

# Ensure we can get Resource object for interfacing with Google Calendar API
discovery.build('calendar', 'v3', http=creds.authorize(Http()))
