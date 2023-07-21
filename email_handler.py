from googleapiclient.errors import HttpError
import base64
import logging

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_unread_emails(service):
    try:
        result = service.users().messages().list(userId='me', q="is:unread").execute()
        messages = result.get('messages', [])
        return messages
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def parse_email_content(service, email):
    try:
        message = service.users().messages().get(userId='me', id=email['id']).execute()
        payload = message['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")

        data = parts[0]
        data_bytes = data['body']['data']
        decoded_data = base64.urlsafe_b64decode(data_bytes)
        str_data = decoded_data.decode('utf-8')
        return str_data
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def create_draft(service, email, draft_response):
    try:
        message_body = {
            'raw': draft_response
        }
        message = service.users().drafts().create(userId='me', body=message_body).execute()
        logging.info(f'Draft id: {message["id"]} created.')
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
