# CalGuru

## Running app
* Navigate to project root.
* Create `conf` folder:
    * In the `conf` folder, add the following files
        * `gcal_service_account.json`: Contains service account credentials
        (including private key) for making authenticated requests to Google
        Calendar API. More information is given in "Google Calendar
        API Authentication" below.
        * `test_gcal_service_account.json`: Contains service account credentials
        utilized when testing calls to Google Calendar API.
    * All files in the `conf` folder are ignored by git as specified in
    `.gitignore`. This is due to its contents containing sensitive information.
* Execute `pip install -r requirements.txt` to install required packages.
* Execute `python calguru.py` to run app.

## Running Tests
* Ensure you have required packages installed.
* Navigate to project root.
* Run `nose2 -v`.

## Endpoints
* Here are CalGuru's currently supported endpoints:
* `POST /gcal/events`: Creates Google Calendar events.
    * Content-Type: application/json
    * Input body: Json with `events` field containing Json array of events
    to be created. Each item in array specifies an event and should follow these
    keys:
        * `summary`: Event summary. Required.
        * `start`: UTC timestamp of event starting time. Required.
        * `end`: UTC timestamp of event ending time. Required.
        * `attendees`: List of attendee emails.
        * `description`: Event description.
        * `location`: Event location.
    * Example input:
        * ```json
            {
                "events": [
                    {
                        "summary": "Test 1",
                        "start": 1532014225,
                        "end": 1532032225,
                        "attendees": ["noah.kaplan@mongodb.com"],
                        "description": "A test event #1",
                        "location": "MongoDB"
                    },
                    {
                        "summary": "Test 2",
                        "start": 1532021425,
                        "end": 1532039425,
                        "attendees": ["noah.kaplan@mongodb.com"],
                        "description": "test event #2",
                        "location": "MongoDB"
                    }
                ]
            }
            ```
            
    * Output: Created events' ids, summaries, and links in json.
    * Output example:
        * ```json
            {
                "status": "success",
                "data": {
                    "calendar_events": [
                        {
                            "id": "hau4n5e0r5b149gcq89rur3gms",
                            "summary": "Test 1",
                            "link": "<link to event in Google Calendar>"
                        },
                        {
                            "id": "eae5c5e0rfb11fgcq59tx43gmd",
                            "summary": "Test 2",
                            "link": "<link to event in Google Calendar>"
                        }
                    ]
                 }
            }
            ```
    * For each created event, email invites are sent to the emails in 
    `attendees`.

## Google Calendar API Authentication
* Background: A service account is a special Google account that belongs to an
    application instead of a user. Each service account is associated with a
    public-private key pair, which is managed by Google Cloud Platform. This key
    pair is what CalGuru uses to make authenticated requests to the Google
    Calendar API.
* All Google Calender API calls made by CalGuru are via the service account
specified in `gcal_service_account.json`, located in the `conf` folder.
`gcal_service_account.json` contains all of the service account's necessary
OAuth credentials (including its private key) for making authenticated Google
Calendar API requests.
* You can change the service account CalGuru uses by doing the following:
    * Create a new Google service account.
    * Download its private key in json format.
    * Replace `gcal_service_account.json` with downloaded file.
    * More information available here: https://developers.google.com/identity/protocols/OAuth2ServiceAccount

## Configuring Calendars
* All Google Calendar API calls currently access the calendar with id
`GoogleCalendarApi.calendar_id`. To change this:
    * Find a new calendar and ensure CalGuru's Google service account has
    read/write access to it.
        * This can be done in the Google Calendar UI by sharing a calendar
         with the service account's email address.
            * Read/write access must be specified when sharing.
            * The service account's email address can be found in
            `gcal_service_account.json`.
        * This can also be done by having the service account create its own
        Google Calendar.
            * Google Calendar API is required for this. You can use this API endpoint:
            https://developers.google.com/calendar/v3/reference/calendars/insert.
    * Replace `GoogleCalendarApi.calendar_id` with new calendar's id.
