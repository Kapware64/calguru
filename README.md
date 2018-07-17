# CalGuru

## Running app
* Navigate to project root.
* Execute `pip install -r requirements.txt` to install required packages.
* Execute `python calguru.py` to run app.

## Running Tests
* Ensure you have required packages installed.
* Navigate to project root.
* Run `nose2 -v`.

## Configuring Google Calendar API
* All Google Calendar API calls are done via a single Google service account 
authorized for the calguru-210514 Google Cloud Platform project.
* The Google Cloud Platform project and Google service account that CalGuru 
interfaces with are both specified via the `gcal_service_account.json` file.
    * This can be changed by doing the following:
        * Create a new Google service account.
        * Download its private key in json format.
        * Replace `gcal_service_account.json` with downloaded file.
        * More information available here: https://developers.google.com/identity/protocols/OAuth2ServiceAccount

## Configuring Calendars
* All Google Calendar API calls currently access the calendar with id
`GoogleCalendarApi.calendar_id`. To change this:
    * Ensure CalGuru's Google service account has read/write access to a new
    calendar.
        * This can be done in the Google Calendar UI by sharing a Google
        Calendar with the service account's email address.
            * Read/write access must be specified when sharing.
            * The service account's email address can be found in
            `gcal_service_account.json`.
        * This can also be done by having the service account create its own
        Google Calendar.
            * Google Calendar API is required for this. Can use this API endpoint:
            https://developers.google.com/calendar/v3/reference/calendars/insert.
    * Replace `GoogleCalendarApi.calendar_id` with new calendar's id.
