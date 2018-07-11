"""
Authenticates Google Calendar API credentials and stores them in
gcal_credentials.json. Account used to sign in with here is used for all Google
Calendar API calls.
"""

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from src.api.gcal_api import GoogleCalendarApi

# Facilitate Google OAuth sign-in via browser
store = file.Storage(GoogleCalendarApi.CREDENTIALS_DIR)
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(
        GoogleCalendarApi.CLIENT_SECRET_DIR, GoogleCalendarApi.SCOPE)
    creds = tools.run_flow(flow, store)
service = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
