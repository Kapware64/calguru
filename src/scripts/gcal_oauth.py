"""
Authenticates Google Calendar API credentials and stores them in
gcal_credentials.json. Account used to sign in with here is used for all Google
Calendar API calls.
"""

from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# Facilitate Google OAuth sign-in via browser
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('../conf/gcal_credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(
        '../conf/gcal_client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
