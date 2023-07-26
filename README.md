# Email Auto-ReplAI

Email Auto-ReplAI is a Python tool that uses AI to automate drafting responses to unread Gmail messages, streamlining email management tasks. It creates drafts for messages specifically addressed to the user, disregarding messages where the user is only CCed or BCCed. Additionally, the application does not generate drafts for messages from or reply-to a noreply or donotreply address and messages with a List-Unsubscribe header. The application can use either a local AI model or the OpenAI API based on your configuration.

## Setup

1. Clone this repository to your local machine.
2. Install the required Python packages by running the following command in your terminal:
```sh
pip install -r requirements.txt
```
3. Set up a project in the Google API Console, enable the Gmail API, and download the `credentials.json` file. For detailed instructions, please refer to the [Google API Python Client's User Guide](https://googleapis.github.io/google-api-python-client/docs/).
4. Place the `credentials.json` file in the same directory as your Python script.
5. Adjust the settings in `settings.json` to match your setup. You can specify the AI model and the Gmail scopes.
6. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
7. Set the `USE_LOCAL` environment variable to `true` if you want to use a local AI model, or `false` (or leave it unset) if you want to use the OpenAI API.
8. Run the script by executing the following command in your terminal:
```sh
python main.py
```
You can also add the `--local` flag to use the local AI model, regardless of the `USE_LOCAL` environment variable:
```sh
python main.py --local
```

## How it works

The script performs the following steps in a loop:

1. Connects to Gmail using OAuth 2.0.
2. Fetches unread emails.
3. Filters emails based on the specified rules (directly addressed to user, no List-Unsubscribe header, and not from a noreply/donotreply address).
4. Parses the filtered email content.
5. Sends the email content to either a local AI model or the OpenAI API, based on your configuration, to generate a response.
6. Creates a draft in Gmail with the generated response.

The script sleeps for an hour between each loop.

## Logging

The script logs information and error messages to a file named `app.log`. This can be used to monitor the script's operation and troubleshoot any issues.

## Note

This script is intended to be run locally on a user's machine. The user must be able to open a web browser on the machine to authorize the script with their Google account.
