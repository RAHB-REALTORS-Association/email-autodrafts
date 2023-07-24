from googleapiclient.errors import HttpError
import base64
import logging
from email.mime.text import MIMEText

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

        # Extract the 'To', 'From', and 'Subject' fields from headers
        email_data = {
            'Body': str_data,
            'To': next(header['value'] for header in headers if header['name'] == 'From'),
            'From': next(header['value'] for header in headers if header['name'] == 'To'),
            'Subject': next(header['value'] for header in headers if header['name'] == 'Subject'),
        }

        if email_data is None:
            logging.error('Failed to parse email content.')
        
        return email_data
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return None

def create_draft(service, user_id, draft_response):
    try:
        # Construct an RFC 2822 message
        message = MIMEText(draft_response['Body'])
        message['to'] = draft_response['To']
        message['from'] = draft_response['To']  # Set 'From' as the 'To' field of the original message
        message['subject'] = draft_response['Subject']
        raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))

        # Create the draft
        message_body = {
            'message': {
                'raw': raw_message.decode('utf-8')
            }
        }
        draft = service.users().drafts().create(userId=user_id, body=message_body).execute()
        logging.info(f'Draft id: {draft["id"]} created.')
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
