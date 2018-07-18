# CalGuru

## Running app
* Navigate to project root.
* Execute `pip install -r requirements.txt` to install required packages.
* Execute `python calguru.py` to run app.

## Running Tests
* Ensure you have required packages installed.
* Navigate to project root.
* Run `nose2 -v`.

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
        * This can be done in the Google Calendar UI by sharing a Google
        Calendar with the service account's email address.
            * Read/write access must be specified when sharing.
            * The service account's email address can be found in
            `gcal_service_account.json`.
        * This can also be done by having the service account create its own
        Google Calendar.
            * Google Calendar API is required for this. You can use this API endpoint:
            https://developers.google.com/calendar/v3/reference/calendars/insert.
    * Replace `GoogleCalendarApi.calendar_id` with new calendar's id.
