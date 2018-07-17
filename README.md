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
