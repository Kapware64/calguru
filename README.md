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
