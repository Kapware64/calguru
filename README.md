# CalGuru

## Running app
* Navigate to project root.
* Execute `pip3 install -r requirements.txt` to install required packages.
* Execute `python3 calguru.py` to run app.

## Running Tests
* Ensure you have required packages installed.
* Navigate to project root.
* Run `nose2 -v`.

## Configuring Google Calendar API
* All Google Calendar API calls are done via a single Google account (currently thecalguru@gmail.com).
* To change the Google account used for Google Calender API calls, follow these steps:
    * Delete `gcal_credentials.json` in the `conf` folder.
    * Navigate to the `scripts` folder and run `python3 gcal_oauth.py` to activate new Google sign-in flow.
    * Sign into new Google account.
