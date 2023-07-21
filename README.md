# Email Auto-Drafter

This is a Python script that uses the Gmail API to fetch unread emails, generates responses using a local AI model, and saves these responses as drafts in Gmail.

## Setup

1. Clone this repository to your local machine.
2. Install the required Python packages by running the following command in your terminal:
```sh
pip install -r requirements.txt
```
3. Set up a project in the Google API Console, enable the Gmail API, and download the `credentials.json` file. For detailed instructions, please refer to the [Google API Python Client's User Guide](https://googleapis.github.io/google-api-python-client/docs/).
4. Place the `credentials.json` file in the same directory as your Python script.
5. Adjust the settings in `settings.json` to match your setup. You can specify the AI model and the Gmail scopes.
6. Run the script by executing the following command in your terminal:
```sh
python main.py
```

## How it works

The script performs the following steps in a loop:

1. Connects to Gmail using OAuth 2.0.
2. Fetches unread emails.
3. Parses the email content.
4. Sends the email content to a local server running an AI model to generate a response.
5. Creates a draft in Gmail with the generated response.

The script sleeps for an hour between each loop.

## Logging

The script logs information and error messages to a file named `app.log`. This can be used to monitor the script's operation and troubleshoot any issues.

## Note

This script is intended to be run locally on a user's machine. The user must be able to open a web browser on the machine to authorize the script with their Google account.
